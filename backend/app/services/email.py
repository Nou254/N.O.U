"""
Email delivery service.

Sends transactional email (OTP codes, assessment results) over SMTP using the
settings in app/core/config.py (SMTP_HOST/SMTP_PORT/SMTP_USER/SMTP_PASSWORD
- e.g. Gmail with an app password).

When SMTP is not configured, the service falls back to development mode:
the email body is logged and appended to logs/emails.log so the full flow can
be exercised locally before a real mail account is wired up.

Connectivity hardening: a dead/unreachable SMTP host must NEVER stall a
request for the OS-level connect timeout (up to 30s+ on Windows). The SMTP
client uses a short explicit timeout and a circuit breaker skips SMTP
entirely for a cooldown period after repeated failures, so the app stays
responsive even when the mail host is down (the message still lands in
the dev log).
"""

import asyncio
import logging
import os
import smtplib
import ssl
import threading
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Optional

from app.core.config import settings

logger = logging.getLogger("email")

_DEV_LOG_PATH = Path(__file__).resolve().parent.parent.parent / "logs" / "emails.log"

# ---------------------------------------------------------------------------
# SMTP circuit breaker
# ---------------------------------------------------------------------------
# Short connect timeout: a slow/down SMTP host must not block the request.
SMTP_TIMEOUT_SECONDS = 15
# After this many consecutive failures, stop trying SMTP for a while.
SMTP_MAX_CONSECUTIVE_FAILURES = 3
# Cooldown before trying SMTP again after the breaker opens.
SMTP_BREAKER_COOLDOWN_SECONDS = 60

_smtp_lock = threading.Lock()
_smtp_failures = 0
_smtp_breaker_open_until = 0.0


def _smtp_breaker_allows() -> bool:
    """True when the circuit breaker permits another SMTP attempt."""
    global _smtp_failures, _smtp_breaker_open_until
    with _smtp_lock:
        if time.time() < _smtp_breaker_open_until:
            return False
        return True


def _smtp_breaker_record(success: bool) -> None:
    """Record an SMTP attempt result; opens the breaker after repeated fails."""
    global _smtp_failures, _smtp_breaker_open_until
    with _smtp_lock:
        if success:
            _smtp_failures = 0
            _smtp_breaker_open_until = 0.0
        else:
            _smtp_failures += 1
            if _smtp_failures >= SMTP_MAX_CONSECUTIVE_FAILURES:
                _smtp_breaker_open_until = time.time() + SMTP_BREAKER_COOLDOWN_SECONDS
                logger.warning(
                    "SMTP failed %d times; skipping SMTP for %.0fs (dev-log fallback)",
                    _smtp_failures, SMTP_BREAKER_COOLDOWN_SECONDS,
                )


def _write_dev_log(to: str, subject: str, html_body: str) -> None:
    try:
        _DEV_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(_DEV_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"\n{'=' * 60}\nTO: {to}\nSUBJECT: {subject}\n{html_body}\n")
    except OSError as exc:  # noqa: BLE001
        logger.warning("could not write dev email log: %s", exc)


def _send_smtp(to: str, subject: str, html_body: str) -> None:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = settings.EMAILS_FROM_EMAIL or settings.SMTP_USER
    msg["To"] = to
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    context = ssl.create_default_context()
    port = settings.SMTP_PORT or 587
    with smtplib.SMTP(
        settings.SMTP_HOST, port, timeout=SMTP_TIMEOUT_SECONDS
    ) as server:
        server.ehlo()
        if port == 587:
            server.starttls(context=context)
            server.ehlo()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)


def smtp_configured() -> bool:
    return bool(
        settings.SMTP_HOST and settings.SMTP_USER and settings.SMTP_PASSWORD
    )


async def _deliver(to: str, subject: str, html_body: str) -> bool:
    """
    Attempt SMTP delivery (dev-log fallback when SMTP is missing or down).
    Never raises - delivery is best-effort.
    """
    if not smtp_configured():
        logger.info("[email dev-mode] to=%s subject=%s", to, subject)
        _write_dev_log(to, subject, html_body)
        return False

    # Circuit breaker: if SMTP has been failing recently, skip straight to the
    # dev log so the request never waits on a dead mail host.
    if not _smtp_breaker_allows():
        _write_dev_log(to, subject, html_body)
        return False

    try:
        await asyncio.to_thread(_send_smtp, to, subject, html_body)
        _smtp_breaker_record(success=True)
        logger.info("email sent to %s: %s", to, subject)
        return True
    except Exception as exc:  # noqa: BLE001
        _smtp_breaker_record(success=False)
        logger.error("email to %s failed: %s", to, exc)
        # Fall back to dev log so the message is never silently lost.
        _write_dev_log(to, subject, html_body)
        return False


