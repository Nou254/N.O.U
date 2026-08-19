"""
Authentication and security utilities.
"""

import threading
import time
import uuid
from datetime import datetime, timedelta
from typing import Optional, Union
import bcrypt
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User


# Bearer token scheme
security = HTTPBearer()


# ---------------------------------------------------------------------------
# Token revocation (Pentest finding L2)
# ---------------------------------------------------------------------------
# Denylist of revoked token jtis (jti -> expiry timestamp). Multi-worker
# hardening: when REDIS_URL is configured the denylist lives in Redis so every
# worker honours logouts; otherwise an in-memory store is used (correct for
# the single-worker development deployment). Redis failures degrade to memory.
_revoked_tokens: dict = {}
_tokens_lock = threading.Lock()


def _revoke_in_redis(jti: str, expires_at: float) -> bool:
    try:
        import redis as _redis_pkg  # optional dependency

        client = _redis_pkg.Redis.from_url(settings.REDIS_URL, decode_responses=True)
        client.set(f"rev:{jti}", "1", ex=max(1, int(expires_at - time.time()) + 1))
        return True
    except Exception:  # noqa: BLE001 - Redis unavailable
        return False


def _revoked_in_redis(jti: str) -> bool:
    try:
        import redis as _redis_pkg

        client = _redis_pkg.Redis.from_url(settings.REDIS_URL, decode_responses=True)
        return bool(client.exists(f"rev:{jti}"))
    except Exception:  # noqa: BLE001
        return False


def revoke_token(jti: Optional[str], expires_at: Optional[float] = None) -> None:
    """Mark a token's jti as revoked until its natural expiry."""
    if not jti:
        return
    expiry = expires_at or (time.time() + 3600)
    if settings.REDIS_URL and _revoke_in_redis(jti, expiry):
        return
    with _tokens_lock:
        _revoked_tokens[jti] = expiry


def is_token_revoked(jti: Optional[str]) -> bool:
    """Return True if the token jti has been revoked (and not yet expired)."""
    if not jti:
        return False
    if settings.REDIS_URL and _revoked_in_redis(jti):
        return True
    now = time.time()
    with _tokens_lock:
        if jti in _revoked_tokens:
            if _revoked_tokens[jti] < now:
                del _revoked_tokens[jti]
                return False
            return True
        # Opportunistic cleanup of expired entries
        expired = [k for k, v in _revoked_tokens.items() if v < now]
        for k in expired:
            del _revoked_tokens[k]
    return False


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a bcrypt hash.
    """
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )
    except (ValueError, TypeError):
        return False


def get_password_hash(password: str) -> str:
    """
    Hash a password with bcrypt.
    """
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(),
    ).decode("utf-8")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create an access token.
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access",
        "jti": uuid.uuid4().hex,
    })
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """
    Create a refresh token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh",
        "jti": uuid.uuid4().hex,
    })
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    """
    Decode and validate a JWT token.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get current authenticated user from token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    payload = decode_token(token)
    
    if payload is None:
        raise credentials_exception

    # Reject tokens that have been revoked (e.g. after logout)
    if payload.get("jti") and is_token_revoked(payload["jti"]):
        raise credentials_exception

    user_id: str = payload.get("sub")
    token_type: str = payload.get("type")
    
    if user_id is None or token_type != "access":
        raise credentials_exception
    
    # Get user from database
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current active user.
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user


# Optional bearer scheme: does NOT raise when no Authorization header is sent.
_optional_security = HTTPBearer(auto_error=False)


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_optional_security),
    db: AsyncSession = Depends(get_db),
) -> Optional[User]:
    """
    Return the authenticated user, or None for anonymous (guest) requests.

    Used by public/guest endpoints (assessment without login, N.O.U Lite
    guest chat) where authentication is optional rather than required.
    Invalid/expired tokens are treated the same as "no token".
    """
    if credentials is None or not credentials.credentials:
        return None
    try:
        return await get_current_user(credentials, db)
    except HTTPException:
        return None


def require_role(allowed_roles: list):
    """
    Dependency to require specific user roles.
    """
    async def role_checker(
        current_user: User = Depends(get_current_user)
    ) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return role_checker


# Role-based dependencies
require_admin = require_role(["admin"])
require_customer = require_role(["customer", "admin"])
require_applicant = require_role(["applicant", "admin"])
require_developer = require_role(["developer", "admin"])
require_investor = require_role(["investor", "admin"])
require_project_member = require_role(["developer", "admin"])
require_authenticated = require_role(["customer", "applicant", "admin", "developer", "investor"])


async def ensure_customer_profile(db: AsyncSession, user: User):
    """
    Return the Customer profile for a user, creating it on first access.

    Registration auto-creates profiles for new customers, but accounts that
    predate that change have no profile row yet. Lazy-creating here heals
    those accounts so customer-scoped endpoints work for everyone.
    """
    from app.models.customer import Customer

    result = await db.execute(select(Customer).where(Customer.user_id == user.id))
    customer = result.scalar_one_or_none()

    if not customer:
        customer = Customer(user_id=user.id)
        db.add(customer)
        await db.flush()
        await db.refresh(customer)

    return customer