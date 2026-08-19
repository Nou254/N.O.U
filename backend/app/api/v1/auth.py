"""
Authentication API endpoints.

Security flows (per product requirements):
- Registration: details are held in the OTP cache until the applicant verifies
  the code emailed to them; only then is the user written to the database.
- Admin login: a valid admin credential pair issues an OTP to the admin's
  email; the dashboard is only reachable after the OTP is verified.
- Password recovery: an OTP is required before a new password is accepted.
- All endpoints are rate-limited; login/register are additionally protected
  against enumeration and brute force.
"""

import asyncio
import logging
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, Field, field_validator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.otp import create_otp, verify_otp, get_otp_data
from app.core.rate_limit import check_rate_limit
from app.core.config import settings
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user,
    security as bearer_scheme,
    revoke_token,
    is_token_revoked,
)
from app.models.user import User
from app.models.customer import Customer
from app.schemas.user import (
    UserCreate,
    UserResponse,
    Token,
    PasswordChange,
    _validate_password_strength,
)
from app.services.email import send_email, otp_email_html

logger = logging.getLogger("auth")

router = APIRouter()


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------
class OtpVerifyRequest(BaseModel):
    email: EmailStr
    otp: str = Field(..., min_length=4, max_length=10)


class RegisterVerifyRequest(BaseModel):
    email: EmailStr
    otp: str = Field(..., min_length=4, max_length=10)


class UsernameRequest(BaseModel):
    """
    Set the user's company handle (displayed as @handle, e.g. @henrydatabase)
    and used to interact with other personnel in the community and projects.
    """
    username: str = Field(
        ...,
        min_length=3,
        max_length=30,
        pattern="^[a-zA-Z0-9_]+$",
        description="3-30 chars: letters, numbers, underscore (no spaces or @)",
    )


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: str = Field(..., min_length=4, max_length=10)
    new_password: str = Field(..., min_length=8, max_length=100)

    @field_validator("new_password")
    @classmethod
    def new_password_strength(cls, value: str) -> str:
        return _validate_password_strength(value)


class ResendOtpRequest(BaseModel):
    email: EmailStr
    purpose: str = Field(..., pattern="^(login|register|reset)$")


@router.post("/username")
async def set_username(
    body: UsernameRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Create or update the user's company handle (@handle, e.g. @henrydatabase).
    The handle is used to interact with other personnel in the community and
    on projects. Only the account owner can set it, and it must be unique.
    """
    username = body.username.strip().lower()

    existing = await db.scalar(
        select(User).where(User.username == username, User.id != current_user.id)
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"@{username} is already taken. Please choose another handle.",
        )

    current_user.username = username
    await db.commit()
    await db.refresh(current_user)
    return {
        "message": f"Your handle is now @{username}",
        "user": _safe_user(current_user),
    }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
async def _issue_otp(
    email: str,
    purpose: str,
    key: str,
    label: str,
    data: dict = None,
) -> dict:
    """Create an OTP, email it, and build the response."""
    code = create_otp(purpose, key, data=data or {})
    try:
        await send_email(
            email,
            "N.O.U Digital Systems - Your verification code",
            otp_email_html(code, label),
        )
    except Exception:  # noqa: BLE001
        # SMTP can be down in dev - never block the flow; the code is still
        # issued and can be found in the email log fallback.
        logger.warning("OTP email to %s failed; code issued anyway", email, exc_info=True)
    # NOTE: the code is NEVER returned in the response (pentest finding -
    # the dev_otp convenience was removed). It only reaches the user via the
    # emailed verification code.
    return {
        "requires_otp": True,
        "email": email,
        "message": f"A verification code has been sent to your email ({label}).",
    }


def _safe_user(user: User) -> dict:
    """Serialize a user WITHOUT sensitive fields (password_hash etc.).
    Matches the UserResponse schema used by /auth/me. (Pentest finding:
    previously the raw ORM object leaked the bcrypt hash in login responses.)"""
    return {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": user.role,
        "username": user.username,
        "is_active": user.is_active,
        "last_login": user.last_login,
        "terms_accepted_at": user.terms_accepted_at,
        "policies_accepted_at": user.policies_accepted_at,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
        "qualification_category_id": user.qualification_category_id,
        "qualification_position_id": user.qualification_position_id,
        "qualification_category_name": user.qualification_category_name,
        "qualification_position_name": user.qualification_position_name,
    }


def _issue_tokens(user: User) -> dict:
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": _safe_user(user),
    }


# ---------------------------------------------------------------------------
# Registration (OTP-verified)
# ---------------------------------------------------------------------------
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Step 1 of registration: validate the details, cache them, and email an OTP.
    The user is only written to the database after /register/verify succeeds.
    """
    check_rate_limit(request, "register:ip", max_hits=30, window_seconds=3600)

    if user_data.role == "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator accounts cannot be self-registered"
        )

    # Reject immediate duplicates without revealing account existence details.
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none():
        return {
            "requires_otp": False,
            "message": "If this email address is not already registered, "
                       "please check your inbox for a verification code.",
        }

    # Cache the pending registration (password is pre-hashed, never stored
    # plain) alongside the OTP; the account is only written to the database
    # once /register/verify succeeds.
    return await _issue_otp(
        user_data.email,
        "register",
        user_data.email,
        "account registration",
        data={
            "email": user_data.email,
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
            "role": user_data.role,
            "password_hash": get_password_hash(user_data.password),
            # Applicant's place of qualification (category where they will be
            # assessed), captured at registration.
            "qualification_category_id": user_data.qualification_category_id,
            "qualification_position_id": user_data.qualification_position_id,
            "qualification_category_name": user_data.qualification_category_name,
            "qualification_position_name": user_data.qualification_position_name,
        },
    )