async def send_email(to: str, subject: str, html_body: str) -> bool:
    """
    Send an HTML email WITHOUT blocking the calling request.

    Delivery runs in a background task, so a slow or unreachable SMTP host
    never stalls an API request (OTP login, registration, etc.). Returns True
    when delivery is queued, False when skipped.
    """
    try:
        asyncio.create_task(_deliver(to, subject, html_body))
        return True
    except RuntimeError:
        # No running event loop (e.g. sync context) - fall back to awaiting.
        return await _deliver(to, subject, html_body)


def otp_email_html(code: str, purpose_label: str, ttl_minutes: int = 10) -> str:
    """HTML template for an OTP verification email."""
    return f"""<!DOCTYPE html>
<html><body style="margin:0;padding:0;font-family:Arial,Helvetica,sans-serif;background:#f1f5f9">
  <div style="max-width:480px;margin:24px auto;background:#ffffff;border-radius:12px;overflow:hidden;border:1px solid #e2e8f0">
    <div style="background:linear-gradient(135deg,#0284c7,#075985);padding:20px 24px">
      <h1 style="color:#ffffff;margin:0;font-size:20px">N.O.U Digital Systems</h1>
    </div>
    <div style="padding:24px">
      <p style="color:#0f172a;font-size:15px">Your one-time verification code for <strong>{purpose_label}</strong> is:</p>
      <div style="background:#f0f9ff;border:1px solid #bae6fd;border-radius:8px;padding:14px;text-align:center;margin:16px 0">
        <span style="font-size:28px;letter-spacing:6px;font-weight:bold;color:#0369a1">{code}</span>
      </div>
      <p style="color:#475569;font-size:13px">This code expires in {ttl_minutes} minutes. If you did not request this, you can safely ignore this email.</p>
    </div>
    <div style="background:#f8fafc;padding:12px 24px;text-align:center">
      <p style="color:#94a3b8;font-size:12px;margin:0">© {__import__('datetime').date.today().year} N.O.U Digital Systems</p>
    </div>
  </div>
</body></html>"""


def onboarding_email_html(
    applicant_name: str,
    assessment_title: str,
    percentage: float,
    login_email: str,
    temp_password: str,
) -> str:
    """HTML template emailed when an admin approves a passed applicant:
    confirms the results and provides the new developer login credentials."""
    return f"""<!DOCTYPE html>
<html><body style="margin:0;padding:0;font-family:Arial,Helvetica,sans-serif;background:#f1f5f9">
  <div style="max-width:560px;margin:24px auto;background:#ffffff;border-radius:12px;overflow:hidden;border:1px solid #e2e8f0">
    <div style="background:linear-gradient(135deg,#0284c7,#075985);padding:20px 24px">
      <h1 style="color:#ffffff;margin:0;font-size:20px">N.O.U Digital Systems — Welcome to the Team!</h1>
    </div>
    <div style="padding:24px">
      <p style="color:#0f172a">Congratulations {applicant_name},</p>
      <p style="color:#0f172a">You passed the <strong>{assessment_title}</strong> assessment with a score of
        <strong>{percentage:.1f}%</strong> and have been <strong>approved</strong> to join N.O.U
        Digital Systems as a developer.</p>
      <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:8px;padding:16px;margin:16px 0">
        <p style="color:#166534;font-weight:bold;margin:0 0 8px">Your new login credentials</p>
        <p style="color:#0f172a;margin:4px 0">Email: <strong>{login_email}</strong></p>
        <p style="color:#0f172a;margin:4px 0">Password: <strong>{temp_password}</strong></p>
        <p style="color:#64748b;font-size:13px;margin:8px 0 0">Sign in at the projects portal and choose the projects you'd like to work on.</p>
      </div>
      <p style="color:#64748b;font-size:13px">Please change your password after your first login. On your first sign-in you will be asked to review and agree to the N.O.U. Organization Policies — the document also remains available on your category page for future reference.</p>
    </div>
    <div style="background:#f8fafc;padding:12px 24px;text-align:center">
      <p style="color:#94a3b8;font-size:12px;margin:0">© {__import__('datetime').date.today().year} N.O.U Digital Systems</p>
    </div>
  </div>
</body></html>"""


