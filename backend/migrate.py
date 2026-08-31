"""
N.O.U Digital Systems - database migration runner (sync version).
Idempotent: checks each column/table via information_schema.
Usage (from backend/): python migrate.py
"""

import os
import sys
from urllib.parse import quote_plus
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ArgumentError
from dotenv import load_dotenv

# Load environment variables from .env in the current directory
load_dotenv()

raw_url = os.getenv("DATABASE_URL")
print(f"Raw value from os.getenv: {repr(raw_url)}")

if not raw_url:
    raise ValueError("DATABASE_URL not set in .env")

# ---- CLEANUP ----
# Remove any leading/trailing whitespace
raw_url = raw_url.strip()

# If the value starts with "DATABASE_URL=" (misformatted .env), strip that prefix
if raw_url.startswith("DATABASE_URL="):
    raw_url = raw_url[len("DATABASE_URL="):]
    print(f"Stripped prefix: {repr(raw_url)}")

# Remove surrounding quotes if any (e.g., 'mysql...' or "mysql...")
if raw_url.startswith(("'", '"')) and raw_url.endswith(("'", '"')):
    raw_url = raw_url[1:-1]
    print(f"Stripped quotes: {repr(raw_url)}")

DATABASE_URL = raw_url
print(f"Cleaned DATABASE_URL: {repr(DATABASE_URL)}")

# Ensure we use pymysql driver
if DATABASE_URL.startswith("mysql://"):
    DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)
elif DATABASE_URL.startswith("mysql+mysqldb://"):
    DATABASE_URL = DATABASE_URL.replace("mysql+mysqldb://", "mysql+pymysql://", 1)

# ---- URL‑encoding (only if needed) ----
# Quick check: if the URL contains "@" and "://", we can safely assume it's valid
# We'll only encode if parsing fails later.

# Create engine with SSL configuration
connect_args = {
    "ssl": {"ca": "/etc/ssl/certs/ca-certificates.crt"}  # for Render; adjust for Windows
}
# On Windows, this file may not exist – you can remove connect_args or use {}.

try:
    engine = create_engine(
        DATABASE_URL,
        connect_args=connect_args,
        pool_pre_ping=True,
        pool_recycle=1800,
    )
except ArgumentError as e:
    print(f"ERROR: Could not parse SQLAlchemy URL: {e}")
    print(f"Problematic URL string: {repr(DATABASE_URL)}")
    print("Attempting to manually encode user and password...")
    # Manual encoding: split at '@' and encode user:pass part
    if "@" in DATABASE_URL:
        prefix, rest = DATABASE_URL.split("@", 1)
        # prefix is like "mysql+pymysql://user:pass"
        if "://" in prefix:
            scheme, user_pass = prefix.split("://", 1)
        else:
            scheme = "mysql+pymysql"
            user_pass = prefix
        if ":" in user_pass:
            user, password = user_pass.split(":", 1)
        else:
            user = user_pass
            password = ""
        user_enc = quote_plus(user)
        pass_enc = quote_plus(password)
        new_url = f"{scheme}://{user_enc}:{pass_enc}@{rest}"
        print(f"Rebuilt URL: {repr(new_url)}")
        DATABASE_URL = new_url
        # Try again
        try:
            engine = create_engine(
                DATABASE_URL,
                connect_args=connect_args,
                pool_pre_ping=True,
                pool_recycle=1800,
            )
        except Exception as e2:
            print(f"Still failing: {e2}")
            sys.exit(1)
    else:
        print("Could not fix URL – no '@' found.")
        sys.exit(1)

