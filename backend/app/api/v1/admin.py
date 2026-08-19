"""
Admin API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, text as sa_text
from sqlalchemy.orm import selectinload
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date, timedelta
import json
import os
import sys
import uuid

from app.core.database import get_db
from app.core.security import require_admin
from app.core.config import settings
from app.models.user import User
from app.models.product import Product, ProductVersion
from app.models.job import JobListing
from app.models.assessment import Assessment, AssessmentSession
from app.models.support import SupportTicket
from app.models.complaint import Complaint
from app.models.application import Application
from app.models.investor import InvestorInterest
from app.models.company_project import (
    CompanyProject, ProjectMember, ProjectDocument, ExtraDeveloperRequest,
)
from app.models.project_release import ProjectRelease
from app.models.project_progress import ProjectDeadlineExtension
from app.models.nou_lite_order import NouliteOrder
from app.models.project_request import ProjectRequest, ProjectPayment
from app.models.customer import Customer
from app.models.personnel import PersonnelCategory, PersonnelPosition
from app.models.question_bank import QuestionBankQuestion
from app.models.visit_log import SiteVisit
from app.models.mobile_app import MobileApp, AppComment
from app.models.ai_key_usage import AIKeyUsage
from app.core.assessment_framework import (
    PARTS, PART_QUESTION_TYPES, BANK_QUESTIONS_PER_PART,
)
from app.services import ai_assessment
from app.services.question_bank import ensure_bank, bank_counts
from app.services.cv_extract import extract_cv_text
from app.services.assessment_results import build_session_feedback
from app.services.onboarding import approve_applicant, list_passed_candidates, generate_temporary_password
from app.services.email import send_email, recruitment_email_html
from app.core.security import get_password_hash

router = APIRouter()

# Server start time - captured when the API process boots, used for the
# uptime report on the admin dashboard.
_SERVER_STARTED_AT = datetime.utcnow()


# Dashboard statistics
@router.get("/dashboard/stats")
async def get_dashboard_stats(
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Get dashboard statistics.
    """
    # Get counts
    users_count = await db.scalar(select(func.count()).select_from(User))
    products_count = await db.scalar(select(func.count()).select_from(Product).where(Product.is_active == True))
    jobs_count = await db.scalar(select(func.count()).select_from(JobListing).where(JobListing.status == "active"))
    applications_count = await db.scalar(select(func.count()).select_from(Application))
    tickets_count = await db.scalar(select(func.count()).select_from(SupportTicket).where(SupportTicket.status == "open"))
    assessments_count = await db.scalar(select(func.count()).select_from(Assessment).where(Assessment.is_active == True))
    investors_count = await db.scalar(select(func.count()).select_from(InvestorInterest))
    projects_count = await db.scalar(select(func.count()).select_from(CompanyProject))
    nou_lite_orders_count = await db.scalar(select(func.count()).select_from(NouliteOrder))
    onboarding_pending = await db.scalar(
        select(func.count())
        .select_from(AssessmentSession)
        .where(
            AssessmentSession.status == "completed",
            AssessmentSession.ai_recommendation == "PASS",
            AssessmentSession.onboarding_status == "pending",
        )
    )

    # ---- Payments summary (today.md docs 8 + 9; excludes support donations) ----
    payments_collected = await db.scalar(
        select(func.coalesce(func.sum(ProjectPayment.amount), 0)).where(
            ProjectPayment.status == "successful",
            ProjectPayment.payment_type != "support",
        )
    )
    payments_pending = await db.scalar(
        select(func.coalesce(func.sum(ProjectPayment.amount), 0)).where(
            ProjectPayment.status.in_(["pending", "processing"]),
            ProjectPayment.payment_type != "support",
        )
    )
    payments_pending_count = await db.scalar(
        select(func.count()).select_from(ProjectPayment).where(
            ProjectPayment.status.in_(["pending", "processing"]),
            ProjectPayment.payment_type != "support",
        )
    )
    payments_successful_count = await db.scalar(
        select(func.count()).select_from(ProjectPayment).where(
            ProjectPayment.status == "successful",
            ProjectPayment.payment_type != "support",
        )
    )
    project_requests_total = await db.scalar(
        select(func.count()).select_from(ProjectRequest)
    )
    requests_awaiting_deposit = await db.scalar(
        select(func.count()).select_from(ProjectRequest).where(
            ProjectRequest.status == "awaiting_deposit"
        )
    )
    requests_quotation_issued = await db.scalar(
        select(func.count()).select_from(ProjectRequest).where(
            ProjectRequest.status == "quotation_issued"
        )
    )

    # ---- Support contributions (separate from project payments) ----
    support_collected = await db.scalar(
        select(func.coalesce(func.sum(ProjectPayment.amount), 0)).where(
            ProjectPayment.payment_type == "support",
            ProjectPayment.status == "successful",
        )
    )
    support_pending = await db.scalar(
        select(func.coalesce(func.sum(ProjectPayment.amount), 0)).where(
            ProjectPayment.payment_type == "support",
            ProjectPayment.status.in_(["pending", "processing"]),
        )
    )
    support_count = await db.scalar(
        select(func.count()).select_from(ProjectPayment).where(
            ProjectPayment.payment_type == "support"
        )
    )

    return {
        "users": users_count,
        "products": products_count,
        "jobs": jobs_count,
        "applications": applications_count,
        "open_tickets": tickets_count,
        "assessments": assessments_count,
        "investor_interests": investors_count,
        "projects": projects_count,
        "nou_lite_orders": nou_lite_orders_count,
        "onboarding_pending": onboarding_pending,
        # Payments summary (project payments only - support is separate)
        "payments_collected": float(payments_collected or 0),
        "payments_pending": float(payments_pending or 0),
        "payments_pending_count": payments_pending_count,
        "payments_successful_count": payments_successful_count,
        "project_requests": project_requests_total,
        "requests_awaiting_deposit": requests_awaiting_deposit,
        "requests_quotation_issued": requests_quotation_issued,
        # Support contributions (footer donations)
        "support_collected": float(support_collected or 0),
        "support_pending": float(support_pending or 0),
        "support_count": support_count,
    }