def announcement_email_html(body: str, subject: str) -> str:
    """HTML template for batch customer announcements (broadcasts)."""
    safe_body = str(body).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f"""<!DOCTYPE html>
<html><body style="margin:0;padding:0;font-family:Arial,Helvetica,sans-serif;background:#f1f5f9">
  <div style="max-width:560px;margin:24px auto;background:#ffffff;border-radius:12px;overflow:hidden;border:1px solid #e2e8f0">
    <div style="background:linear-gradient(135deg,#0f172a,#1e3a8a);padding:20px 24px">
      <h1 style="color:#ffffff;margin:0;font-size:20px">N.O.U Digital Systems</h1>
    </div>
    <div style="padding:24px">
      <p style="color:#0f172a;font-size:15px;font-weight:bold;margin:0 0 12px">{subject}</p>
      <p style="color:#334155;font-size:14px;line-height:1.6;white-space:pre-wrap">{safe_body}</p>
    </div>
    <div style="background:#f8fafc;padding:12px 24px;text-align:center">
      <p style="color:#94a3b8;font-size:12px;margin:0">© {__import__('datetime').date.today().year} N.O.U Digital Systems</p>
    </div>
  </div>
</body></html>"""


def applicant_credentials_email_html(
    applicant_name: str,
    job_title: str,
    login_email: str,
    temp_password: str,
) -> str:
    """HTML template emailed when a guest applies for a job (no account
    needed): confirms the application and provides the login details used
    to take the assessment. Results are emailed to the same address."""
    return f"""<!DOCTYPE html>
<html><body style="margin:0;padding:0;font-family:Arial,Helvetica,sans-serif;background:#f1f5f9">
  <div style="max-width:560px;margin:24px auto;background:#ffffff;border-radius:12px;overflow:hidden;border:1px solid #e2e8f0">
    <div style="background:linear-gradient(135deg,#0284c7,#075985);padding:20px 24px">
      <h1 style="color:#ffffff;margin:0;font-size:20px">N.O.U Digital Systems — Application Received</h1>
    </div>
    <div style="padding:24px">
      <p style="color:#0f172a">Hello {applicant_name},</p>
      <p style="color:#0f172a">Your application for <strong>{job_title}</strong> has been received.
        Your assessment results will be emailed to <strong>{login_email}</strong>.</p>
      <p style="color:#0f172a">To take the employment assessment, sign in with the temporary credentials below:</p>
      <div style="background:#f0f9ff;border:1px solid #bae6fd;border-radius:8px;padding:16px;margin:16px 0">
        <p style="color:#0f172a;margin:4px 0">Email: <strong>{login_email}</strong></p>
        <p style="color:#0f172a;margin:4px 0">Password: <strong>{temp_password}</strong></p>
        <p style="color:#64748b;font-size:13px;margin:8px 0 0">Sign in at nou.portal and open Employment Assessment.</p>
      </div>
      <p style="color:#64748b;font-size:13px">Please change your password after your first login.</p>
    </div>
    <div style="background:#f8fafc;padding:12px 24px;text-align:center">
      <p style="color:#94a3b8;font-size:12px;margin:0">© {__import__('datetime').date.today().year} N.O.U Digital Systems</p>
    </div>
  </div>
</body></html>"""


def recruitment_email_html(
    applicant_name: str,
    role_title: str,
    login_email: str,
    temp_password: str,
) -> str:
    """HTML template emailed by an administrator when they directly recruit a
    developer (no assessment required). Provides the developer login
    credentials that open the projects portal."""
    return f"""<!DOCTYPE html>
<html><body style="margin:0;padding:0;font-family:Arial,Helvetica,sans-serif;background:#f1f5f9">
  <div style="max-width:560px;margin:24px auto;background:#ffffff;border-radius:12px;overflow:hidden;border:1px solid #e2e8f0">
    <div style="background:linear-gradient(135deg,#0f766e,#155e75);padding:20px 24px">
      <h1 style="color:#ffffff;margin:0;font-size:20px">N.O.U Digital Systems — You're Recruited!</h1>
    </div>
    <div style="padding:24px">
      <p style="color:#0f172a">Hello {applicant_name},</p>
      <p style="color:#0f172a">The N.O.U. administration has <strong>directly recruited</strong> you as
        {role_title}. No assessment is required — your developer account is ready.</p>
      <p style="color:#0f172a">Sign in with the credentials below to access the company projects portal:</p>
      <div style="background:#f0fdfa;border:1px solid #99f6e4;border-radius:8px;padding:16px;margin:16px 0">
        <p style="color:#0f172a;margin:4px 0">Email: <strong>{login_email}</strong></p>
        <p style="color:#0f172a;margin:4px 0">Password: <strong>{temp_password}</strong></p>
        <p style="color:#64748b;font-size:13px;margin:8px 0 0">After your first sign-in, create your company handle (e.g. @yourname)
        so the team can interact with you in the community and on projects.</p>
      </div>
      <p style="color:#64748b;font-size:13px">Please change your password after your first login.</p>
    </div>
    <div style="background:#f8fafc;padding:12px 24px;text-align:center">
      <p style="color:#94a3b8;font-size:12px;margin:0">© {__import__('datetime').date.today().year} N.O.U Digital Systems</p>
    </div>
  </div>
</body></html>"""


