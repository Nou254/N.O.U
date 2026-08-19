"""
N.O.U Digital Systems - Main FastAPI Application
Centralized web platform for customer interaction, software distribution,
and competency-based technical recruitment.
"""

import asyncio
import threading
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1 import (
    auth, products, customers, employment, personnel, assessments, support,
    admin, projects, investors, projects_portal, project_lifecycle, nou_lite,
    announcements, community, payments, apps, complaints, policies,
)
from app.services.results_email import results_email_worker
from app.core.rate_limit import allow_request
from app.api.v1.policies import ensure_policies_seeded
# Ensure tables that are only referenced lazily are registered with
# Base.metadata at startup (create_all creates them).
from app.models.project_release import ProjectRelease  # noqa: F401
from app.models.question_bank import QuestionBankQuestion  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager for startup and shutdown events.
    """
    # Startup
    logger.info("Starting N.O.U Digital Systems API...")
    
    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("Database tables created/verified")

    # Seed the organization policies document from the bundled text file
    # (no-op when already present).
    await ensure_policies_seeded()

    # Background task: email assessment results 2 hours after submission.
    results_email_task = asyncio.create_task(results_email_worker())

    yield

    # Shutdown
    results_email_task.cancel()
    try:
        await results_email_task
    except asyncio.CancelledError:
        pass
    logger.info("Shutting down N.O.U Digital Systems API...")


# API documentation is only exposed in development. In production the
# OpenAPI surface is hidden from unauthenticated visitors. (M4)
_docs_enabled = settings.ENVIRONMENT == "development"

# Create FastAPI application
app = FastAPI(
    title="N.O.U Digital Systems API",
    description="Centralized web platform for N.O.U. Digital Systems",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs" if _docs_enabled else None,
    redoc_url="/api/redoc" if _docs_enabled else None,
    openapi_url="/api/openapi.json" if _docs_enabled else None,
)

# CORS middleware - explicit method allow-list (fixed origins, credentials on)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.middleware("http")
async def same_origin_redirects(request: Request, call_next):
    """
    Keep redirect responses same-origin for the browser.

    When the frontend calls a bare collection path (e.g. GET
    /api/v1/assessments) Starlette answers with a 307 to the trailing-slash
    variant. Because the dev proxy rewrites the Host header (changeOrigin),
    Starlette builds an absolute Location pointing straight at the backend
    (:8000) - a cross-origin jump that the browser's CSP
    (connect-src 'self') blocks instantly, so the page shows an eternal
    spinner/error while curl works fine. Rewriting the Location to a
    relative path keeps the redirect inside the frontend origin, so it is
    followed through the proxy again (same-origin, CSP-legal).
    """
    response = await call_next(request)
    if response.status_code in (301, 302, 303, 307, 308):
        location = response.headers.get("location")
        if location:
            for backend_host in ("http://localhost:8000", "http://127.0.0.1:8000"):
                if location.startswith(backend_host):
                    response.headers["location"] = location[len(backend_host):]
                    break
    return response


# ---------------------------------------------------------------------------
# DDoS / abuse hardening (pentest pass)
# ---------------------------------------------------------------------------
MAX_JSON_BODY = 10 * 1024 * 1024      # default cap for JSON / form bodies
MAX_UPLOAD_BODY = 350 * 1024 * 1024   # uploads: releases, APK, specs, CVs
_UPLOAD_PATH_MARKERS = (
    "release", "/apps", "project", "product", "employment", "/cv", "assessments",
)
API_RATE_MAX = 300        # requests per minute per IP against the API
API_RATE_WINDOW = 60      # seconds

# Visit recording throttle: at most one DB write per IP per interval so a
# traffic flood cannot turn into a database-write flood (amplification).
_VISIT_MIN_INTERVAL = 60
_visit_last: dict = {}
_visit_lock = threading.Lock()


def _visit_throttle_ok(ip: str | None) -> bool:
    key = ip or "unknown"
    now = time.monotonic()
    with _visit_lock:
        last = _visit_last.get(key, 0)
        if now - last < _VISIT_MIN_INTERVAL:
            return False
        _visit_last[key] = now
        if len(_visit_last) > 10000:  # bounded memory under floods
            _visit_last.clear()
        return True


def _body_cap_for(path: str) -> int:
    lower = path.lower()
    if any(marker in lower for marker in _UPLOAD_PATH_MARKERS):
        return MAX_UPLOAD_BODY
    return MAX_JSON_BODY


# Paths that should not be counted as site visits (API calls, static
# assets, health checks, service-worker/config files).
_STATIC_SUFFIXES = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".css", ".js", ".ico", ".woff", ".woff2", ".ttf", ".map", ".webmanifest", ".txt", ".json")
_SKIPPED_PREFIXES = ("/api/", "/assets/", "/uploads/", "/static/", "/docs", "/redoc", "/openapi.json")
_SKIPPED_PATHS = {"/", "/health", "/favicon.ico", "/vite.svg", "/grid.svg", "/banner.png", "/manifest.webmanifest", "/sw.js", "/robots.txt", "/sitemap.xml"}


def _should_track_visit(path: str) -> bool:
    """Only real page views count as visits (GET on HTML routes)."""
    if not path or path in _SKIPPED_PATHS:
        return False
    if path.startswith(_SKIPPED_PREFIXES):
        return False
    if path.lower().endswith(_STATIC_SUFFIXES):
        return False
    return True


async def _record_visit(path: str, ip: str | None, user_agent: str | None) -> None:
    """Persist one page view. Runs in a background task so a slow database
    can never delay a page response; failures are swallowed silently."""
    try:
        from app.models.visit_log import SiteVisit
        from app.core.database import async_session_factory
        from datetime import date
        async with async_session_factory() as db:
            db.add(SiteVisit(
                visit_date=date.today(),
                path=path[:255],
                ip=ip,
                user_agent=(user_agent or "")[:255],
            ))
            await db.commit()
    except Exception:  # noqa: BLE001 - analytics must never break the site
        logger.debug("visit recording failed for %s", path)


@app.middleware("http")
async def track_site_visits(request: Request, call_next):
    """Count every public page view for the admin daily-visits report.
    Throttled per IP so a DDoS cannot flood the analytics table."""
    response = await call_next(request)
    if request.method == "GET" and response.status_code < 400:
        path = request.url.path
        if _should_track_visit(path):
            ip = request.client.host if request.client else None
            if _visit_throttle_ok(ip):
                ua = request.headers.get("user-agent")
                asyncio.create_task(_record_visit(path, ip, ua))
    return response


@app.middleware("http")
async def ddos_guards(request: Request, call_next):
    """
    L7 DDoS / abuse brakes applied to every request:
    1. Reject oversized request bodies early (memory-exhaustion guard).
    2. Global per-IP sliding-window rate limit on the API.
    3. Never cache API responses (no shared-cache data leakage).
    """
    # 1) Body-size cap - reject before the body is read into memory.
    content_length = request.headers.get("content-length")
    if content_length and content_length.isdigit():
        cap = _body_cap_for(request.url.path)
        if int(content_length) > cap:
            return JSONResponse(
                status_code=413,
                content={"error": True, "message": "Request body too large", "status_code": 413},
            )

    # 2) Global per-IP rate limit on the API (generous ceiling for legit
    #    traffic, hard brake against floods).
    if request.url.path.startswith("/api/") and request.method != "OPTIONS":
        ip = request.client.host if request.client else "unknown"
        if not allow_request(ip, "global-api", API_RATE_MAX, API_RATE_WINDOW):
            return JSONResponse(
                status_code=429,
                content={
                    "error": True,
                    "message": "Too many requests. Please try again later.",
                    "status_code": 429,
                },
                headers={"Retry-After": str(API_RATE_WINDOW), "Cache-Control": "no-store"},
            )

    response = await call_next(request)

    # 3) No shared-cache storing of API responses (user data, tokens, etc.).
    if request.url.path.startswith("/api/"):
        response.headers.setdefault("Cache-Control", "no-store")
    return response


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    Middleware to add processing time header to responses.
    Only added in development - it leaks internal timing in production. (L5)
    """
    start_time = time.time()
    response = await call_next(request)
    if settings.ENVIRONMENT == "development":
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
    return response


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """
    Middleware setting security hardening headers on every response. (M1)
    """
    response = await call_next(request)
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com data:; "
        "img-src 'self' data: blob:; "
        "connect-src 'self' ws: wss:; "
        "frame-ancestors 'none'"
    )
    if settings.ENVIRONMENT != "development":
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
    response.headers["Permissions-Policy"] = (
        "camera=(), microphone=(), geolocation=(), payment=()"
    )
    return response


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Custom HTTP exception handler.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code
        },
        headers=exc.headers,
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    General exception handler for unhandled exceptions.
    """
    # Log the exception without stringifying it directly - str(exc) can itself
    # raise (e.g. DetachedInstanceError when repr-ing ORM instances whose
    # session is already closed), which would mask the real error.
    logger.opt(exception=exc).error("Unhandled exception")
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error",
            "status_code": 500
        }
    )


# Include API routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(products.router, prefix="/api/v1/products", tags=["Products"])
app.include_router(customers.router, prefix="/api/v1/customers", tags=["Customers"])
app.include_router(employment.router, prefix="/api/v1/employment", tags=["Employment"])
app.include_router(personnel.router, prefix="/api/v1/personnel", tags=["Personnel"])
app.include_router(assessments.router, prefix="/api/v1/assessments", tags=["Assessments"])
app.include_router(support.router, prefix="/api/v1/support", tags=["Support"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Administration"])
app.include_router(projects.router, prefix="/api/v1", tags=["Projects"])
app.include_router(investors.router, prefix="/api/v1/investors", tags=["Investors"])
app.include_router(projects_portal.router, prefix="/api/v1/portal", tags=["Projects Portal"])
app.include_router(project_lifecycle.portal_router, prefix="/api/v1/portal", tags=["Project Lifecycle"])
app.include_router(project_lifecycle.admin_router, prefix="/api/v1/admin", tags=["Project Lifecycle Admin"])
app.include_router(nou_lite.router, prefix="/api/v1/nou-lite", tags=["N.O.U Lite"])
app.include_router(announcements.router, prefix="/api/v1/announcements", tags=["Announcements"])
app.include_router(community.router, prefix="/api/v1/community", tags=["Community"])
app.include_router(payments.router, prefix="/api/v1", tags=["Payments"])
app.include_router(apps.router, prefix="/api/v1", tags=["Mobile Apps"])
app.include_router(complaints.router, prefix="/api/v1/complaints", tags=["Complaints"])
app.include_router(policies.router, prefix="/api/v1/policies", tags=["Policies"])


@app.get("/", tags=["Health"])
async def root():
    """
    Health check endpoint.
    """
    return {
        "message": "N.O.U Digital Systems API",
        "version": "1.0.0",
        "status": "healthy"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Detailed health check endpoint.
    """
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )