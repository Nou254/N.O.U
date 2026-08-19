"""
Sliding-window rate limiter.

Used to protect the authentication endpoints against brute force and
credential stuffing (Pentest finding H1), the AI sections, and file uploads.

Multi-worker hardening:
- If ``REDIS_URL`` is set and the ``redis`` package is installed, limits are
  enforced in Redis so every worker shares one counter (correct for
  multi-worker production deployments). Redis failures degrade gracefully to
  the in-memory store rather than crashing requests.
- Otherwise an in-process sliding-window store is used (correct for the
  single-worker development deployment).
"""

import threading
import time
from collections import defaultdict, deque

from fastapi import HTTPException, Request

from app.core.config import settings

try:  # optional dependency - Redis is not required to run the app
    import redis as _redis_pkg  # type: ignore

    _redis = (
        _redis_pkg.Redis.from_url(settings.REDIS_URL, decode_responses=True)
        if settings.REDIS_URL else None
    )
except Exception:  # noqa: BLE001 - package missing / connection refused
    _redis = None

_lock = threading.Lock()
_hits: dict = defaultdict(deque)


def _prune(key: str, window_seconds: float) -> None:
    now = time.monotonic()
    q = _hits[key]
    while q and now - q[0] > window_seconds:
        q.popleft()
    if not q:
        # Drop empty keys so the store cannot grow unboundedly from
        # unique usernames/IPs (memory-exhaustion hardening).
        _hits.pop(key, None)


def _check_redis(full_key: str, max_hits: int, window_seconds: float) -> bool:
    """Redis fixed-window check. Returns True if the request is allowed."""
    if _redis is None:
        return False  # not applicable - use the in-memory store
    try:
        rkey = f"rl:{full_key}"
        count = _redis.incr(rkey)
        if count == 1:
            _redis.expire(rkey, int(window_seconds))
        return count <= max_hits
    except Exception:  # noqa: BLE001 - Redis down: fall back to in-memory
        return False


def check_rate_limit(
    request: Request,
    key: str,
    max_hits: int,
    window_seconds: float,
) -> None:
    """
    Count one hit for ``key`` (scoped by client IP) and raise HTTP 429 with a
    Retry-After header once the sliding window is exhausted.
    """
    client_ip = request.client.host if request.client else "unknown"
    if not allow_request(client_ip, key, max_hits, window_seconds):
        retry_after = int(window_seconds) + 1
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again later.",
            headers={"Retry-After": str(retry_after)},
        )


def allow_request(
    client_ip: str,
    scope: str,
    max_hits: int,
    window_seconds: float,
) -> bool:
    """
    Non-raising sliding-window check for middleware use (DDoS brake).
    Returns True if the request is allowed, False if the window is exhausted.
    Counts one hit when allowed (Redis path counts every probe, like the
    fixed-window check it mirrors).
    """
    full_key = f"{client_ip}:{scope}"

    if _check_redis(full_key, max_hits, window_seconds):
        return True

    with _lock:
        _prune(full_key, window_seconds)
        q = _hits[full_key]
        if len(q) >= max_hits:
            return False
        q.append(time.monotonic())
        return True