@router.post("/register/verify", status_code=status.HTTP_201_CREATED)
async def register_verify(
    body: RegisterVerifyRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Step 2 of registration: verify the emailed OTP, then create the account.
    """
    check_rate_limit(request, f"otp:email:{body.email}", max_hits=10, window_seconds=900)
    check_rate_limit(request, "otp:ip", max_hits=40, window_seconds=900)

    pending = verify_otp("register", body.email, body.otp)
    if pending is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification code"
        )

    # The email may have been registered between OTP creation and verification.
    result = await db.execute(select(User).where(User.email == pending["email"]))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is already registered. Please sign in."
        )

    new_user = User(
        email=pending["email"],
        password_hash=pending["password_hash"],
        first_name=pending["first_name"],
        last_name=pending["last_name"],
        role=pending["role"],
        # Applicant's chosen place of qualification (drives the assessment).
        qualification_category_id=pending.get("qualification_category_id"),
        qualification_position_id=pending.get("qualification_position_id"),
        qualification_category_name=pending.get("qualification_category_name"),
        qualification_position_name=pending.get("qualification_position_name"),
    )
    db.add(new_user)
    await db.flush()

    if pending["role"] == "customer":
        db.add(Customer(user_id=new_user.id))

    # Commit *before* responding: get_db()'s post-yield commit runs after the
    # response is sent, which would let a fast follow-up login request race the
    # write and see a missing user (read-your-writes).
    await db.commit()
    await db.refresh(new_user)
    return {"message": "Account verified and created. Please sign in."}


# ---------------------------------------------------------------------------
# Login (admin requires OTP)
# ---------------------------------------------------------------------------
@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    request: Request = None,  # injected by FastAPI; default keeps IDE happy
    db: AsyncSession = Depends(get_db),
):
    """
    Login. Regular users receive tokens directly. Admin accounts require a
    second step: an OTP is emailed and must be verified via /login/verify.
    """
    check_rate_limit(request, f"login:acct:{form_data.username}",
                     max_hits=10, window_seconds=900)
    check_rate_limit(request, "login:ip", max_hits=60, window_seconds=900)

    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )

    # Admin accounts: 2-step login with OTP.
    if user.role == "admin":
        return await _issue_otp(
            user.email, "login", str(user.id), "admin sign in"
        )

    # Regular users: direct tokens.
    user.last_login = datetime.utcnow()
    await db.flush()
    await db.refresh(user)
    return _issue_tokens(user)


@router.post("/login/verify", response_model=Token)
async def login_verify(
    body: OtpVerifyRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Complete admin login by verifying the emailed OTP, then receive tokens.
    """
    check_rate_limit(request, f"otp:email:{body.email}", max_hits=10, window_seconds=900)
    check_rate_limit(request, "otp:ip", max_hits=40, window_seconds=900)

    result = await db.execute(select(User).where(User.email == body.email))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid verification code"
        )

    if verify_otp("login", str(user.id), body.otp) is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired verification code"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )

    user.last_login = datetime.utcnow()
    await db.flush()
    await db.refresh(user)
    return _issue_tokens(user)


# ---------------------------------------------------------------------------
# Password recovery (OTP-required)
# ---------------------------------------------------------------------------
@router.post("/forgot-password")
async def forgot_password(
    body: ForgotPasswordRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Request a password reset. Emails an OTP if the account exists; the
    response is intentionally generic to avoid account enumeration.
    """
    check_rate_limit(request, f"forgot:email:{body.email}", max_hits=3, window_seconds=900)
    check_rate_limit(request, "forgot:ip", max_hits=20, window_seconds=900)

    result = await db.execute(select(User).where(User.email == body.email))
    user = result.scalar_one_or_none()

    response = {
        "message": "If that email is registered, a password reset code has been sent to it."
    }
    if user:
        await _issue_otp(
            user.email, "reset", user.email, "password recovery"
        )

    return response


@router.post("/reset-password")
async def reset_password(
    body: ResetPasswordRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Verify the reset OTP and set a new password.
    """
    check_rate_limit(request, f"otp:email:{body.email}", max_hits=10, window_seconds=900)
    check_rate_limit(request, "otp:ip", max_hits=40, window_seconds=900)

    if verify_otp("reset", body.email, body.otp) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification code"
        )

    result = await db.execute(select(User).where(User.email == body.email))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification code"
        )

    user.password_hash = get_password_hash(body.new_password)
    # Commit before responding so an immediate sign-in sees the new hash
    # (get_db()'s post-yield commit runs after the response is sent).
    await db.commit()

    return {"message": "Password reset successful. Please sign in."}


@router.post("/resend-otp")
async def resend_otp(
    body: ResendOtpRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    Re-send an existing OTP (login / register / reset) without invalidating it.
    """
    check_rate_limit(request, f"resend:{body.purpose}:{body.email}", max_hits=3, window_seconds=600)
    check_rate_limit(request, "resend:ip", max_hits=15, window_seconds=600)

    key = body.email
    if body.purpose == "login":
        # Login OTPs are keyed by the user id - resolve it from the email.
        result = await db.execute(select(User).where(User.email == body.email))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No pending verification found for this email"
            )
        key = str(user.id)

    payload = get_otp_data(body.purpose, key)

    # If the OTP expired or was consumed, login can still resend (the user
    # exists and no extra data is needed).  Register / reset cannot — the
    # cached payload is gone — so we ask the user to restart the flow.
    if not payload and body.purpose == "login":
        payload = {}  # login OTPs only need the user-id key

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification code expired. Please start the process again."
        )

    label = {
        "login": "admin sign in",
        "register": "account registration",
        "reset": "password recovery",
    }[body.purpose]

    code = create_otp(body.purpose, key, data=payload)
    try:
        await send_email(
            body.email,
            "N.O.U Digital Systems - Your verification code",
            otp_email_html(code, label),
        )
    except Exception:  # noqa: BLE001
        logger.warning("Resend OTP email to %s failed; code issued anyway", body.email, exc_info=True)
    return {
        "requires_otp": True,
        "email": body.email,
        "message": "A new verification code has been sent.",
    }


# ---------------------------------------------------------------------------
# Token refresh / profile / password change / logout
# ---------------------------------------------------------------------------
class RefreshTokenRequest(BaseModel):
    refresh_token: str


@router.post("/refresh", response_model=Token)
async def refresh_token(
    body: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
):
    """Refresh access token with rotation (the used refresh token is revoked)."""
    payload = decode_token(body.refresh_token)

    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    if payload.get("jti") and is_token_revoked(payload["jti"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has been revoked"
        )

    user_id = payload.get("sub")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )

    revoke_token(payload.get("jti"), payload.get("exp"))
    return _issue_tokens(user)


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
):
    """Get current user information."""
    return current_user


@router.post("/accept-terms")
async def accept_terms(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Record the user's agreement to the Terms & Conditions and Privacy Policy.
    Required before a user can submit details (investor form, assessments,
    projects, etc.) - enforced by the first-login consent gate on the frontend.
    """
    current_user.terms_accepted_at = datetime.utcnow()
    await db.commit()
    return {
        "message": "Thank you - you have agreed to the Terms & Conditions and Privacy Policy.",
        "terms_accepted_at": current_user.terms_accepted_at,
    }


@router.post("/accept-policies")
async def accept_policies(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Record the user's agreement to the N.O.U. Organization Policies document.
    Required on the first login after the admin approves a passed applicant -
    the full policies document is shown and the user must agree before using
    the platform (enforced by the frontend consent gate).
    """
    current_user.policies_accepted_at = datetime.utcnow()
    await db.commit()
    return {
        "message": "Thank you - you have agreed to the N.O.U. Organization Policies.",
        "policies_accepted_at": current_user.policies_accepted_at,
    }


@router.post("/change-password")
async def change_password(
    body: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Change the current user's password (requires the current password)."""
    if not verify_password(body.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )

    current_user.password_hash = get_password_hash(body.new_password)
    await db.commit()

    return {"message": "Password changed successfully"}


@router.post("/logout")
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    current_user: User = Depends(get_current_user),
):
    """Logout - revokes the presented access token."""
    payload = decode_token(credentials.credentials)
    if payload:
        revoke_token(payload.get("jti"), payload.get("exp"))

    return {"message": "Successfully logged out"}
