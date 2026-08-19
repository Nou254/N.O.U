#!/usr/bin/env python3
"""
Production startup script for N.O.U Digital Systems backend.
Runs migrations, seeds admin, and starts the server.
"""

import os
import sys
import subprocess
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("startup")

def main():
    logger.info("Starting N.O.U Digital Systems backend...")
    
    # Ensure we're in the backend directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Run migrations
    logger.info("Running database migrations...")
    try:
        subprocess.run([sys.executable, "migrate.py"], check=True)
        logger.info("Migrations completed successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"Migration failed: {e}")
        # Continue anyway - tables may already exist
    
    # Seed admin if needed
    logger.info("Checking admin seed...")
    try:
        subprocess.run([sys.executable, "seed_admin.py"], check=True)
        logger.info("Admin seed completed")
    except subprocess.CalledProcessError as e:
        logger.warning(f"Admin seed skipped or failed: {e}")
    
    # Start uvicorn
    logger.info("Starting uvicorn server...")
    port = int(os.environ.get("PORT", 8000))
    os.execvp("uvicorn", [
        "uvicorn",
        "app.main:app",
        "--host", "0.0.0.0",
        "--port", str(port),
        "--workers", "1",
        "--log-level", "info"
    ])

if __name__ == "__main__":
    main()