def results_email_html(
    applicant_name: str,
    assessment_title: str,
    percentage: float,
    passed: bool,
    module_breakdown: list,
    login_email: str = "",
    temp_password: str = "",
    failure_reasons: list = None,
) -> str:
    """HTML template for the assessment results email (sent 2h after submit).

    - PASS: includes the applicant's login credentials so they can sign in.
    - FAIL: includes the reason(s) for failure (score below the qualifying
      mark, weak sections, and the recommended alternative category).
    """
    rows = "".join(
        f"<tr><td style='padding:8px 12px;border-bottom:1px solid #e2e8f0'>{m['module']}</td>"
        f"<td style='padding:8px 12px;border-bottom:1px solid #e2e8f0;text-align:center'>{m['percentage']:.1f}%</td>"
        f"<td style='padding:8px 12px;border-bottom:1px solid #e2e8f0;text-align:center'>{'Compulsory' if m.get('compulsory') else 'Elective'}</td></tr>"
        for m in module_breakdown
    )
    verdict_color = "#16a34a" if passed else "#dc2626"
    verdict = "PASS" if passed else "FAIL"

    if passed and login_email and temp_password:
        credentials_block = f"""
      <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:8px;padding:16px;margin:16px 0">
        <p style="color:#166534;font-weight:bold;margin:0 0 8px">🎉 Congratulations! You are qualified. Sign in with the credentials below:</p>
        <p style="color:#0f172a;margin:4px 0">Email: <strong>{login_email}</strong></p>
        <p style="color:#0f172a;margin:4px 0">Password: <strong>{temp_password}</strong></p>
        <p style="color:#64748b;font-size:13px;margin:8px 0 0">Sign in at the N.O.U portal and open the Employment Assessment / Results section.
        Please change your password after your first login.</p>
      </div>"""
    else:
        credentials_block = ""

    reasons_block = ""
    if not passed and failure_reasons:
        reasons_items = "".join(
            f"<li style='color:#7f1d1d;margin:4px 0'>{r}</li>" for r in failure_reasons
        )
        reasons_block = f"""
      <div style="background:#fef2f2;border:1px solid #fecaca;border-radius:8px;padding:16px;margin:16px 0">
        <p style="color:#991b1b;font-weight:bold;margin:0 0 8px">Why the assessment was not passed:</p>
        <ul style="margin:0;padding-left:18px">{reasons_items}</ul>
        <p style="color:#64748b;font-size:13px;margin:8px 0 0">You are welcome to retake the assessment for this or a different career.</p>
      </div>"""

    return f"""<!DOCTYPE html>
<html><body style="margin:0;padding:0;font-family:Arial,Helvetica,sans-serif;background:#f1f5f9">
  <div style="max-width:560px;margin:24px auto;background:#ffffff;border-radius:12px;overflow:hidden;border:1px solid #e2e8f0">
    <div style="background:linear-gradient(135deg,#0284c7,#075985);padding:20px 24px">
      <h1 style="color:#ffffff;margin:0;font-size:20px">N.O.U Digital Systems — Assessment Result</h1>
    </div>
    <div style="padding:24px">
      <p style="color:#0f172a">Hi {applicant_name},</p>
      <p style="color:#0f172a">Your results for <strong>{assessment_title}</strong> are ready.</p>
      <div style="text-align:center;margin:16px 0">
        <div style="font-size:40px;font-weight:bold;color:{verdict_color}">{verdict}</div>
        <div style="font-size:22px;color:#334155">Overall score: <strong>{percentage:.1f}%</strong></div>
        <div style="font-size:13px;color:#64748b">Passing requires an overall score of at least 80% (N.O.U. Qualified)</div>
      </div>
      <table style="width:100%;border-collapse:collapse;margin:16px 0;font-size:14px">
        <thead><tr style="background:#f8fafc">
          <th style="padding:8px 12px;text-align:left">Module</th>
          <th style="padding:8px 12px">Score</th>
          <th style="padding:8px 12px">Type</th>
        </tr></thead>
        <tbody>{rows}</tbody>
      </table>
      {credentials_block}
      {reasons_block}
      <p style="color:#64748b;font-size:13px">Detailed AI feedback is available in your applicant dashboard after sign-in.</p>
    </div>
    <div style="background:#f8fafc;padding:12px 24px;text-align:center">
      <p style="color:#94a3b8;font-size:12px;margin:0">© {__import__('datetime').date.today().year} N.O.U Digital Systems</p>
    </div>
  </div>
</body></html>"""
