"""Quick email smoke-test for N.O.U. backend.

Usage:
    python test_mail.py                          # sends to SMTP_USER (self-test)
    python test_mail.py you@gmail.com            # sends to the given address
"""

import os
import sys
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
smtp_port = int(os.getenv("SMTP_PORT", 587))
smtp_user = os.getenv("SMTP_USER")
smtp_password = os.getenv("SMTP_PASSWORD")
from_email = os.getenv("EMAILS_FROM_EMAIL", smtp_user)

# Recipient: command-line arg or fall back to the sender (self-test)
to_email = sys.argv[1] if len(sys.argv) > 1 else smtp_user

if not smtp_user or not smtp_password:
    print("❌ SMTP_USER and SMTP_PASSWORD must be set in backend/.env")
    print("   See backend/.env.example for the required variables.")
    sys.exit(1)

if not to_email:
    print("❌ No recipient specified. Pass an email address or set SMTP_USER.")
    sys.exit(1)

msg = MIMEText(
    "This is a test email from the N.O.U. Digital Systems backend.\n\n"
    "If you received this, SMTP is configured correctly."
)
msg["Subject"] = "N.O.U. - SMTP test email"
msg["From"] = from_email
msg["To"] = to_email

try:
    server = smtplib.SMTP(smtp_host, smtp_port, timeout=10)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(smtp_user, smtp_password)
    server.sendmail(from_email, [to_email], msg.as_string())
    server.quit()
    print(f"✅ Email sent successfully to {to_email}")
except smtplib.SMTPAuthenticationError:
    print("❌ SMTP authentication failed - check SMTP_USER / SMTP_PASSWORD")
    print("   For Gmail, use an App Password (not your account password):")
    print("   https://myaccount.google.com/apppasswords")
except smtplib.SMTPConnectError as e:
    print(f"❌ Could not connect to {smtp_host}:{smtp_port} - {e}")
except Exception as e:
    print(f"❌ Failed: {e}")