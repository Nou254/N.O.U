"""
N.O.U Digital Systems - database migration runner.

The ORM auto-creates *missing tables* at startup, but it never alters an
existing table. This script applies the ALTERs needed after the 2026-08-07
feature build (investor questions, onboarding fields, key pool) in an
idempotent way: every column/table is checked against information_schema
first, so it is safe to re-run any number of times.

Usage (from backend/):
    python migrate.py

It prints what it did:
    [skip]  investor_interests.monthly_investment (already exists)
    [added] investor_interests.joining_fee_paid
"""

import asyncio

from sqlalchemy import text

from app.core.database import engine


# (table, column, column DDL) - columns added to existing tables.
COLUMN_ALTERS = [
    ("investor_interests", "monthly_investment", "DECIMAL(14,2) NULL"),
    ("investor_interests", "expectations", "TEXT NULL"),
    ("investor_interests", "risk_knowledge", "VARCHAR(50) NULL"),
    ("investor_interests", "joining_fee_paid", "TINYINT(1) DEFAULT 0"),
    ("investor_interests", "joining_fee_paid_at", "DATETIME NULL"),
    ("investor_interests", "joining_fee_amount", "DECIMAL(10,2) DEFAULT 500"),
    ("assessment_sessions", "onboarding_status", "VARCHAR(20) DEFAULT 'pending'"),
    ("assessment_sessions", "onboarding_decided_at", "DATETIME NULL"),
    ("assessment_sessions", "onboarding_notes", "TEXT NULL"),
    ("users", "is_active", "TINYINT(1) DEFAULT 1"),
    ("users", "terms_accepted_at", "DATETIME NULL"),
    # Organization policies agreement (approved personnel first login).
    ("users", "policies_accepted_at", "DATETIME NULL"),
    # Developer handles (@username) + applicant's place of qualification.
    ("users", "username", "VARCHAR(30) NULL"),
    ("users", "qualification_category_id", "INT NULL"),
    ("users", "qualification_position_id", "INT NULL"),
    ("users", "qualification_category_name", "VARCHAR(120) NULL"),
    ("users", "qualification_position_name", "VARCHAR(120) NULL"),
    # Applicant contact details + CV (public apply form + assessment page).
    ("users", "phone", "VARCHAR(30) NULL"),
    ("users", "cv_file_path", "VARCHAR(500) NULL"),
    # Groq-generated CV review summary (admin HR screens).
    ("users", "cv_summary", "TEXT NULL"),
    ("applications", "category_id", "INT NULL"),
    ("applications", "position_id", "INT NULL"),
    ("applications", "category_name", "VARCHAR(120) NULL"),
    ("applications", "position_name", "VARCHAR(120) NULL"),
    ("applications", "phone", "VARCHAR(30) NULL"),
    # Company projects: gallery section + admin-graded weekly progress.
    ("products", "status", "VARCHAR(30) NOT NULL DEFAULT 'Available'"),
    ("products", "platforms", "VARCHAR(200) NOT NULL DEFAULT 'Web'"),
    ("products", "licence", "VARCHAR(200) NULL"),
    ("products", "requirements", "TEXT NULL"),
    ("products", "features", "TEXT NULL"),
    ("products", "featured", "TINYINT(1) NOT NULL DEFAULT 0"),
    ("company_projects", "section", "VARCHAR(50) NULL"),
    ("company_projects", "product_status", "VARCHAR(40) NOT NULL DEFAULT 'Free'"),
    ("company_projects", "platform", "VARCHAR(60) NULL"),
    ("project_progress_reports", "admin_percentage", "DECIMAL(5,2) NULL"),
    ("project_progress_reports", "graded_by", "INT NULL"),
    ("project_progress_reports", "graded_at", "DATETIME NULL"),
    # Customer project requests: quotation/payment lifecycle (today.md).
    ("project_requests", "request_number", "VARCHAR(30) NULL"),
    ("project_requests", "status", "VARCHAR(40) NOT NULL DEFAULT 'submitted'"),
    # Technical services on customer requests (Wi-Fi/CCTV/consultancy).
    ("project_requests", "service_type", "VARCHAR(50) NOT NULL DEFAULT 'software_development'"),
    ("project_requests", "location", "VARCHAR(255) NULL"),
    ("project_requests", "quotation_amount", "DECIMAL(14,2) NULL"),
    ("project_requests", "quotation_currency", "VARCHAR(10) DEFAULT 'KSh'"),
    ("project_requests", "deposit_percent", "INT DEFAULT 30"),
    ("project_requests", "payment_schedule", "TEXT NULL"),
    ("project_requests", "scope_included", "TEXT NULL"),
    ("project_requests", "scope_excluded", "TEXT NULL"),
    ("project_requests", "quotation_version", "INT DEFAULT 1"),
    ("project_requests", "quotation_issued_at", "DATETIME NULL"),
    ("project_requests", "quotation_accepted_at", "DATETIME NULL"),
    ("project_requests", "quotation_declined_at", "DATETIME NULL"),
    ("project_requests", "admin_decision", "TEXT NULL"),
    ("project_requests", "decision_at", "DATETIME NULL"),
    ("project_requests", "agreed_amount", "DECIMAL(14,2) NULL"),
    ("project_requests", "agreed_at", "DATETIME NULL"),
    ("project_requests", "paid_amount", "DECIMAL(14,2) DEFAULT 0"),
    ("project_requests", "activated_at", "DATETIME NULL"),
    # Personnel categories/positions + 5-part assessment framework.
    ("assessment_sessions", "category_id", "INT NULL"),
    ("assessment_sessions", "position_id", "INT NULL"),
    ("assessment_sessions", "category_name", "VARCHAR(120) NULL"),
    ("assessment_sessions", "position_name", "VARCHAR(120) NULL"),
    ("assessment_sessions", "part_scores", "TEXT NULL"),
    ("assessment_sessions", "competency_band", "VARCHAR(30) NULL"),
    ("assessment_sessions", "recommended_category", "VARCHAR(120) NULL"),
    ("assessment_session_questions", "part", "VARCHAR(30) DEFAULT 'position'"),
    ("assessment_session_questions", "question_type", "VARCHAR(30) DEFAULT 'written_explanation'"),
    # Project lifecycle + staffing + document approval workflow.
    # Support contributions + department communities.
    ("community_posts", "department", "VARCHAR(120) NULL"),
    # Community chat: public visitors post with a display name + optional
    # email instead of an account (freedom of expression, admin approves).
    ("community_posts", "guest_name", "VARCHAR(120) NULL"),
    ("community_posts", "guest_email", "VARCHAR(255) NULL"),
    # Guest N.O.U Lite orders (chat without an account).
    ("nou_lite_orders", "guest_email", "VARCHAR(255) NULL"),
    ("company_projects", "lifecycle_stage", "VARCHAR(40) DEFAULT 'requested'"),
    ("project_documents", "doc_status", "VARCHAR(30) DEFAULT 'draft'"),
    ("project_documents", "version", "INT DEFAULT 1"),
    ("project_documents", "reviewer_notes", "TEXT NULL"),
    ("project_documents", "reviewed_by", "INT NULL"),
    ("project_documents", "reviewed_at", "DATETIME NULL"),
]