# Product management
@router.post("/products", status_code=status.HTTP_201_CREATED)
async def create_product(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    category: str = Form("software"),
    version: str = Form("1.0.0"),
    status: str = Form("Available"),
    platforms: Optional[str] = Form("Web"),
    licence: Optional[str] = Form(None),
    requirements: Optional[str] = Form(None),
    features: Optional[str] = Form(None),
    featured: bool = Form(False),
    file: Optional[UploadFile] = File(None),
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new product (catalogue fields per today.md Ch.5).
    """
    # Handle file upload
    file_path = None
    file_size = None
    
    if file:
        # Validate file type against the configured allow-list (M2)
        if file.content_type not in settings.ALLOWED_FILE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=f"File type '{file.content_type}' is not allowed"
            )

        # Validate file size
        contents = await file.read()
        file_size = len(contents)
        
        if file_size > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size exceeds maximum allowed size of {settings.MAX_FILE_SIZE / (1024 * 1024)}MB"
            )
        
        # Save file
        file_ext = os.path.splitext(file.filename)[1]
        stored_name = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(settings.UPLOAD_DIR, "products", stored_name)
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "wb") as f:
            f.write(contents)
    
    # Create product
    new_product = Product(
        name=name,
        description=description,
        category=category,
        version=version,
        status=status,
        platforms=platforms,
        licence=licence,
        requirements=requirements,
        features=features,
        featured=featured,
        file_path=file_path,
        file_size=file_size
    )
    
    db.add(new_product)
    await db.flush()
    await db.refresh(new_product)
    
    return {"message": "Product created", "product": {
        "id": new_product.id, "name": new_product.name,
        "category": new_product.category, "status": new_product.status,
        "platforms": (new_product.platforms or "").split(","),
        "featured": bool(new_product.featured),
    }}


@router.put("/products/{product_id}")
async def update_product(
    product_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    category: Optional[str] = None,
    version: Optional[str] = None,
    status: Optional[str] = None,
    platforms: Optional[str] = None,
    licence: Optional[str] = None,
    requirements: Optional[str] = None,
    features: Optional[str] = None,
    featured: Optional[bool] = None,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Update product information (incl. catalogue fields per today.md Ch.5).
    """
    result = await db.execute(
        select(Product).where(Product.id == product_id, Product.is_active == True)
    )
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Update fields
    if name is not None:
        product.name = name
    if description is not None:
        product.description = description
    if category is not None:
        product.category = category
    if version is not None:
        product.version = version
    if status is not None:
        product.status = status
    if platforms is not None:
        product.platforms = platforms
    if licence is not None:
        product.licence = licence
    if requirements is not None:
        product.requirements = requirements
    if features is not None:
        product.features = features
    if featured is not None:
        product.featured = featured
    
    await db.flush()
    await db.refresh(product)
    
    return {"message": "Product updated", "product": {
        "id": product.id, "name": product.name,
        "category": product.category, "status": product.status,
        "platforms": (product.platforms or "").split(","),
        "featured": bool(product.featured),
    }}


@router.delete("/products/{product_id}")
async def delete_product(
    product_id: str,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Soft delete a product.
    """
    result = await db.execute(
        select(Product).where(Product.id == product_id, Product.is_active == True)
    )
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Soft delete
    product.is_active = False
    await db.flush()
    
    return {"message": "Product deleted successfully"}


# Job management
@router.post("/jobs", status_code=status.HTTP_201_CREATED)
async def create_job(
    title: str,
    description: str,
    department: Optional[str] = None,
    location: Optional[str] = None,
    employment_type: Optional[str] = "full_time",
    requirements: Optional[str] = None,
    salary_range: Optional[str] = None,
    deadline: Optional[datetime] = None,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new job listing.
    """
    new_job = JobListing(
        title=title,
        description=description,
        department=department,
        location=location,
        employment_type=employment_type,
        requirements=requirements,
        salary_range=salary_range,
        deadline=deadline
    )
    
    db.add(new_job)
    await db.flush()
    await db.refresh(new_job)
    
    return new_job


@router.put("/jobs/{job_id}")
async def update_job(
    job_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    status: Optional[str] = None,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Update job listing.
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
    
    # Update fields
    if title is not None:
        job.title = title
    if description is not None:
        job.description = description
    if status is not None:
        job.status = status
    
    await db.flush()
    await db.refresh(job)
    
    return job


# User management
@router.get("/users")
async def list_users(
    role: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    List all users.
    """
    query = select(User)
    
    if role:
        query = query.where(User.role == role)
    
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query)
    
    # Apply pagination
    query = query.offset((page - 1) * limit).limit(limit)
    result = await db.execute(query)
    users = result.scalars().all()

    # Never expose password hashes (matches the login/_safe_user contract).
    from app.api.v1.auth import _safe_user
    return {
        "users": [_safe_user(u) for u in users],
        "pagination": {
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (total + limit - 1) // limit
        }
    }


class UserStatusUpdate(BaseModel):
    is_active: bool


@router.put("/users/{user_id}/status")
async def update_user_status(
    user_id: str,
    body: UserStatusUpdate,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Update user status (activate/deactivate).
    """
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_active = body.is_active
    await db.flush()
    
    return {"message": f"User {'activated' if body.is_active else 'deactivated'} successfully"}


# Support ticket management
@router.get("/tickets")
async def list_all_tickets(
    status_filter: Optional[str] = None,
    priority: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    List all support tickets.
    """
    query = select(SupportTicket)
    
    if status_filter:
        query = query.where(SupportTicket.status == status_filter)
    
    if priority:
        query = query.where(SupportTicket.priority == priority)
    
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query)
    
    # Apply pagination and ordering
    query = query.order_by(SupportTicket.created_at.desc())
    query = query.offset((page - 1) * limit).limit(limit)
    
    result = await db.execute(query)
    tickets = result.scalars().all()
    
    return {
        "tickets": tickets,
        "pagination": {
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (total + limit - 1) // limit
        }
    }


@router.put("/tickets/{ticket_id}/assign")
async def assign_ticket(
    ticket_id: str,
    assigned_to: str,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Assign a support ticket to an admin.
    """
    result = await db.execute(
        select(SupportTicket).where(SupportTicket.id == ticket_id)
    )
    ticket = result.scalar_one_or_none()
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Support ticket not found"
        )
    
    # Verify assignee exists and is admin
    assignee_result = await db.execute(
        select(User).where(User.id == assigned_to, User.role == "admin")
    )
    assignee = assignee_result.scalar_one_or_none()
    
    if not assignee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignee not found or not an admin"
        )
    
    ticket.assigned_to = assigned_to
    ticket.status = "in_progress"
    ticket.updated_at = datetime.utcnow()
    
    await db.flush()
    
    return {"message": "Ticket assigned successfully"}


class AssessmentCreate(BaseModel):
    title: str
    description: Optional[str] = None
    durationMinutes: int = 60
    totalQuestions: int = 50
    passingScore: int = 60


@router.post("/assessments", status_code=status.HTTP_201_CREATED)
async def create_assessment(
    assessment: AssessmentCreate,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new assessment (Admin only).
    """
    new_assessment = Assessment(
        title=assessment.title,
        description=assessment.description,
        duration_minutes=assessment.durationMinutes,
        total_questions=assessment.totalQuestions,
        passing_score=assessment.passingScore
    )

    db.add(new_assessment)
    await db.flush()
    await db.refresh(new_assessment)

    return new_assessment


# AI assessment results (admin review of Groq-graded candidates)
@router.get("/assessment-results")
async def list_assessment_results(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    List completed AI-graded assessment sessions with candidate info,
    score, and the AI verdict, newest first.
    """
    joined = (
        select(AssessmentSession, User, Assessment)
        .join(User, User.id == AssessmentSession.applicant_id)
        .join(Assessment, Assessment.id == AssessmentSession.assessment_id)
        .where(AssessmentSession.status == "completed")
    )
    total = await db.scalar(select(func.count()).select_from(joined.subquery()))

    result = await db.execute(
        joined
        .order_by(AssessmentSession.completed_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
    )
    rows = result.all()

    results = []
    for session, applicant, assessment in rows:
        applicant_name = f"{applicant.first_name} {applicant.last_name}".strip()
        results.append({
            "session_id": session.id,
            "applicant": {
                "id": session.applicant_id,
                "name": applicant_name or (applicant.email if applicant else "Unknown"),
                "email": applicant.email if applicant else None,
            },
            "assessment": {
                "id": session.assessment_id,
                "title": assessment.title if assessment else "Assessment",
            },
            "score": session.score,
            "percentage": session.percentage,
            "recommendation": session.ai_recommendation,
            "summary": session.ai_summary,
            "completed_at": session.completed_at,
            "onboarding_status": session.onboarding_status,
            "onboarding_decided_at": session.onboarding_decided_at,
            "category_name": session.category_name,
            "position_name": session.position_name,
            "competency_band": session.competency_band,
            "recommended_category": session.recommended_category,
            "phone": applicant.phone if applicant else None,
            "cv_file_path": applicant.cv_file_path if applicant else None,
            "cv_reviewed": bool(applicant.cv_summary) if applicant else False,
        })

    return {
        "results": results,
        "pagination": {
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (total + limit - 1) // limit if total else 0,
        },
    }


@router.get("/assessment-results/{session_id}")
async def get_assessment_result_detail(
    session_id: str,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Get one AI-graded assessment session with per-question feedback.
    """
    session = await db.scalar(
        select(AssessmentSession).where(AssessmentSession.id == session_id)
    )
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment session not found",
        )

    feedback = await build_session_feedback(db, session_id)

    applicant = await db.scalar(
        select(User).where(User.id == session.applicant_id)
    )
    assessment = await db.scalar(
        select(Assessment).where(Assessment.id == session.assessment_id)
    )
    applicant_name = ""
    if applicant:
        applicant_name = f"{applicant.first_name} {applicant.last_name}".strip()

    import json as _json
    try:
        part_scores = _json.loads(session.part_scores) if session.part_scores else {}
    except (TypeError, ValueError):
        part_scores = {}

    cv_summary = {}
    if applicant and applicant.cv_summary:
        try:
            cv_summary = _json.loads(applicant.cv_summary)
        except (TypeError, ValueError):
            cv_summary = {}

    return {
        "session": {
            "id": session.id,
            "score": session.score,
            "percentage": session.percentage,
            "status": session.status,
            "completed_at": session.completed_at,
            "ai_summary": session.ai_summary,
            "ai_recommendation": session.ai_recommendation,
            "category_name": session.category_name,
            "position_name": session.position_name,
            "part_scores": part_scores,
            "competency_band": session.competency_band,
            "recommended_category": session.recommended_category,
        },
        "applicant": {
            "id": session.applicant_id,
            "name": applicant_name or (applicant.email if applicant else "Unknown"),
            "email": applicant.email if applicant else None,
            "phone": applicant.phone if applicant else None,
            "cv_file_path": applicant.cv_file_path if applicant else None,
            "cv_summary": cv_summary,
        },
        "assessment": {
            "id": session.assessment_id,
            "title": assessment.title if assessment else "Assessment",
        },
        "feedback": feedback,
    }


# ---------------------------------------------------------------------------
# Investor funding-interest management
# ---------------------------------------------------------------------------
class InvestorStatusUpdate(BaseModel):
    status: str


def _investor_payload(i: InvestorInterest) -> dict:
    """Serialize an investor interest WITHOUT the (removed) joining-fee
    fields - the joining fee requirement was dropped from the investor
    portal, so it is no longer exposed anywhere in the API."""
    return {
        "id": i.id,
        "full_name": i.full_name,
        "email": i.email,
        "phone": i.phone,
        "country": i.country,
        "organization": i.organization,
        "investment_amount": float(i.investment_amount) if i.investment_amount is not None else None,
        "investment_range": i.investment_range,
        "monthly_investment": float(i.monthly_investment) if i.monthly_investment is not None else None,
        "expectations": i.expectations,
        "risk_knowledge": i.risk_knowledge,
        "message": i.message,
        "status": i.status,
        "admin_notes": i.admin_notes,
        "created_at": i.created_at,
        "updated_at": i.updated_at,
    }


@router.get("/investors")
async def list_investor_interests(
    status_filter: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    List investor funding-interest submissions, newest first.
    """
    query = select(InvestorInterest)

    if status_filter:
        query = query.where(InvestorInterest.status == status_filter)

    count_query = select(func.count()).select_from(query.subquery())
    total = await db.scalar(count_query)

    query = query.order_by(InvestorInterest.created_at.desc())
    query = query.offset((page - 1) * limit).limit(limit)

    result = await db.execute(query)
    interests = result.scalars().all()

    return {
        "interests": [_investor_payload(i) for i in interests],
        "pagination": {
            "total": total,
            "page": page,
            "limit": limit,
            "pages": (total + limit - 1) // limit
        }
    }


@router.get("/investors/{interest_id}")
async def get_investor_interest(
    interest_id: str,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Get one investor interest submission.
    """
    result = await db.execute(
        select(InvestorInterest).where(InvestorInterest.id == interest_id)
    )
    interest = result.scalar_one_or_none()

    if not interest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investor interest not found"
        )

    return _investor_payload(interest)


@router.put("/investors/{interest_id}/status")
async def update_investor_status(
    interest_id: str,
    body: InvestorStatusUpdate,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """
    Update an investor interest status (new / contacted / declined / closed).
    """
    result = await db.execute(
        select(InvestorInterest).where(InvestorInterest.id == interest_id)
    )
    interest = result.scalar_one_or_none()

    if not interest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investor interest not found"
        )

    if body.status not in {"new", "contacted", "declined", "closed"}:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Status must be one of: new, contacted, declined, closed"
        )

    interest.status = body.status
    await db.flush()
    await db.refresh(interest)

    return _investor_payload(interest)


# ---------------------------------------------------------------------------
# Developer onboarding (approve passed applicants)
# ---------------------------------------------------------------------------
@router.get("/onboarding/candidates")
async def onboarding_candidates(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """List applicants who passed the assessment threshold, awaiting approval."""
    return await list_passed_candidates(db, page=page, limit=limit)


# ---------------------------------------------------------------------------
# Direct recruitment (admin recruits a developer without an assessment)
# ---------------------------------------------------------------------------
class RecruitDeveloperIn(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=3, max_length=255)
    # Place of qualification: the professional category (and optional
    # position) the developer is recruited into.
    category_id: int = Field(..., ge=1)
    position_id: Optional[int] = None
    category_name: Optional[str] = Field(None, max_length=120)
    position_name: Optional[str] = Field(None, max_length=120)
    notes: Optional[str] = None


@router.post("/recruit", status_code=status.HTTP_201_CREATED)
async def recruit_developer(
    body: RecruitDeveloperIn,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """
    Admin-only: recruit a developer directly. The applicant details and an
    official email are supplied by the admin; login credentials are generated
    and emailed to them. The recruited developer gets full developer access
    (projects portal + community) WITHOUT taking an assessment.
    """
    email = body.email.strip().lower()
    existing = await db.scalar(select(User).where(User.email == email))
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists. Use the Onboarding page for passed applicants.",
        )

    # Verify the qualification category exists and is active.
    from app.models.personnel import PersonnelCategory
    category = await db.scalar(
        select(PersonnelCategory).where(PersonnelCategory.id == body.category_id)
    )
    if not category or category.is_active != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please choose a valid professional category",
        )

    temp_password = generate_temporary_password()
    new_user = User(
        email=email,
        password_hash=get_password_hash(temp_password),
        first_name=body.first_name.strip(),
        last_name=body.last_name.strip(),
        role="developer",
        is_active=True,
        # Recruiting constitutes agreement to the terms.
        terms_accepted_at=datetime.now(),
        # Place of qualification - recorded for the talent pool.
        qualification_category_id=category.id,
        qualification_position_id=body.position_id,
        qualification_category_name=category.name,
        qualification_position_name=body.position_name,
    )
    db.add(new_user)
    await db.flush()

    # Email the login credentials (non-blocking SMTP with dev-log fallback).
    name = f"{new_user.first_name} {new_user.last_name}".strip() or "there"
    role_title = body.position_name or category.name
    await send_email(
        new_user.email,
        "N.O.U Digital Systems - You're recruited! Your developer login",
        recruitment_email_html(
            applicant_name=name,
            role_title=role_title,
            login_email=new_user.email,
            temp_password=temp_password,
        ),
    )

    # Commit before responding (read-your-writes).
    await db.commit()
    await db.refresh(new_user)

    payload = {
        "message": f"{name} recruited as {role_title}. Login credentials emailed to {new_user.email}.",
        "developer": {
            "id": new_user.id,
            "email": new_user.email,
            "name": name,
            "role": new_user.role,
            "qualification_category": category.name,
            "qualification_position": body.position_name,
        },
    }
    # Dev convenience: surface the generated password locally so the chain can
    # be tested end-to-end (the email is the real channel in production).
    if settings.ENVIRONMENT.lower() == "development":
        payload["developer"]["temp_password"] = temp_password
    return payload


@router.get("/recruited")
async def list_recruited_developers(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """List developers who were directly recruited by administration."""
    query = select(User).where(User.role == "developer")
    total = await db.scalar(select(func.count()).select_from(query.subquery()))
    result = await db.execute(
        query.order_by(User.created_at.desc())
        .offset((page - 1) * limit).limit(limit)
    )
    from app.api.v1.auth import _safe_user
    developers = []
    for u in result.scalars().all():
        data = _safe_user(u)
        data["name"] = f"{u.first_name} {u.last_name}".strip()
        developers.append(data)
    return {
        "developers": developers,
        "pagination": {"total": total, "page": page, "limit": limit,
                       "pages": (total + limit - 1) // limit if total else 0},
    }


class OnboardingDecision(BaseModel):
    approve: bool = True
    notes: Optional[str] = None


@router.post("/onboarding/{session_id}/decision")
async def onboarding_decision(
    session_id: str,
    body: OnboardingDecision,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """
    Approve a passed applicant to join as a developer: emails their results
    and fresh login credentials (opening the projects portal).
    """
    try:
        result = await approve_applicant(
            db, session_id, approve=body.approve, notes=body.notes
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return result


# ---------------------------------------------------------------------------
# Talent pool (today.md: qualified personnel from assessments)
# ---------------------------------------------------------------------------
@router.get("/talent-pool")
async def talent_pool(
    category_filter: Optional[str] = None,
    min_percentage: Optional[float] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """
    Qualified personnel (completed assessments, 50%+) with their latest
    classification, competency band, and active project load - the N.O.U.
    Talent Pool used for project staffing (today.md sec. 6-8).
    """
    from app.api.v1.project_lifecycle import _active_project_count

    # Latest completed session per applicant.
    latest_ids = select(
        func.max(AssessmentSession.id)
    ).where(
        AssessmentSession.status == "completed"
    ).group_by(AssessmentSession.applicant_id).subquery()

    query = (
        select(AssessmentSession, User)
        .join(User, User.id == AssessmentSession.applicant_id)
        .join(latest_ids, latest_ids.c.max == AssessmentSession.id)
        .where(AssessmentSession.percentage >= 50)
        .order_by(AssessmentSession.percentage.desc())
    )
    if category_filter:
        query = query.where(AssessmentSession.category_name == category_filter)
    if min_percentage is not None:
        query = query.where(AssessmentSession.percentage >= min_percentage)

    total = await db.scalar(select(func.count()).select_from(query.subquery()))
    result = await db.execute(
        query.offset((page - 1) * limit).limit(limit)
    )
    rows = result.all()

    personnel = []
    for session, user in rows:
        personnel.append({
            "user_id": user.id,
            "name": f"{user.first_name} {user.last_name}".strip() or user.email,
            "email": user.email,
            "category": session.category_name,
            "position": session.position_name,
            "percentage": session.percentage,
            "competency_band": session.competency_band,
            "assessment_date": session.completed_at,
            "active_projects": await _active_project_count(db, user.id),
            "availability": "available" if await _active_project_count(db, user.id) < 3 else "fully_assigned",
        })

    return {
        "personnel": personnel,
        "pagination": {"total": total, "page": page, "limit": limit,
                       "pages": (total + limit - 1) // limit if total else 0},
    }


@router.get("/talent-pool/categories")
async def talent_pool_categories(
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Distinct professional categories present in the talent pool."""
    result = await db.execute(
        select(AssessmentSession.category_name).distinct().where(
            AssessmentSession.status == "completed",
            AssessmentSession.category_name.isnot(None),
        )
    )
    return {"categories": [c for (c,) in result.all() if c]}


# ---------------------------------------------------------------------------
# Company projects portal (admin)
# ---------------------------------------------------------------------------
@router.post("/projects", status_code=status.HTTP_201_CREATED)
async def create_company_project(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    section: Optional[str] = Form(None),
    required_people: int = Form(1, ge=1, le=20),
    budget: Optional[float] = Form(None),
    deadline: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Create a project/job post (optional PDF/DOCX spec upload + gallery
    section). Form body, consistent with the existing admin product endpoint."""
    from app.api.v1.projects_portal import _save_upload, _project_payload
    from sqlalchemy.orm import selectinload

    parsed_deadline = None
    if deadline:
        try:
            parsed_deadline = datetime.strptime(deadline, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(
                status_code=422,
                detail="Deadline must be a date in YYYY-MM-DD format",
            )

    new_project = CompanyProject(
        title=title,
        description=description,
        category=category,
        section=section,
        required_people=required_people,
        budget=budget,
        deadline=parsed_deadline,
        created_by=current_user.id,
        status="open",
    )
    db.add(new_project)
    await db.flush()

    if file:
        stored_path = await _save_upload(file, "spec")
        db.add(ProjectDocument(
            project_id=new_project.id,
            filename=file.filename or "spec.pdf",
            stored_path=stored_path,
            doc_type="spec",
            uploaded_by=current_user.id,
        ))

    await db.commit()
    fresh = await db.scalar(
        select(CompanyProject)
        .options(
            selectinload(CompanyProject.members),
            selectinload(CompanyProject.documents),
            selectinload(CompanyProject.progress_reports),
            selectinload(CompanyProject.help_requests),
            selectinload(CompanyProject.deadline_extensions),
            selectinload(CompanyProject.staffing_plan),
            selectinload(CompanyProject.change_requests),
            selectinload(CompanyProject.releases),
        )
        .where(CompanyProject.id == new_project.id)
    )
    return _project_payload(fresh or new_project)


@router.get("/projects")
async def admin_list_projects(
    status_filter: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Admin listing of all company projects (with members + docs)."""
    from sqlalchemy.orm import selectinload
    query = (
        select(CompanyProject)
        .options(
            selectinload(CompanyProject.members).selectinload(ProjectMember.user),
            selectinload(CompanyProject.documents),
            selectinload(CompanyProject.progress_reports),
            selectinload(CompanyProject.help_requests),
            selectinload(CompanyProject.deadline_extensions),
            selectinload(CompanyProject.staffing_plan),
            selectinload(CompanyProject.change_requests),
            selectinload(CompanyProject.releases),
        )
    )
    if status_filter:
        query = query.where(CompanyProject.status == status_filter)
    total = await db.scalar(select(func.count()).select_from(query.subquery()))
    result = await db.execute(
        query.order_by(CompanyProject.created_at.desc())
        .offset((page - 1) * limit).limit(limit)
    )
    projects = result.scalars().all()
    from app.api.v1.projects_portal import _project_payload
    return {
        "projects": [_project_payload(p) for p in projects],
        "pagination": {"total": total, "page": page, "limit": limit,
                       "pages": (total + limit - 1) // limit if total else 0},
    }


class PublishProjectIn(BaseModel):
    section: Optional[str] = Field(None, max_length=50)
    # N.O.U. product classification (today.md): Free/Paid/Subscription/...
    product_status: Optional[str] = Field(None, max_length=40)
    # N.O.U. platform classification (today.md): Web/PWA/Android/...
    platform: Optional[str] = Field(None, max_length=60)


@router.post("/projects/{project_id}/publish")
async def admin_publish_project(
    project_id: str,
    body: Optional[PublishProjectIn] = None,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Publish a completed project for customers under a gallery section
    (Games, Bots, Education, ...), with product status + platform from the
    N.O.U. product-classification system (today.md)."""
    project = await db.scalar(
        select(CompanyProject).where(CompanyProject.id == project_id)
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.status != "review":
        raise HTTPException(
            status_code=400,
            detail="Only projects under review can be published (upload completed work first)",
        )
    if body:
        if body.section:
            project.section = body.section
        if body.product_status:
            project.product_status = body.product_status
        if body.platform:
            project.platform = body.platform
    project.status = "published"
    await db.commit()
    return {
        "message": "Project published for customers",
        "status": project.status,
        "section": project.section,
        "product_status": project.product_status,
        "platform": project.platform,
    }


# ---------------------------------------------------------------------------
# Software releases - admin uploads the developed software (.apk/.zip/...)
# so customers can download and install it on their own devices.
# ---------------------------------------------------------------------------
@router.post("/projects/{project_id}/releases", status_code=status.HTTP_201_CREATED)
async def admin_upload_release(
    project_id: str,
    file: UploadFile = File(...),
    version: str = Form("1.0.0"),
    platform: Optional[str] = Form(None),
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Upload a software build (.apk, .aab, .zip, .exe, ...) for a project.
    The release appears in the customer gallery download list once the
    project is published."""
    from app.api.v1.projects_portal import _save_release

    project = await db.scalar(
        select(CompanyProject).where(CompanyProject.id == project_id)
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.status in ("published",):
        # Allowed: publishing a new version of already-published software.
        pass

    stored_path = await _save_release(file)
    release = ProjectRelease(
        project_id=project.id,
        filename=file.filename or "release",
        stored_path=stored_path,
        version=version or "1.0.0",
        platform=platform,
        file_size=os.path.getsize(stored_path),
        uploaded_by=current_user.id,
    )
    db.add(release)
    await db.commit()
    await db.refresh(release)
    return {
        "message": f"Release {release.filename} uploaded",
        "release": {
            "id": release.id,
            "filename": release.filename,
            "version": release.version,
            "platform": release.platform,
            "file_size": release.file_size,
        },
    }


@router.delete("/projects/{project_id}/releases/{release_id}")
async def admin_delete_release(
    project_id: str,
    release_id: str,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Soft-delete a release (it stops appearing in downloads)."""
    release = await db.scalar(
        select(ProjectRelease).where(
            ProjectRelease.id == release_id,
            ProjectRelease.project_id == project_id,
        )
    )
    if not release:
        raise HTTPException(status_code=404, detail="Release not found")
    release.is_active = False
    await db.commit()
    return {"message": "Release removed"}


@router.get("/projects/extensions")
async def admin_list_extensions(
    status_filter: Optional[str] = None,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """List project deadline-extension requests (pending/approved/denied)."""
    query = select(ProjectDeadlineExtension)
    if status_filter:
        query = query.where(ProjectDeadlineExtension.status == status_filter)
    result = await db.execute(
        query.order_by(ProjectDeadlineExtension.created_at.desc())
    )
    return {"requests": result.scalars().all()}


class ExtensionDecision(BaseModel):
    approve: bool = True


@router.post("/projects/extensions/{extension_id}/decision")
async def admin_extension_decision(
    extension_id: str,
    body: ExtensionDecision,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Approve/deny a deadline extension (max 4 weeks from the schedule)."""
    ext = await db.scalar(
        select(ProjectDeadlineExtension).where(
            ProjectDeadlineExtension.id == extension_id
        )
    )
    if not ext:
        raise HTTPException(status_code=404, detail="Extension request not found")
    if ext.status != "pending":
        raise HTTPException(status_code=400, detail="Extension already decided")
    ext.status = "approved" if body.approve else "denied"
    ext.decided_by = current_user.id
    ext.decided_at = datetime.now()
    await db.commit()
    project = await db.scalar(
        select(CompanyProject).where(CompanyProject.id == ext.project_id)
    )
    return {
        "message": "Extension " + ext.status,
        "extension_id": ext.id,
        "effective_deadline": str(
            project.deadline) if project and project.deadline else None,
    }


@router.get("/projects/extra-requests")
async def admin_extra_requests(
    status_filter: Optional[str] = None,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """List team requests for extra developers."""
    query = select(ExtraDeveloperRequest)
    if status_filter:
        query = query.where(ExtraDeveloperRequest.status == status_filter)
    result = await db.execute(query.order_by(ExtraDeveloperRequest.created_at.desc()))
    return {"requests": result.scalars().all()}


class ExtraDecision(BaseModel):
    approve: bool = True


@router.post("/projects/extra-requests/{request_id}/decision")
async def admin_extra_decision(
    request_id: str,
    body: ExtraDecision,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Approve/deny an extra-developer request; approved projects can take more members."""
    req = await db.scalar(
        select(ExtraDeveloperRequest).where(ExtraDeveloperRequest.id == request_id)
    )
    if not req:
        raise HTTPException(status_code=404, detail="Extra developer request not found")
    req.status = "approved" if body.approve else "denied"
    req.decided_by = current_user.id
    req.decided_at = datetime.utcnow()
    project = await db.scalar(
        select(CompanyProject).where(CompanyProject.id == req.project_id)
    )
    if project and body.approve:
        # Approved requests raise the project's headroom for the requested count.
        project.required_people += req.requested_count
    await db.commit()
    return {"message": "Request " + req.status, "required_people": project.required_people if project else None}


# ---------------------------------------------------------------------------
# N.O.U Lite orders (admin review)
# ---------------------------------------------------------------------------
@router.get("/nou-lite/orders")
async def admin_nou_lite_orders(
    status_filter: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    query = select(NouliteOrder)
    if status_filter:
        query = query.where(NouliteOrder.status == status_filter)
    total = await db.scalar(select(func.count()).select_from(query.subquery()))
    result = await db.execute(
        query.order_by(NouliteOrder.created_at.desc())
        .offset((page - 1) * limit).limit(limit)
    )
    return {
        "orders": result.scalars().all(),
        "pagination": {"total": total, "page": page, "limit": limit,
                       "pages": (total + limit - 1) // limit if total else 0},
    }


class NouLiteOrderStatus(BaseModel):
    status: str


@router.put("/nou-lite/orders/{order_id}/status")
async def admin_nou_lite_order_status(
    order_id: str,
    body: NouLiteOrderStatus,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    if body.status not in {"new", "in_progress", "completed", "declined"}:
        raise HTTPException(
            status_code=422,
            detail="Status must be one of: new, in_progress, completed, declined",
        )
    order = await db.scalar(
        select(NouliteOrder).where(NouliteOrder.id == order_id)
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = body.status
    await db.commit()
    return {"message": "Order status updated", "status": order.status}


# ---------------------------------------------------------------------------
# AI key pool status (admin debug)
# ---------------------------------------------------------------------------
@router.get("/ai/pool")
async def ai_pool_status(
    current_user: User = Depends(require_admin),
):
    from app.services.groq_pool import pool_status
    return pool_status()


# ---------------------------------------------------------------------------
# Site analytics: daily visits, visitors, uptime and API key health
# ---------------------------------------------------------------------------
@router.get("/analytics/visits")
async def admin_analytics_visits(
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """
    Daily site-visit statistics: today, all-time totals, the last 14 days
    (visits + unique visitors per day) and the most-viewed pages.
    """
    today = date.today()

    today_visits = await db.scalar(
        select(func.count()).select_from(SiteVisit).where(SiteVisit.visit_date == today)
    ) or 0
    today_unique = await db.scalar(
        select(func.count(func.distinct(SiteVisit.ip)))
        .select_from(SiteVisit)
        .where(SiteVisit.visit_date == today)
    ) or 0
    total_visits = await db.scalar(select(func.count()).select_from(SiteVisit)) or 0
    total_unique = await db.scalar(
        select(func.count(func.distinct(SiteVisit.ip))).select_from(SiteVisit)
    ) or 0

    start = today - timedelta(days=13)
    rows = await db.execute(
        select(
            SiteVisit.visit_date,
            func.count(SiteVisit.id),
            func.count(func.distinct(SiteVisit.ip)),
        )
        .where(SiteVisit.visit_date >= start)
        .group_by(SiteVisit.visit_date)
    )
    by_date = {d: (int(visits), int(uniq)) for d, visits, uniq in rows.all()}
    daily = []
    for i in range(13, -1, -1):
        d = today - timedelta(days=i)
        visits, uniq = by_date.get(d, (0, 0))
        daily.append({"date": d.isoformat(), "visits": visits, "unique": uniq})

    top_rows = await db.execute(
        select(SiteVisit.path, func.count(SiteVisit.id))
        .group_by(SiteVisit.path)
        .order_by(func.count(SiteVisit.id).desc())
        .limit(10)
    )
    top_pages = [{"path": path, "count": count} for path, count in top_rows.all()]

    return {
        "today": {"visits": today_visits, "unique": today_unique},
        "totals": {"visits": total_visits, "unique": total_unique},
        "daily": daily,
        "top_pages": top_pages,
    }


@router.get("/system/status")
async def admin_system_status(
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """
    Site uptime and internal runnings: how long the API has been up, whether
    the database responds, the environment, and the configured AI key pools.
    """
    db_ok = True
    try:
        await db.execute(sa_text("SELECT 1"))
    except Exception:  # noqa: BLE001
        db_ok = False

    uptime_seconds = max(0, int((datetime.utcnow() - _SERVER_STARTED_AT).total_seconds()))
    days, rem = divmod(uptime_seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, _ = divmod(rem, 60)
    uptime_human = f"{days}d {hours}h {minutes}m" if days else f"{hours}h {minutes}m"

    key_sections = {
        "assessments": settings.GROQ_ASSESSMENT_KEYS,
        "nou_lite": settings.GROQ_CHATBOT_KEYS,
        "project_chat": settings.GROQ_COMMUNITY_KEYS,
        "general": settings.GROQ_API_KEYS,
    }
    keys_configured = sum(1 for keys in key_sections.values() for k in keys if k)

    failed_keys_today = await db.scalar(
        select(func.count())
        .select_from(AIKeyUsage)
        .where(AIKeyUsage.usage_date == date.today(), AIKeyUsage.failed == True)  # noqa: E712
    ) or 0

    return {
        "status": "up" if db_ok else "degraded",
        "uptime_seconds": uptime_seconds,
        "uptime": uptime_human,
        "server_started_at": _SERVER_STARTED_AT.isoformat() + "Z",
        "server_time": datetime.utcnow().isoformat() + "Z",
        "database": "ok" if db_ok else "unreachable",
        "environment": settings.ENVIRONMENT,
        "version": settings.APP_VERSION,
        "python_version": sys.version.split()[0],
        "ai_keys_configured": keys_configured,
        "ai_keys_failed_today": failed_keys_today,
        "workers": {
            "results_email": "running (scheduled)",
        },
    }


@router.get("/ai/keys")
async def admin_ai_key_health(
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """
    Health report for every configured Groq API key: which section it serves,
    how many requests it served today, and whether it has failed (auth/expiry)
    so it is skipped for the rest of the day.
    """
    today = date.today()
    sections = [
        ("assessments", settings.GROQ_ASSESSMENT_KEYS),
        ("nou_lite", settings.GROQ_CHATBOT_KEYS),
        ("project_chat", settings.GROQ_COMMUNITY_KEYS),
        ("general", settings.GROQ_API_KEYS),
    ]
    keys = []
    for section, section_keys in sections:
        for idx, key in enumerate(section_keys):
            if not key:
                continue
            masked = f"{key[:6]}...{key[-4:]}" if len(key) > 12 else "configured"
            usage = await db.scalar(
                select(AIKeyUsage).where(
                    AIKeyUsage.usage_date == today,
                    AIKeyUsage.section == section,
                    AIKeyUsage.key_index == idx,
                )
            )
            keys.append({
                "section": section,
                "index": idx,
                "masked": masked,
                "requests_today": usage.requests if usage else 0,
                "failed": bool(usage and usage.failed),
                "healthy": not (usage and usage.failed),
            })
    return {
        "keys": keys,
        "configured": len(keys),
        "failed_today": sum(1 for k in keys if k["failed"]),
    }


# ---------------------------------------------------------------------------
# Mobile applications: admin publishes apps (banner + description + APK)
# and customers view/comment/download them on the public Apps page.
# ---------------------------------------------------------------------------
async def _save_app_file(file: UploadFile, subdir: str) -> tuple:
    """Save an app banner/APK under uploads/apps/<subdir>/ and return
    (path, size). APK size is validated against the release limit."""
    contents = await file.read()
    ext = os.path.splitext(file.filename or "file")[1]
    stored_name = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(settings.UPLOAD_DIR, "apps", subdir, stored_name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(contents)
    return path, len(contents)


def _app_payload(a: MobileApp, comments_count: int = 0) -> dict:
    # NOTE: never touch the ``comments`` relationship here - lazy-loading it
    # in an async context raises MissingGreenlet. Counts come from a query.
    return {
        "id": a.id,
        "name": a.name,
        "tagline": a.tagline,
        "description": a.description,
        "version": a.version,
        "platform": a.platform,
        "status": a.status,
        "banner_image": a.banner_image,
        "apk_file": a.apk_file,
        "apk_filename": a.apk_filename,
        "apk_size": a.apk_size,
        "downloads": a.downloads or 0,
        "comments_count": comments_count,
        "created_at": a.created_at,
        "updated_at": a.updated_at,
    }


@router.get("/apps")
async def admin_list_apps(
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """List all mobile apps (upcoming + published)."""
    rows = await db.execute(
        select(MobileApp)
        .where(MobileApp.is_active == True)  # noqa: E712
        .order_by(MobileApp.created_at.desc())
    )
    apps = rows.scalars().all()
    count_rows = await db.execute(
        select(AppComment.app_id, func.count(AppComment.id)).group_by(AppComment.app_id)
    )
    comment_counts = {int(app_id): int(c) for app_id, c in count_rows.all()}
    return {
        "apps": [_app_payload(a, comments_count=comment_counts.get(a.id, 0)) for a in apps]
    }


@router.post("/apps", status_code=status.HTTP_201_CREATED)
async def admin_create_app(
    name: str = Form(...),
    tagline: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    version: str = Form("1.0.0"),
    platform: str = Form("Android"),
    status: str = Form("upcoming"),
    banner: Optional[UploadFile] = File(None),
    apk: Optional[UploadFile] = File(None),
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """
    Publish an application: give it a banner, description and (optionally) the
    APK file customers download. Uploading an APK makes the app 'published'.
    """
    if status not in {"upcoming", "published"}:
        raise HTTPException(status_code=422, detail="status must be 'upcoming' or 'published'")

    banner_path = None
    if banner and banner.filename:
        banner_path, _ = await _save_app_file(banner, "banners")

    apk_path = apk_filename = None
    apk_size = None
    if apk and apk.filename:
        if not apk.filename.lower().endswith(".apk"):
            raise HTTPException(status_code=415, detail="Only .apk files can be uploaded for download")
        if apk.content_type == "text/html":
            raise HTTPException(status_code=415, detail="Invalid APK file")
        apk_path, apk_size = await _save_app_file(apk, "apk")
        apk_filename = apk.filename
        if apk_size > settings.MAX_RELEASE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"APK exceeds the {settings.MAX_RELEASE_SIZE // (1024 * 1024)}MB limit",
            )
        # An uploaded APK means the app is available for download.
        status = "published"

    new_app = MobileApp(
        name=name,
        tagline=tagline,
        description=description,
        version=version,
        platform=platform,
        status=status,
        banner_image=banner_path,
        apk_file=apk_path,
        apk_filename=apk_filename,
        apk_size=apk_size,
        created_by=current_user.id,
    )
    db.add(new_app)
    await db.commit()
    await db.refresh(new_app)
    return {"message": f"App '{new_app.name}' published", "app": _app_payload(new_app)}


@router.put("/apps/{app_id}")
async def admin_update_app(
    app_id: str,
    name: Optional[str] = Form(None),
    tagline: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    version: Optional[str] = Form(None),
    platform: Optional[str] = Form(None),
    status: Optional[str] = Form(None),
    banner: Optional[UploadFile] = File(None),
    apk: Optional[UploadFile] = File(None),
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Update an app's details, banner, APK or status."""
    app = await db.scalar(
        select(MobileApp).where(MobileApp.id == app_id, MobileApp.is_active == True)  # noqa: E712
    )
    if not app:
        raise HTTPException(status_code=404, detail="App not found")
    if status and status not in {"upcoming", "published"}:
        raise HTTPException(status_code=422, detail="status must be 'upcoming' or 'published'")

    if name is not None:
        app.name = name
    if tagline is not None:
        app.tagline = tagline
    if description is not None:
        app.description = description
    if version is not None:
        app.version = version
    if platform is not None:
        app.platform = platform
    if status is not None:
        app.status = status
    if banner and banner.filename:
        app.banner_image, _ = await _save_app_file(banner, "banners")
    if apk and apk.filename:
        if not apk.filename.lower().endswith(".apk"):
            raise HTTPException(status_code=415, detail="Only .apk files can be uploaded for download")
        app.apk_file, app.apk_size = await _save_app_file(apk, "apk")
        app.apk_filename = apk.filename
        app.status = "published"
    await db.commit()
    await db.refresh(app)
    return {"message": "App updated", "app": _app_payload(app)}


@router.delete("/apps/{app_id}")
async def admin_delete_app(
    app_id: str,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Soft-delete an app (it disappears from the public Apps page)."""
    app = await db.scalar(
        select(MobileApp).where(MobileApp.id == app_id, MobileApp.is_active == True)  # noqa: E712
    )
    if not app:
        raise HTTPException(status_code=404, detail="App not found")
    app.is_active = False
    await db.commit()
    return {"message": "App removed"}


# ---------------------------------------------------------------------------
# Customer project requests: review -> feasibility -> quotation -> payment
# (today.md docs 8 + 9)
# ---------------------------------------------------------------------------
REQUEST_STATUSES = {
    "submitted", "under_review", "clarification_required", "technically_feasible",
    "documentation", "estimation", "quotation_issued", "customer_decision",
    "agreement", "awaiting_deposit", "payment_verified", "project_activated",
    "development", "testing", "delivery", "completed",
    "declined", "cancelled", "on_hold", "suspended", "terminated",
}


def _pr_payload(r: ProjectRequest) -> dict:
    deposit_amount = None
    if r.quotation_amount is not None:
        deposit_amount = float(r.quotation_amount) * (r.deposit_percent or 30) / 100
    customer_name = None
    if r.customer and r.customer.user:
        customer_name = f"{r.customer.user.first_name} {r.customer.user.last_name}".strip()
    return {
        "id": r.id,
        "request_number": r.request_number,
        "title": r.title,
        "description": r.description,
        "service_type": r.service_type,
        "location": r.location,
        "category": r.category,
        "status": r.status,
        "customer": {
            "id": r.customer_id,
            "name": customer_name or "-",
            "email": r.customer.user.email if r.customer and r.customer.user else None,
        },
        "budget": float(r.budget) if r.budget is not None else None,
        "deadline": r.deadline,
        "admin_notes": r.admin_notes,
        "admin_decision": r.admin_decision,
        "decision_at": r.decision_at,
        "quotation_amount": float(r.quotation_amount) if r.quotation_amount is not None else None,
        "quotation_currency": r.quotation_currency,
        "deposit_percent": r.deposit_percent,
        "deposit_amount": deposit_amount,
        "payment_schedule": r.payment_schedule,
        "scope_included": r.scope_included,
        "scope_excluded": r.scope_excluded,
        "quotation_version": r.quotation_version,
        "quotation_issued_at": r.quotation_issued_at,
        "quotation_accepted_at": r.quotation_accepted_at,
        "agreed_amount": float(r.agreed_amount) if r.agreed_amount is not None else None,
        "paid_amount": float(r.paid_amount) if r.paid_amount is not None else 0,
        "activated_at": r.activated_at,
        "created_at": r.created_at,
        "payments": [{
            "id": p.id,
            "payment_type": p.payment_type,
            "amount": float(p.amount),
            "currency": p.currency,
            "status": p.status,
            "method": p.method,
            "reference": p.reference,
            "provider_reference": p.provider_reference,
            "receipt_number": p.receipt_number,
            "verified_at": p.verified_at,
            "created_at": p.created_at,
        } for p in (r.payments or [])],
    }


async def _get_request(db: AsyncSession, request_id: str) -> ProjectRequest:
    from sqlalchemy.orm import selectinload
    r = await db.scalar(
        select(ProjectRequest)
        .options(
            selectinload(ProjectRequest.customer).selectinload(Customer.user),
            selectinload(ProjectRequest.payments),
        )
        .where(ProjectRequest.id == request_id)
    )
    if not r:
        raise HTTPException(status_code=404, detail="Project request not found")
    return r


@router.get("/support-contributions")
async def admin_support_contributions(
    status_filter: Optional[str] = None,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """List support contributions (footer donations) so admins can see who
    contributed, how much, and whether the payment was completed."""
    query = select(ProjectPayment).where(ProjectPayment.payment_type == "support")
    if status_filter:
        query = query.where(ProjectPayment.status == status_filter)
    result = await db.execute(
        query.order_by(ProjectPayment.created_at.desc())
    )
    payments = []
    for p in result.scalars().all():
        payments.append({
            "id": p.id,
            "amount": float(p.amount),
            "currency": p.currency,
            "status": p.status,
            "method": p.method,
            "receipt_number": p.receipt_number,
            "provider_reference": p.provider_reference,
            "notes": p.notes,
            "paid_at": p.paid_at,
            "created_at": p.created_at,
        })
    return {"contributions": payments}


@router.get("/project-requests")
async def admin_list_project_requests(
    status_filter: Optional[str] = None,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """List customer project requests (optionally by status)."""
    from sqlalchemy.orm import selectinload
    query = (
        select(ProjectRequest)
        .options(
            selectinload(ProjectRequest.customer).selectinload(Customer.user),
            selectinload(ProjectRequest.payments),
        )
    )
    if status_filter:
        query = query.where(ProjectRequest.status == status_filter)
    result = await db.execute(query.order_by(ProjectRequest.created_at.desc()))
    return {"requests": [_pr_payload(r) for r in result.scalars().all()]}


class RequestReviewIn(BaseModel):
    decision: str = Field(..., pattern="^(approve|clarify|decline)$")
    note: Optional[str] = None


@router.post("/project-requests/{request_id}/review")
async def admin_review_request(
    request_id: str,
    body: RequestReviewIn,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Initial administrative review: approve for technical review / clarify / decline."""
    r = await _get_request(db, request_id)
    if body.decision == "approve":
        r.status = "technically_feasible"
    elif body.decision == "clarify":
        r.status = "clarification_required"
    else:
        r.status = "declined"
    r.admin_notes = body.note or r.admin_notes
    r.admin_decision = f"initial_review:{body.decision}"
    r.decision_at = datetime.now()
    await db.commit()
    return {"message": f"Request {body.decision}d", "request": _pr_payload(r)}


class FeasibilityIn(BaseModel):
    decision: str = Field(..., pattern="^(feasible|conditions|clarify|not_feasible)$")
    note: Optional[str] = None


@router.post("/project-requests/{request_id}/feasibility")
async def admin_feasibility(
    request_id: str,
    body: FeasibilityIn,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Technical feasibility decision (feasible != accepted; quotation follows)."""
    r = await _get_request(db, request_id)
    if body.decision == "feasible":
        r.status = "documentation"
    elif body.decision == "conditions":
        r.status = "documentation"
    elif body.decision == "clarify":
        r.status = "clarification_required"
    else:
        r.status = "declined"
    r.admin_notes = body.note or r.admin_notes
    r.admin_decision = f"feasibility:{body.decision}"
    r.decision_at = datetime.now()
    await db.commit()
    return {"message": f"Feasibility: {body.decision}", "request": _pr_payload(r)}


class QuotationIn(BaseModel):
    quotation_amount: float = Field(..., gt=0)
    currency: str = "KSh"
    deposit_percent: int = Field(30, ge=0, le=100)
    payment_schedule: Optional[str] = None
    scope_included: Optional[str] = None
    scope_excluded: Optional[str] = None


@router.post("/project-requests/{request_id}/quotation")
async def admin_issue_quotation(
    request_id: str,
    body: QuotationIn,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Issue a formal quotation -> QUOTATION ISSUED (customer decides)."""
    r = await _get_request(db, request_id)
    r.quotation_amount = body.quotation_amount
    r.quotation_currency = body.currency
    r.deposit_percent = body.deposit_percent
    r.payment_schedule = body.payment_schedule
    r.scope_included = body.scope_included
    r.scope_excluded = body.scope_excluded
    r.status = "quotation_issued"
    r.quotation_version = (r.quotation_version or 0) + 1
    r.quotation_issued_at = datetime.now()
    r.admin_decision = f"quotation:v{r.quotation_version}"
    r.decision_at = datetime.now()
    await db.commit()
    return {"message": "Quotation issued", "request": _pr_payload(r)}


@router.post("/project-requests/{request_id}/payments/{payment_id}/verify")
async def admin_verify_payment(
    request_id: str,
    payment_id: str,
    approve: bool = True,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Admin verifies a submitted payment. A verified deposit activates the
    project (today.md doc 8 sec. 20-23)."""
    r = await _get_request(db, request_id)
    payment = next(
        (p for p in (r.payments or []) if str(p.id) == str(payment_id)), None
    )
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    if payment.status == "successful":
        raise HTTPException(status_code=400, detail="Payment already verified")

    if approve:
        year = datetime.now().year
        seq = await db.scalar(
            select(func.count()).select_from(ProjectPayment)
            .where(ProjectPayment.receipt_number.like(f"NOU-RCP-{year}-%"))
        ) or 0
        payment.status = "successful"
        payment.receipt_number = f"NOU-RCP-{year}-{(seq + 1):04d}"
        payment.verified_by = current_user.id
        payment.verified_at = datetime.now()
        payment.paid_at = datetime.now()
        r.paid_amount = (r.paid_amount or 0) + payment.amount
        # Deposit verified -> project activates.
        if r.status in ("awaiting_deposit", "payment_verified"):
            r.status = "project_activated"
            r.activated_at = datetime.now()
    else:
        payment.status = "failed"
        payment.notes = "Rejected by N.O.U. administration"
    await db.commit()
    return {
        "message": "Payment verified - project activated" if approve else "Payment rejected",
        "request": _pr_payload(r),
    }


class RequestStatusIn(BaseModel):
    status: str = Field(..., min_length=1, max_length=40)


@router.post("/project-requests/{request_id}/status")
async def admin_set_request_status(
    request_id: str,
    body: RequestStatusIn,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Advance a project through development/testing/delivery/completed or pause it."""
    if body.status not in REQUEST_STATUSES:
        raise HTTPException(status_code=422, detail="Invalid project request status")
    r = await _get_request(db, request_id)
    r.status = body.status
    if body.status == "completed":
        r.activated_at = r.activated_at or datetime.now()
    await db.commit()
    return {"message": f"Status set to {body.status}", "request": _pr_payload(r)}


# ---------------------------------------------------------------------------
# Question bank (100 pre-generated AI questions per professional category)
# ---------------------------------------------------------------------------
async def _bank_categories_payload(db: AsyncSession, categories: List[PersonnelCategory]) -> dict:
    """Build the admin question-bank status payload for a list of categories."""
    counts_by_category: dict = {}
    # One grouped query for every category's per-part counts.
    rows = await db.execute(
        select(
            QuestionBankQuestion.category_id,
            QuestionBankQuestion.part,
            func.count(QuestionBankQuestion.id),
        )
        .where(QuestionBankQuestion.is_active == True)  # noqa: E712
        .group_by(QuestionBankQuestion.category_id, QuestionBankQuestion.part)
    )
    for category_id, part, count in rows.all():
        counts_by_category.setdefault(int(category_id), {})[part] = int(count)

    # Position counts per category (no lazy-loading in async contexts).
    position_counts: dict = {}
    p_rows = await db.execute(
        select(
            PersonnelCategory.id,
            func.count(PersonnelPosition.id),
        )
        .join(PersonnelPosition, PersonnelPosition.category_id == PersonnelCategory.id)
        .where(PersonnelPosition.is_active == "active")
        .group_by(PersonnelCategory.id)
    )
    for cat_id, count in p_rows.all():
        position_counts[int(cat_id)] = int(count)

    items = []
    for cat in categories:
        counts = counts_by_category.get(cat.id, {})
        total = sum(counts.values())
        items.append({
            "id": cat.id,
            "name": cat.name,
            "positions": position_counts.get(cat.id, 0),
            "per_part": {p: counts.get(p, 0) for p in PARTS},
            "total": total,
            "ready": total >= BANK_QUESTIONS_PER_PART * len(PARTS),
        })
    return items


@router.get("/question-bank")
async def admin_question_bank_status(
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Question bank status per professional category: how many questions are
    stored and whether the category is ready for instant assessments (100)."""
    categories = (
        await db.execute(
            select(PersonnelCategory)
            .where(PersonnelCategory.is_active == "active")
            .order_by(PersonnelCategory.name)
        )
    ).scalars().all()
    return {"categories": await _bank_categories_payload(db, categories)}


@router.post("/question-bank/generate/{category_id}", status_code=status.HTTP_201_CREATED)
async def admin_generate_question_bank(
    category_id: int,
    bank_size: int = Query(BANK_QUESTIONS_PER_PART * len(PARTS), ge=20, le=300),
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """
    Generate (or top up) the 100-question AI bank for one professional
    category. Groq writes advanced real-world questions - 20 per assessment
    part (common/category/position/practical/professional). Every assessment
    in the category then draws 20 random questions from the bank instantly.
    Only missing questions are generated; re-running tops up.
    """
    category = await db.scalar(
        select(PersonnelCategory).where(
            PersonnelCategory.id == category_id,
            PersonnelCategory.is_active == "active",
        )
    )
    if not category:
        raise HTTPException(status_code=404, detail="Professional category not found")

    questions_per_part = max(1, bank_size // len(PARTS))
    try:
        counts = await ensure_bank(
            db, category, questions_per_part=questions_per_part
        )
    except ai_assessment.AINotConfiguredError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except ai_assessment.AIAPIError as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    total = sum(counts.values())
    return {
        "message": (
            f"Question bank for '{category.name}' is ready: {total} questions "
            f"stored (target {questions_per_part} per part). Assessments in this "
            f"category now start instantly."
        ),
        "category": category.name,
        "per_part": {p: counts.get(p, 0) for p in PARTS},
        "total": total,
        "ready": total >= questions_per_part * len(PARTS),
    }


@router.get("/cvs")
async def admin_list_cvs(
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """
    List every applicant who has a CV on file (uploaded via the Careers apply
    form), so the admin can read its contents and activate the Groq review
    from one place - regardless of whether they have completed an assessment
    yet.
    """
    rows = (
        await db.execute(
            select(User)
            .where(User.cv_file_path.isnot(None), User.role == "applicant")
            .order_by(User.created_at.desc())
        )
    ).scalars().all()
    applicants = []
    for u in rows:
        cv_summary = {}
        if u.cv_summary:
            try:
                cv_summary = json.loads(u.cv_summary)
            except (TypeError, ValueError):
                cv_summary = {}
        applicants.append({
            "id": u.id,
            "name": f"{u.first_name} {u.last_name}".strip() or u.email,
            "email": u.email,
            "phone": u.phone,
            "cv_file_path": u.cv_file_path,
            "cv_reviewed": bool(cv_summary.get("summary")),
            "cv_summary": cv_summary,
            "qualification_category": u.qualification_category_name,
            "qualification_position": u.qualification_position_name,
            "created_at": u.created_at,
        })
    return {"applicants": applicants}


# ---------------------------------------------------------------------------
# CV management (admin views the CV contents + Groq review/summary)
# ---------------------------------------------------------------------------
@router.get("/cv/{user_id}/download")
async def admin_download_cv(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Download the applicant's uploaded CV file."""
    user = await db.scalar(select(User).where(User.id == user_id))
    if not user or not user.cv_file_path:
        raise HTTPException(status_code=404, detail="No CV on file for this applicant")
    path = os.path.normpath(user.cv_file_path)
    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="CV file not found on the server")
    return FileResponse(
        path,
        filename=f"cv_{user_id}{os.path.splitext(path)[1]}",
        media_type="application/octet-stream",
    )


@router.get("/cv/{user_id}/text")
async def admin_cv_text(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Return the extracted plain-text contents of the applicant's CV so the
    admin can read it without downloading (PDF/DOCX/TXT)."""
    user = await db.scalar(select(User).where(User.id == user_id))
    if not user or not user.cv_file_path:
        raise HTTPException(status_code=404, detail="No CV on file for this applicant")
    text = extract_cv_text(user.cv_file_path)
    if not text.strip():
        raise HTTPException(
            status_code=422,
            detail="No readable text could be extracted from this CV (it may be a scanned image PDF).",
        )
    return {"text": text}


@router.post("/cv/{user_id}/review")
async def admin_review_cv(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """
    Activate Groq to review the applicant's CV: the extracted text is sent to
    Groq, which summarises it (overview, highlights, strengths, concerns) for
    the admin. The review is stored so it only runs once per CV.
    """
    user = await db.scalar(select(User).where(User.id == user_id))
    if not user or not user.cv_file_path:
        raise HTTPException(status_code=404, detail="No CV on file for this applicant")

    text = extract_cv_text(user.cv_file_path)
    if not text.strip():
        raise HTTPException(
            status_code=422,
            detail="No readable text could be extracted from this CV (it may be a scanned image PDF).",
        )

    try:
        review = await ai_assessment.review_cv_text(text)
    except ai_assessment.AINotConfiguredError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except ai_assessment.AIAPIError as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    user.cv_summary = json.dumps(review)
    await db.commit()
    return {"message": "CV reviewed by AI", "review": review}


# ---------------------------------------------------------------------------
# Complaints (forwarded from the public Complaints screen)
# ---------------------------------------------------------------------------
def _complaint_payload(c: Complaint) -> dict:
    return {
        "id": c.id,
        "full_name": c.full_name,
        "email": c.email,
        "phone": c.phone,
        "subject": c.subject,
        "category": c.category,
        "message": c.message,
        "status": c.status,
        "admin_notes": c.admin_notes,
        "created_at": c.created_at,
        "updated_at": c.updated_at,
        "resolved_at": c.resolved_at,
    }


@router.get("/complaints")
async def admin_list_complaints(
    status_filter: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """List every complaint forwarded from the public Complaints screen,
    newest first, optionally filtered by status."""
    query = select(Complaint)
    if status_filter:
        query = query.where(Complaint.status == status_filter)
    total = await db.scalar(select(func.count()).select_from(query.subquery()))
    result = await db.execute(
        query.order_by(Complaint.created_at.desc())
        .offset((page - 1) * limit).limit(limit)
    )
    complaints = result.scalars().all()
    return {
        "complaints": [_complaint_payload(c) for c in complaints],
        "pagination": {
            "total": total, "page": page, "limit": limit,
            "pages": (total + limit - 1) // limit if total else 0,
        },
    }


class ComplaintUpdate(BaseModel):
    status: str = Field(..., pattern="^(new|in_progress|resolved|closed)$")
    admin_notes: Optional[str] = None


@router.put("/complaints/{complaint_id}/status")
async def admin_update_complaint(
    complaint_id: int,
    body: ComplaintUpdate,
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """Update a complaint's status (and optionally the admin's notes)."""
    complaint = await db.scalar(
        select(Complaint).where(Complaint.id == complaint_id)
    )
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    complaint.status = body.status
    if body.admin_notes is not None:
        complaint.admin_notes = body.admin_notes
    if body.status in ("resolved", "closed") and not complaint.resolved_at:
        complaint.resolved_at = datetime.now()
    await db.commit()
    await db.refresh(complaint)
    return _complaint_payload(complaint)


# ---------------------------------------------------------------------------
# Per-category screens (each assessed category - e.g. Cybersecurity - has its
# own admin screen listing the candidates assessed in that category).
# ---------------------------------------------------------------------------
@router.get("/categories")
async def admin_category_screens(
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """
    All 29 professional categories with per-category assessment statistics
    (candidates assessed, passed, pending onboarding approval) so the admin
    can open each category's own screen from the dashboard.
    """
    categories = (
        await db.execute(
            select(PersonnelCategory)
            .options(selectinload(PersonnelCategory.positions))
            .where(PersonnelCategory.is_active == "active")
            .order_by(PersonnelCategory.name)
        )
    ).scalars().all()

    items = []
    for cat in categories:
        assessed = await db.scalar(
            select(func.count()).select_from(AssessmentSession).where(
                AssessmentSession.category_id == cat.id,
                AssessmentSession.status == "completed",
            )
        )
        passed = await db.scalar(
            select(func.count()).select_from(AssessmentSession).where(
                AssessmentSession.category_id == cat.id,
                AssessmentSession.status == "completed",
                AssessmentSession.ai_recommendation == "PASS",
            )
        )
        pending = await db.scalar(
            select(func.count()).select_from(AssessmentSession).where(
                AssessmentSession.category_id == cat.id,
                AssessmentSession.status == "completed",
                AssessmentSession.ai_recommendation == "PASS",
                AssessmentSession.onboarding_status == "pending",
            )
        )
        items.append({
            "id": cat.id,
            "name": cat.name,
            "description": cat.description,
            "positions_count": len(cat.positions or []),
            "assessed": assessed or 0,
            "passed": passed or 0,
            "pending_approval": pending or 0,
        })
    return {"categories": items}


@router.get("/categories/{category_id}/results")
async def admin_category_results(
    category_id: int,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """
    The per-category screen: every candidate assessed in this category with
    their contact details (name, email, phone), score, verdict and onboarding
    status - newest first. The admin can review and approve/decline from here.
    """
    category = await db.scalar(
        select(PersonnelCategory).where(PersonnelCategory.id == category_id)
    )
    if not category:
        raise HTTPException(status_code=404, detail="Professional category not found")

    joined = (
        select(AssessmentSession, User, Assessment)
        .join(User, User.id == AssessmentSession.applicant_id)
        .join(Assessment, Assessment.id == AssessmentSession.assessment_id)
        .where(
            AssessmentSession.category_id == category_id,
            AssessmentSession.status == "completed",
        )
    )
    total = await db.scalar(select(func.count()).select_from(joined.subquery()))
    result = await db.execute(
        joined.order_by(AssessmentSession.completed_at.desc())
        .offset((page - 1) * limit).limit(limit)
    )
    rows = result.all()

    results = []
    for session, applicant, assessment in rows:
        name = f"{applicant.first_name} {applicant.last_name}".strip() or (applicant.email if applicant else "Unknown")
        results.append({
            "session_id": session.id,
            "applicant": {
                "id": session.applicant_id,
                "name": name,
                "email": applicant.email if applicant else None,
                "phone": applicant.phone if applicant else None,
                "cv_file_path": applicant.cv_file_path if applicant else None,
                "policies_accepted_at": applicant.policies_accepted_at if applicant else None,
            },
            "assessment": {
                "id": session.assessment_id,
                "title": assessment.title if assessment else "Assessment",
            },
            "position_name": session.position_name,
            "score": session.score,
            "percentage": session.percentage,
            "recommendation": session.ai_recommendation,
            "summary": session.ai_summary,
            "completed_at": session.completed_at,
            "competency_band": session.competency_band,
            "onboarding_status": session.onboarding_status,
        })

    return {
        "category": {"id": category.id, "name": category.name},
        "results": results,
        "pagination": {
            "total": total, "page": page, "limit": limit,
            "pages": (total + limit - 1) // limit if total else 0,
        },
    }