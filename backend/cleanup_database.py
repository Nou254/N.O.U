"""
N.O.U Digital Systems - database cleanup.

Clears ALL mock / seed / demo / test data so the platform starts clean, while
keeping the admin account (admin@nou.com) fully working.

Kept (configuration the admin manages):
  - personnel_categories / personnel_positions (departments & qualifications)
  - job_listings (careers page - company postings)
  - question_bank (pre-generated AI questions - assessments draw from them)

Cleared (demo/mock/test data):
  - products (all seeded mock products)
  - all users EXCEPT the admin (demo customers, applicants, developers...)
  - assessment SESSION data (sessions, answers, session questions),
    applications, orders, project requests & payments, company projects & their
    chat/progress/docs, announcements, community posts, investor interests,
    support tickets, releases, key usage, etc.

The assessments DEFINITION record (the active assessment the public
assessment page lists) is configuration - like personnel categories/positions
and job listings - so it is kept.

Safe to re-run. The admin credentials are read ONLY from the environment
(backend/.env, NOU_ADMIN_EMAIL / NOU_ADMIN_PASSWORD) so login always works
after a cleanup - never hardcoded in source (pentest finding).
"""

import asyncio
import os

from sqlalchemy import text

from app.core.database import async_session_factory
from app.core.security import get_password_hash

ADMIN_EMAIL = os.environ.get("NOU_ADMIN_EMAIL", "").strip().lower()
ADMIN_PASSWORD = os.environ.get("NOU_ADMIN_PASSWORD", "").strip()
if not ADMIN_EMAIL or not ADMIN_PASSWORD:
    raise SystemExit(
        "Missing required environment variables NOU_ADMIN_EMAIL / NOU_ADMIN_PASSWORD "
        "- set them in backend/.env before cleaning the database."
    )

# Tables with mock/demo data, in dependency-safe order (FK checks disabled
# anyway, but keep it tidy).
CLEAR_TABLES = [
    "assessment_answers",
    "assessment_session_questions",
    "assessment_sessions",
    # NOTE: the "assessments" definition record is kept (config data the
    # public assessment page depends on - like categories and job listings).
    "applications",
    "project_change_requests",
    "project_deadline_extensions",
    "project_help_requests",
    "project_progress_reports",
    "project_chat_messages",
    "project_releases",
    "project_documents",
    "extra_developer_requests",
    "staffing_plan_items",
    "project_members",
    "company_projects",
    "project_payments",
    "project_requests",
    "nou_lite_orders",
    "announcements",
    "community_posts",
    "investor_interests",
    "expression_of_interests",
    "support_tickets",
    "ai_key_usage",
    "products",
    "customers",
]


async def run() -> None:
    print("N.O.U database cleanup\n")
    async with async_session_factory() as session:
        async with session.begin():
            await session.execute(text("SET FOREIGN_KEY_CHECKS = 0"))

            # 1. Clear demo data tables.
            for table in CLEAR_TABLES:
                try:
                    result = await session.execute(text(f"DELETE FROM {table}"))
                    print(f"  [cleared] {table} ({result.rowcount} rows)")
                except Exception as exc:  # noqa: BLE001
                    print(f"  [warn] {table}: {exc}")

            # 2. Delete every user except the admin (and their profiles).
            users = await session.execute(
                text("SELECT id, email, role FROM users WHERE email != :admin"),
                {"admin": ADMIN_EMAIL},
            )
            user_ids = [row[0] for row in users.fetchall()]
            print(f"  [cleared] users ({len(user_ids)} non-admin accounts removed)")
            if user_ids:
                id_list = ",".join(str(i) for i in user_ids)
                await session.execute(text(f"DELETE FROM customers WHERE user_id IN ({id_list})"))
                await session.execute(text(f"DELETE FROM users WHERE id IN ({id_list})"))

            # 3. Ensure the admin account exists and can log in.
            admin = await session.execute(
                text("SELECT id FROM users WHERE email = :admin"),
                {"admin": ADMIN_EMAIL},
            )
            admin_id = admin.scalar()
            if admin_id is None:
                await session.execute(
                    text(
                        "INSERT INTO users (email, password_hash, first_name, last_name, role,"
                        " is_active, terms_accepted_at) VALUES (:email, :pw, 'System', 'Administrator',"
                        " 'admin', 1, NOW())"
                    ),
                    {"email": ADMIN_EMAIL, "pw": get_password_hash(ADMIN_PASSWORD)},
                )
                print(f"  [admin] created {ADMIN_EMAIL}")
            else:
                await session.execute(
                    text(
                        "UPDATE users SET password_hash = :pw, role = 'admin', is_active = 1,"
                        " terms_accepted_at = NOW(), username = NULL WHERE id = :id"
                    ),
                    {"pw": get_password_hash(ADMIN_PASSWORD), "id": admin_id},
                )
                print(f"  [admin] {ADMIN_EMAIL} password reset")

            await session.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

    print("\nDone. The platform is now clean - only the admin account remains.")


if __name__ == "__main__":
    asyncio.run(run())
