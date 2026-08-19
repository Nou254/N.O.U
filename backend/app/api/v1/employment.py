"""
Employment API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File, Form, Request
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Union
from datetime import datetime
import os
import uuid

from app.core.database import get_db
from app.core.rate_limit import check_rate_limit
from app.core.security import get_current_user, require_admin, require_applicant, get_password_hash
from app.core.config import settings
from app.models.user import User
from app.models.job import JobListing
from app.models.application import Application
from app.services.email import send_email, applicant_credentials_email_html
from app.services.onboarding import generate_temporary_password

router = APIRouter()


@router.get("/jobs")
async def list_jobs(
    department: Optional[str] = None,
    status: Optional[str] = "active",
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    List available job listings.
    """
    query = select(JobListing)
    
    if department:
        query = query.where(JobListing.department == department)
    
    if status:
        query = query.where(JobListing.status == status)
    
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query)
    
    # Apply pagination
    query = query.offset((page - 1) * limit).limit(limit)
    result = await db.execute(query)
    jobs = result.scalars().all()
    
    return {
        "jobs": jobs,
        "pagination": {
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (total + limit - 1) // limit
        }
    }


@router.get("/jobs/{job_id}")
async def get_job(
    job_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get job listing details.
    """
    result = await db.execute(
        select(JobListing).where(JobListing.id == job_id)
    )
    job = result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job listing not found"
        )
    
    return job


class PublicApplicationIn(BaseModel):
    """Guest job application - no account required. The applicant provides
    their official names, email, phone number, optional CV and their chosen
    place of qualification (category + position); assessment results are
    emailed to them."""
    full_name: str = Field(min_length=3, max_length=200)
    email: EmailStr
    job_id: Union[int, str]
    cover_letter: Optional[str] = Field(None, max_length=5000)
    phone: Optional[str] = Field(None, max_length=30)
    # Place of qualification - the professional category (and optional
    # position) the applicant will be assessed in.
    category_id: Optional[int] = None
    position_id: Optional[int] = None
    category_name: Optional[str] = Field(None, max_length=120)
    position_name: Optional[str] = Field(None, max_length=120)


async def _save_cv(cv_file: UploadFile) -> Optional[str]:
    """Validate and store an uploaded CV; returns the stored file path."""
    if cv_file is None or not getattr(cv_file, "filename", None):
        return None
    if cv_file.content_type not in settings.ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="File type not allowed. Please upload a PDF, Word document or plain text file.",
        )
    contents = await cv_file.read()
    if len(contents) > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds the maximum allowed size of {settings.MAX_FILE_SIZE // (1024 * 1024)}MB",
        )
    # Whitelist the stored extension (independent of the reported content
    # type) so a file is never saved with a dangerous extension.
    ext = os.path.splitext(cv_file.filename or "")[1].lower()
    if ext not in {".pdf", ".doc", ".docx", ".txt"}:
        ext = ".pdf"
    stored_name = f"{uuid.uuid4()}{ext}"
    cv_path = os.path.join(settings.UPLOAD_DIR, "cvs", stored_name)
    os.makedirs(os.path.dirname(cv_path), exist_ok=True)
    with open(cv_path, "wb") as f:
        f.write(contents)
    return cv_path


async def _read_application_request(
    request: Request,
) -> tuple[PublicApplicationIn, Optional[UploadFile]]:
    """Accept the application as JSON or multipart form data (JSON keeps the
    original API contract; multipart additionally carries the CV file)."""
    content_type = request.headers.get("content-type", "")
    if "multipart/form-data" in content_type:
        form = await request.form()
        values: dict = {}
        for field in (
            "full_name", "email", "job_id", "cover_letter", "phone",
            "category_id", "position_id", "category_name", "position_name",
        ):
            v = form.get(field)
            if v is not None:
                values[field] = v if isinstance(v, str) else str(v)
        body = PublicApplicationIn(**values)
        cv_file = form.get("cv_file")
        if cv_file is not None and not hasattr(cv_file, "read"):
            cv_file = None
        return body, cv_file
    raw = await request.body()
    if not raw:
        raise HTTPException(status_code=422, detail="Request body is required")
    body = PublicApplicationIn.model_validate_json(raw)
    return body, None


@router.post("/applications/public-apply", status_code=status.HTTP_201_CREATED)
async def public_apply(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Apply for a job WITHOUT registering or creating an account.

    The applicant enters their official names, email, phone number and an
    optional CV. An applicant record is created on the fly with temporary
    credentials (emailed to them so they can sign in and take the
    assessment); their results are emailed to the address they provided.
    """
    body, cv_file = await _read_application_request(request)
    check_rate_limit(request, "public-apply:ip", max_hits=15, window_seconds=3600)
    check_rate_limit(request, f"public-apply:email:{body.email}", max_hits=5, window_seconds=3600)

    job = await db.scalar(
        select(JobListing).where(
            JobListing.id == body.job_id, JobListing.status == "active"
        )
    )
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job listing not found or not active",
        )

    parts = body.full_name.strip().split(None, 1)
    first_name = parts[0] if parts else body.email.split("@")[0]
    last_name = parts[1] if len(parts) > 1 else ""

    user = await db.scalar(select(User).where(User.email == body.email))
    created = False
    temp_password = None
    if not user:
        temp_password = generate_temporary_password()
        user = User(
            email=body.email,
            password_hash=get_password_hash(temp_password),
            first_name=first_name,
            last_name=last_name,
            role="applicant",
            is_active=True,
            phone=body.phone,
            # Applying constitutes agreement to the terms.
            terms_accepted_at=datetime.now(),
        )
        db.add(user)
        await db.flush()
        created = True
    elif user.role != "applicant":
        # Keep the assessment portal reachable for this email address.
        user.role = "applicant"
        db.add(user)

    # Always refresh the applicant's contact details so the latest phone
    # number and name stay on file for the admin/HR screens.
    if body.phone:
        user.phone = body.phone
    if body.full_name:
        user.first_name = first_name or user.first_name
        user.last_name = last_name or user.last_name

    # Save the applicant's chosen place of qualification - this is where
    # they are assessed (today.md: "where they choose is where they are
    # assessed").
    if body.category_id or body.category_name:
        user.qualification_category_id = body.category_id
        user.qualification_position_id = body.position_id
        user.qualification_category_name = body.category_name
        user.qualification_position_name = body.position_name

    existing = await db.scalar(
        select(Application).where(
            Application.applicant_id == user.id,
            Application.job_id == job.id,
        )
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already applied for this position",
        )

    cv_path = await _save_cv(cv_file) if cv_file is not None else None
    application = Application(
        applicant_id=user.id,
        job_id=job.id,
        cover_letter=body.cover_letter,
        phone=body.phone,
        cv_file_path=cv_path,
    )
    db.add(application)
    # Also capture the qualification choice on the application record itself.
    application.category_id = body.category_id
    application.position_id = body.position_id
    application.category_name = body.category_name
    application.position_name = body.position_name
    # Keep the CV path on the user too, so the admin/HR screens can see it
    # even before a formal application row exists (assessment-page guests).
    if cv_path:
        user.cv_file_path = cv_path
    # Commit before responding (read-your-writes).
    await db.commit()
    await db.refresh(application)

    if created:
        name = f"{user.first_name} {user.last_name}".strip() or "there"
        await send_email(
            user.email,
            "N.O.U Digital Systems - Your application is received",
            applicant_credentials_email_html(
                applicant_name=name,
                job_title=job.title,
                login_email=user.email,
                temp_password=temp_password,
            ),
        )

    payload = {
        "message": (
            "Application received. You are now taken straight into your "
            "assessment - your results will be emailed to you afterwards."
        ),
        "application": {
            "id": application.id,
            "job_id": application.job_id,
            "status": application.status,
        },
        "applicant": {"email": user.email, "role": user.role},
    }
    # Dev convenience: surface the temp password locally so the chain can be
    # tested end-to-end (the email is the real channel in production).
    if created and settings.ENVIRONMENT.lower() == "development":
        payload["applicant"]["temp_password"] = temp_password
    return payload