# (table, column, new DDL) - MODIFY existing columns (e.g. dropping NOT NULL).
COLUMN_MODIFIES = [
    # Support contributions have no project request - allow NULL.
    ("project_payments", "project_request_id", "INT NULL"),
    # Guest N.O.U Lite chat: orders may have no customer account.
    ("nou_lite_orders", "customer_id", "INT NULL"),
    # Community chat: public visitors have no user account - author_id NULL.
    ("community_posts", "author_id", "INT NULL"),
]

# (table) - tables that the ORM auto-creates at startup; reported for clarity.
EXPECTED_TABLES = [
    "company_projects",
    "project_members",
    "project_documents",
    "project_chat_messages",
    "extra_developer_requests",
    "project_progress_reports",
    "project_help_requests",
    "project_deadline_extensions",
    "announcements",
    "nou_lite_orders",
    "ai_key_usage",
    "project_requests",
    "project_payments",
    "project_releases",
    "community_posts",
    "personnel_categories",
    "personnel_positions",
    "staffing_plan_items",
    "expression_of_interests",
    "project_change_requests",
    "site_policies",
]


async def table_exists(conn, table: str) -> bool:
    row = await conn.execute(text(
        "SELECT COUNT(*) FROM information_schema.TABLES "
        "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = :t"
    ), {"t": table})
    return row.scalar() > 0


async def column_exists(conn, table: str, column: str) -> bool:
    row = await conn.execute(text(
        "SELECT COUNT(*) FROM information_schema.COLUMNS "
        "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = :t AND COLUMN_NAME = :c"
    ), {"t": table, "c": column})
    return row.scalar() > 0


async def run() -> None:
    print("N.O.U database migration (idempotent)\n")
    async with engine.begin() as conn:
        # 1. Column ALTERs on existing tables.
        for table, column, ddl in COLUMN_ALTERS:
            if not await table_exists(conn, table):
                print(f"  [warn] table {table} missing - will be created by the ORM at startup")
                continue
            if await column_exists(conn, table, column):
                print(f"  [skip] {table}.{column} (already exists)")
                continue
            await conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {ddl}"))
            print(f"  [added] {table}.{column}")

        # 1b. MODIFY existing columns (nullability / type changes).
        for table, column, ddl in COLUMN_MODIFIES:
            if not await table_exists(conn, table):
                print(f"  [warn] table {table} missing - will be created by the ORM at startup")
                continue
            if not await column_exists(conn, table, column):
                print(f"  [warn] {table}.{column} missing - skipped (add via COLUMN_ALTERS)")
                continue
            await conn.execute(text(f"ALTER TABLE {table} MODIFY COLUMN {column} {ddl}"))
            print(f"  [modified] {table}.{column} -> {ddl}")

        # 2. Expected tables - report presence (ORM creates them at startup).
        print()
        for table in EXPECTED_TABLES:
            exists = await table_exists(conn, table)
            print(f"  [{'ok' if exists else 'absent'}] {table}"
                  + ("" if exists else " (ORM creates at next startup)"))

    print("\nDone. Columns added; missing tables are auto-created when the "
          "backend starts (app.main lifespan).")


if __name__ == "__main__":
    asyncio.run(run())
