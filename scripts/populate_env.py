#!/usr/bin/env python3
"""
Populate N.O.U environment files (.env) for local development.

- Reads SMTP credentials from YourGallery/yourgallery/.env (source of truth)
- Generates a fresh SECRET_KEY
- Writes N.O.U/backend/.env and N.O.U/frontend/.env
- Does NOT print secret values to stdout
"""
import os
import secrets
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # N.O.U/
YOURGALLERY_ENV = ROOT.parent / "YourGallery" / "yourgallery" / ".env"
BACKEND_ENV = ROOT / "backend" / ".env"
BACKEND_ENV_EXAMPLE = ROOT / "backend" / ".env.example"
FRONTEND_ENV = ROOT / "frontend" / ".env"
FRONTEND_ENV_EXAMPLE = ROOT / "frontend" / ".env.example"


def parse_env(path: Path) -> dict:
    """Parse a simple KEY=VALUE env file (ignores comments/blank lines)."""
    result = {}
    if not path.exists():
        return result
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        result[key.strip()] = value.strip()
    return result


def write_env(path: Path, values: dict, comments: dict | None = None):
    """Write values to env file in deterministic order with optional comments."""
    comments = comments or {}
    lines = []
    for key, value in values.items():
        if key in comments:
            lines.append(f"# {comments[key]}")
        lines.append(f"{key}={value}")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  wrote {path.relative_to(ROOT.parent)} ({len(values)} keys)")


def main():
    print("N.O.U environment setup")
    print("========================")

    yourgallery = parse_env(YOURGALLERY_ENV)
    if not yourgallery:
        print(f"ERROR: could not read {YOURGALLERY_ENV}")
        sys.exit(1)

    smtp_user = yourgallery.get("SMTP_USER", "")
    smtp_pass = yourgallery.get("SMTP_PASS", "")
    if not smtp_user or not smtp_pass:
        print("ERROR: SMTP_USER/SMTP_PASS missing from YourGallery .env")
        sys.exit(1)

    # ---- Backend .env ----
    example = parse_env(BACKEND_ENV_EXAMPLE)
    secret_key = secrets.token_urlsafe(48)

    backend_values = {
        "APP_NAME": example.get("APP_NAME", "N.O.U Digital Systems"),
        "APP_VERSION": example.get("APP_VERSION", "1.0.0"),
        "ENVIRONMENT": "development",
        "DEBUG": "true",
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "DATABASE_URL": "mysql+aiomysql://root:Eric%40254.J@localhost:3306/nou_database",
        "DATABASE_ECHO": "false",
        "SECRET_KEY": secret_key,
        "ALGORITHM": "HS256",
        "ACCESS_TOKEN_EXPIRE_MINUTES": "30",
        "REFRESH_TOKEN_EXPIRE_DAYS": "7",
        "CORS_ORIGINS": "http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173",
        "UPLOAD_DIR": "uploads",
        "MAX_FILE_SIZE": "10485760",
        "SMTP_HOST": yourgallery.get("SMTP_HOST", "smtp.gmail.com"),
        "SMTP_PORT": yourgallery.get("SMTP_PORT", "587"),
        "SMTP_USER": smtp_user,
        "SMTP_PASSWORD": smtp_pass,
        "EMAILS_FROM_EMAIL": yourgallery.get("SMTP_FROM_EMAIL", smtp_user),
        "EMAILS_FROM_NAME": "N.O.U Digital Systems",
        "LOG_LEVEL": "INFO",
        "LOG_FILE": "logs/app.log",
    }
    backend_comments = {
        "DATABASE_URL": "MySQL (aiomysql) - root / local MySQL instance",
        "SMTP_HOST": "SMTP credentials inherited from YourGallery/.env",
        "EMAILS_FROM_NAME": "Optional Redis: REDIS_URL=redis://localhost:6379",
    }
    write_env(BACKEND_ENV, backend_values, backend_comments)

    # ---- Frontend .env ----
    frontend_example = parse_env(FRONTEND_ENV_EXAMPLE)
    frontend_values = {
        "VITE_API_BASE_URL": "http://localhost:8000/api",
        "VITE_APP_NAME": "N.O.U Digital Systems",
        "VITE_APP_VERSION": "1.0.0",
        "VITE_ENABLE_ANALYTICS": frontend_example.get("VITE_ENABLE_ANALYTICS", "false"),
        "VITE_ENABLE_MAINTENANCE_MODE": "false",
        "VITE_GOOGLE_ANALYTICS_ID": "",
        "VITE_SENTRY_DSN": "",
    }
    write_env(FRONTEND_ENV, frontend_values)

    print()
    print("Done. Secrets written to .env files (values not echoed).")
    print(f"  SMTP user : {smtp_user}")
    print(f"  DB        : nou_database @ localhost:3306")


if __name__ == "__main__":
    main()
