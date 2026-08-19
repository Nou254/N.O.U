"""
In-memory OTP (one-time password) store.

OTPs are used for:
- admin login verification (2-step login),
- registration verification (details held in the cache until the OTP is
  verified, then written to the database),
- password recovery.

Process-local store: like the rate limiter and token revocation store, swap
for Redis when the deployment grows to multiple workers.

OTP codes are 6 characters (cryptographically random) and expire after 10
minutes; a limited number of verification attempts is allowed per code.
"""

import secrets
import threading
import time
from typing import Any, Optional

OTP_LENGTH = 6
OTP_TTL_SECONDS = 600  # 10 minutes
MAX_ATTEMPTS = 5

_lock = threading.Lock()
_store: dict = {}  # (purpose, key) -> entry


def _make_code() -> str:
    return secrets.token_hex(3)  # 6 hex characters


def create_otp(
    purpose: str,
    key: str,
    data: Optional[dict] = None,
    ttl: int = OTP_TTL_SECONDS,
) -> str:
    """Create a new OTP for (purpose, key) and return the code."""
    code = _make_code()
    with _lock:
        _store[(purpose, key)] = {
            "code": code,
            "data": data or {},
            "expires_at": time.time() + ttl,
            "attempts": 0,
        }
    return code


def get_otp_data(purpose: str, key: str) -> Optional[dict]:
    """Return the data payload stored with the OTP (without consuming it)."""
    with _lock:
        entry = _store.get((purpose, key))
        if entry and entry["expires_at"] > time.time():
            return entry.get("data")
    return None


def verify_otp(purpose: str, key: str, code: str) -> Optional[dict]:
    """
    Verify a code. Returns the stored data payload on success and consumes
    the OTP. On repeated failures the OTP is consumed too (rate protection).
    """
    code = (code or "").strip()
    with _lock:
        entry = _store.get((purpose, key))
        if not entry:
            return None
        if entry["expires_at"] <= time.time():
            del _store[(purpose, key)]
            return None
        if not secrets.compare_digest(entry["code"], code):
            entry["attempts"] += 1
            if entry["attempts"] >= MAX_ATTEMPTS:
                del _store[(purpose, key)]
            return None
        data = entry.get("data")
        del _store[(purpose, key)]
        return data


def delete_otp(purpose: str, key: str) -> None:
    with _lock:
        _store.pop((purpose, key), None)
