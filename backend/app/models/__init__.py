"""
Model package.

Imports every model module so that all tables and string-based relationships
are registered on Base.metadata before the first database query runs.
"""

from app.models import (  # noqa: F401
    ai_key_usage,
    announcement,
    application,
    complaint,
    assessment,
    company_project,
    customer,
    investor,
    job,
    mobile_app,
    nou_lite_order,
    personnel,
    product,
    project_lifecycle,
    project_progress,
    project_release,
    project_request,
    question,
    site_policy,
    support,
    user,
    visit_log,
)