@router.post("/applications/attach-cv")
async def attach_cv(
    request: Request,
    email: str = Form(...),
    cv_file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    """Attach a CV to an applicant by email - used by guests who start the
    assessment straight from the /assessment page (no Careers apply step).
    The applicant record is created by the assessment start flow."""
    check_rate_limit(request, "attach-cv:ip", max_hits=20, window_seconds=3600)
    normalized = email.strip().lower()
    user = await db.scalar(select(User).where(User.email == normalized))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No applicant found for this email yet. Apply via Careers or start the assessment first.",
        )
    cv_path = await _save_cv(cv_file)
    user.cv_file_path = cv_path
    # Mirror the CV onto their latest application row if one exists.
    latest = await db.scalar(
        select(Application)
        .where(Application.applicant_id == user.id)
        .order_by(Application.submitted_at.desc())
        .limit(1)
    )
    if latest:
        latest.cv_file_path = cv_path
    await db.commit()
    return {"message": "CV uploaded successfully", "cv_file_path": cv_path}


@router.post("/applications", status_code=status.HTTP_201_CREATED)
async def submit_application(
    job_id: str,
    cover_letter: Optional[str] = None,
    cv_file: Optional[UploadFile] = File(None),
    current_user: User = Depends(require_applicant),
    db: AsyncSession = Depends(get_db)
):
    """
    Submit a job application.
    """
    # Check if job exists
    job_result = await db.execute(
        select(JobListing).where(JobListing.id == job_id, JobListing.status == "active")
    )
    job = job_result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job listing not found or not active"
        )
    
    # Check if already applied
    existing_application = await db.execute(
        select(Application).where(
            Application.applicant_id == current_user.id,
            Application.job_id == job_id
        )
    )
    if existing_application.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already applied for this position"
        )
    
    # Handle CV file upload
    cv_file_path = None
    if cv_file:
        # Validate file type against the configured allow-list (M2)
        if cv_file.content_type not in settings.ALLOWED_FILE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=f"File type '{cv_file.content_type}' is not allowed"
            )

        # Validate file size
        contents = await cv_file.read()
        file_size = len(contents)
        
        if file_size > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size exceeds maximum allowed size of {settings.MAX_FILE_SIZE / (1024 * 1024)}MB"
            )
        
        # Save file
        file_ext = os.path.splitext(cv_file.filename)[1]
        stored_name = f"{uuid.uuid4()}{file_ext}"
        cv_file_path = os.path.join(settings.UPLOAD_DIR, "cvs", stored_name)
        
        os.makedirs(os.path.dirname(cv_file_path), exist_ok=True)
        
        with open(cv_file_path, "wb") as f:
            f.write(contents)
    
    # Create application
    new_application = Application(
        applicant_id=current_user.id,
        job_id=job_id,
        cover_letter=cover_letter,
        cv_file_path=cv_file_path
    )
    
    db.add(new_application)
    await db.flush()
    await db.refresh(new_application)
    
    return new_application


@router.get("/applications/me")
async def get_my_applications(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(require_applicant),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current user's applications.
    """
    query = (
        select(Application)
        .options(selectinload(Application.job))
        .where(Application.applicant_id == current_user.id)
    )

    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query)

    query = query.order_by(Application.submitted_at.desc())
    query = query.offset((page - 1) * limit).limit(limit)

    result = await db.execute(query)
    applications = result.scalars().all()

    return {
        "applications": applications,
        "pagination": {
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (total + limit - 1) // limit
        }
    }


@router.get("/applications/{application_id}")
async def get_application(
    application_id: str,
    current_user: User = Depends(require_applicant),
    db: AsyncSession = Depends(get_db)
):
    """
    Get application details.
    """
    result = await db.execute(
        select(Application)
        .options(selectinload(Application.job))
        .where(
            Application.id == application_id,
            Application.applicant_id == current_user.id
        )
    )
    application = result.scalar_one_or_none()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    return application