# ------------------------------------------------------------------
# Column additions – (table, column, column DDL)
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
    ("users", "policies_accepted_at", "DATETIME NULL"),
    ("users", "username", "VARCHAR(30) NULL"),
    ("users", "qualification_category_id", "INT NULL"),
    ("users", "qualification_position_id", "INT NULL"),
    ("users", "qualification_category_name", "VARCHAR(120) NULL"),
    ("users", "qualification_position_name", "VARCHAR(120) NULL"),
    ("users", "phone", "VARCHAR(30) NULL"),
    ("users", "cv_file_path", "VARCHAR(500) NULL"),
    ("users", "cv_summary", "TEXT NULL"),
    ("applications", "category_id", "INT NULL"),
    ("applications", "position_id", "INT NULL"),
    ("applications", "category_name", "VARCHAR(120) NULL"),
    ("applications", "position_name", "VARCHAR(120) NULL"),
    ("applications", "phone", "VARCHAR(30) NULL"),
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
    ("project_requests", "request_number", "VARCHAR(30) NULL"),
    ("project_requests", "status", "VARCHAR(40) NOT NULL DEFAULT 'submitted'"),
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
    ("assessment_sessions", "category_id", "INT NULL"),
    ("assessment_sessions", "position_id", "INT NULL"),
    ("assessment_sessions", "category_name", "VARCHAR(120) NULL"),
    ("assessment_sessions", "position_name", "VARCHAR(120) NULL"),
    ("assessment_sessions", "part_scores", "TEXT NULL"),
    ("assessment_sessions", "competency_band", "VARCHAR(30) NULL"),
    ("assessment_sessions", "recommended_category", "VARCHAR(120) NULL"),
    ("assessment_session_questions", "part", "VARCHAR(30) DEFAULT 'position'"),
    ("assessment_session_questions", "question_type", "VARCHAR(30) DEFAULT 'written_explanation'"),
    ("community_posts", "department", "VARCHAR(120) NULL"),
    ("community_posts", "guest_name", "VARCHAR(120) NULL"),
    ("community_posts", "guest_email", "VARCHAR(255) NULL"),
    ("nou_lite_orders", "guest_email", "VARCHAR(255) NULL"),
    ("company_projects", "lifecycle_stage", "VARCHAR(40) DEFAULT 'requested'"),
    ("project_documents", "doc_status", "VARCHAR(30) DEFAULT 'draft'"),
    ("project_documents", "version", "INT DEFAULT 1"),
    ("project_documents", "reviewer_notes", "TEXT NULL"),
    ("project_documents", "reviewed_by", "INT NULL"),
    ("project_documents", "reviewed_at", "DATETIME NULL"),
]

# Modifications (ALTER MODIFY) – (table, column, new DDL)
COLUMN_MODIFIES = [
    ("project_payments", "project_request_id", "INT NULL"),
    ("nou_lite_orders", "customer_id", "INT NULL"),
    ("community_posts", "author_id", "INT NULL"),
]

# Tables that the ORM auto‑creates – just for reporting
EXPECTED_TABLES = [
    "company_projects", "project_members", "project_documents",
    "project_chat_messages", "extra_developer_requests", "project_progress_reports",
    "project_help_requests", "project_deadline_extensions", "announcements",
    "nou_lite_orders", "ai_key_usage", "project_requests", "project_payments",
    "project_releases", "community_posts", "personnel_categories",
    "personnel_positions", "staffing_plan_items", "expression_of_interests",
    "project_change_requests", "site_policies",
]

# ------------------------------------------------------------------
def table_exists(conn, table: str) -> bool:
    result = conn.execute(
        text("SELECT COUNT(*) FROM information_schema.TABLES "
             "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = :t"),
        {"t": table}
    )
    return result.scalar() > 0

def column_exists(conn, table: str, column: str) -> bool:
    result = conn.execute(
        text("SELECT COUNT(*) FROM information_schema.COLUMNS "
             "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = :t AND COLUMN_NAME = :c"),
        {"t": table, "c": column}
    )
    return result.scalar() > 0

def run():
    print("N.O.U database migration (idempotent, sync version)\n")
    with engine.begin() as conn:
        # 1. Add columns
        for table, column, ddl in COLUMN_ALTERS:
            if not table_exists(conn, table):
                print(f"  [warn] table {table} missing - will be created by the ORM at startup")
                continue
            if column_exists(conn, table, column):
                print(f"  [skip] {table}.{column} (already exists)")
                continue
            conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {ddl}"))
            print(f"  [added] {table}.{column}")

        # 2. Modify columns (nullability / type)
        for table, column, ddl in COLUMN_MODIFIES:
            if not table_exists(conn, table):
                print(f"  [warn] table {table} missing - will be created by the ORM at startup")
                continue
            if not column_exists(conn, table, column):
                print(f"  [warn] {table}.{column} missing - skipped (add via COLUMN_ALTERS)")
                continue
            conn.execute(text(f"ALTER TABLE {table} MODIFY COLUMN {column} {ddl}"))
            print(f"  [modified] {table}.{column} -> {ddl}")

        # 3. Report expected tables
        print()
        for table in EXPECTED_TABLES:
            exists = table_exists(conn, table)
            print(f"  [{'ok' if exists else 'absent'}] {table}"
                  + ("" if exists else " (ORM creates at next startup)"))

    print("\nDone. Columns added; missing tables are auto-created when the backend starts.")

if __name__ == "__main__":
    run()