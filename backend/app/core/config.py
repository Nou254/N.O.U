"""
Application configuration settings.
"""

from pydantic import field_validator
from pydantic_settings import BaseSettings
from pydantic_settings.sources import DotEnvSettingsSource
from typing import List, Optional, Any
import re


class CommaSeparatedDotEnvSettingsSource(DotEnvSettingsSource):
    """
    Dotenv source that keeps comma-separated values as raw strings instead of
    forcing JSON decoding on complex fields (e.g. CORS_ORIGINS), matching the
    format documented in .env.example.
    """

    def decode_complex_value(self, field_name: str, field: Any, value: Any) -> Any:
        if field_name in {
            "CORS_ORIGINS",
            "GROQ_API_KEYS",
            "GROQ_ASSESSMENT_KEYS",
            "GROQ_CHATBOT_KEYS",
            "GROQ_COMMUNITY_KEYS",
        }:
            return value
        return super().decode_complex_value(field_name, field, value)


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    
    # Application
    APP_NAME: str = "N.O.U Digital Systems"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database - REQUIRED from .env.
    DATABASE_URL: str
    DATABASE_ECHO: bool = False

    # Security - REQUIRED from .env.
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    # Admin bootstrap credentials
    NOU_ADMIN_EMAIL: Optional[str] = None
    NOU_ADMIN_PASSWORD: Optional[str] = None
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def _split_cors_origins(cls, value: Any) -> Any:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        return (
            init_settings,
            env_settings,
            CommaSeparatedDotEnvSettingsSource(settings_cls),
            file_secret_settings,
        )
    
    # File Upload
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    MAX_RELEASE_SIZE: int = 300 * 1024 * 1024  # 300MB
    ALLOWED_RELEASE_EXTENSIONS: List[str] = [
        ".apk", ".aab", ".zip", ".exe", ".msi", ".dmg", ".ipa", ".jar",
        ".deb", ".rpm", ".tar.gz", ".tgz", ".7z", ".rar", ".bin",
        ".pdf", ".docx", ".doc", ".xlsx", ".pptx", ".txt", ".py",
        ".js", ".html", ".css", ".png", ".jpg", ".jpeg", ".webp",
        ".iso", ".img", ".whl", ".tar", ".gz", ".csv", ".json",
    ]
    ALLOWED_FILE_TYPES: List[str] = [
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain",
        "image/jpeg",
        "image/png",
        "image/webp"
    ]
    
    # Email (optional)
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[int] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = None
    
    # Redis (optional)
    REDIS_URL: Optional[str] = None

    # AI Assessment (Groq)
    GROQ_API_KEY: Optional[str] = None
    GROQ_API_KEYS: List[str] = []
    GROQ_ASSESSMENT_KEYS: List[str] = []
    GROQ_CHATBOT_KEYS: List[str] = []
    GROQ_COMMUNITY_KEYS: List[str] = []
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    GROQ_TIMEOUT: int = 120

    GROQ_KEYS_PER_SECTION: int = 10
    GROQ_KEYS_TOP_UP: int = 2

    @field_validator("GROQ_API_KEYS", "GROQ_ASSESSMENT_KEYS", "GROQ_CHATBOT_KEYS", "GROQ_COMMUNITY_KEYS", mode="before")
    @classmethod
    def _split_groq_keys(cls, value: Any) -> Any:
        if isinstance(value, str):
            return [k.strip() for k in value.split(",") if k.strip()]
        if value is None:
            return []
        return value

    # M-Pesa and Flutterwave
    MPESA_CONSUMER_KEY: Optional[str] = None
    MPESA_CONSUMER_SECRET: Optional[str] = None
    MPESA_SHORTCODE: Optional[str] = None
    MPESA_PASSKEY: Optional[str] = None
    MPESA_ENV: str = "sandbox"
    MPESA_CALLBACK_BASE_URL: Optional[str] = None

    FLUTTERWAVE_SECRET_KEY: Optional[str] = None
    FLUTTERWAVE_PUBLIC_KEY: Optional[str] = None
    FLUTTERWAVE_WEBHOOK_SECRET_HASH: Optional[str] = None
    FRONTEND_BASE_URL: str = "http://localhost:3000"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    # ----- DATABASE URL CLEANING (use aiomysql) -----
    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def _clean_database_url(cls, value: Any) -> str:
        if not isinstance(value, str):
            raise ValueError("DATABASE_URL must be a string")
        value = value.strip()
        if value.startswith("DATABASE_URL="):
            value = value[len("DATABASE_URL="):].strip()
        if value.startswith(("'", '"')) and value.endswith(("'", '"')):
            value = value[1:-1]

        # Remove SSL query params (we'll handle via connect_args)
        value = re.sub(r'[?&]ssl_verify_cert=[^&]*', '', value)
        value = re.sub(r'[?&]ssl_verify_identity=[^&]*', '', value)
        value = re.sub(r'\?&', '?', value)
        value = re.sub(r'&$', '', value)
        if value.endswith('?'):
            value = value[:-1]

        # ---- Switch to aiomysql (more stable on Windows) ----
        if value.startswith("mysql+pymysql://"):
            value = value.replace("mysql+pymysql://", "mysql+aiomysql://", 1)
        elif value.startswith("mysql+mysqldb://"):
            value = value.replace("mysql+mysqldb://", "mysql+aiomysql://", 1)
        elif value.startswith("mysql://"):
            value = value.replace("mysql://", "mysql+aiomysql://", 1)
        elif value.startswith("mysql+asyncmy://"):
            value = value.replace("mysql+asyncmy://", "mysql+aiomysql://", 1)

        # Ensure charset
        if "charset=utf8mb4" not in value:
            if "?" in value:
                value += "&charset=utf8mb4"
            else:
                value += "?charset=utf8mb4"

        return value
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Create the settings instance
settings = Settings()


def get_settings() -> Settings:
    """
    Get application settings.
    """
    return settings