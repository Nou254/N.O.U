"""
Application configuration settings.
"""

from pydantic import field_validator
from pydantic_settings import BaseSettings
from pydantic_settings.sources import DotEnvSettingsSource
from typing import List, Optional, Any


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
    # Debug is enabled explicitly via .env for local development only; the
    # default is safe for production. (Pentest finding L5)
    DEBUG: bool = False
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database - REQUIRED from .env (never hardcoded - pentest finding).
    # Use 127.0.0.1 (not localhost) to avoid Windows IPv6 (::1) resolution
    # hangs with aiomysql. Example:
    #   DATABASE_URL=mysql+aiomysql://root:password@127.0.0.1:3306/nou_database
    DATABASE_URL: str
    DATABASE_ECHO: bool = False

    # Security - REQUIRED from .env (a strong random secret, 32+ chars -
    # pentest finding: previously had a known public default value).
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    # Admin bootstrap credentials - used ONLY by seed_admin.py and
    # cleanup_database.py (never hardcoded in source - pentest finding).
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
    # Software releases (.apk/.zip/.exe/...) are much larger than documents.
    MAX_RELEASE_SIZE: int = 300 * 1024 * 1024  # 300MB
    # Extensions allowed for customer software downloads (validated by name,
    # since browsers report inconsistent MIME types for binaries).
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
    
    # Redis (optional - for caching)
    REDIS_URL: Optional[str] = None

    # AI Assessment (Groq)
    # Get a free API key at https://console.groq.com/keys
    GROQ_API_KEY: Optional[str] = None
    GROQ_API_KEYS: List[str] = []
    # Per-feature key pools (comma-separated in .env, see groq_apis.md which
    # was moved into .env). Each AI section draws from its own pool so one
    # feature cannot exhaust another's quota.
    GROQ_ASSESSMENT_KEYS: List[str] = []   # question generation + grading
    GROQ_CHATBOT_KEYS: List[str] = []      # N.O.U Lite customer assistant
    GROQ_COMMUNITY_KEYS: List[str] = []    # project chat / community AI
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    GROQ_TIMEOUT: int = 120

    # Groq key pool rules: each AI section gets KEYS_PER_SECTION keys per day;
    # if a section exhausts them, it is topped up with KEYS_TOP_UP more.
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

    # ------------------------------------------------------------------
    # Payments - M-Pesa Daraja C2B (Kenya) + Flutterwave (cards)
    # Leave the keys empty to run in SIMULATION mode (records the payment as
    # pending without contacting the provider). Fill them in backend/.env
    # when the credentials are ready.
    # ------------------------------------------------------------------
    MPESA_CONSUMER_KEY: Optional[str] = None
    MPESA_CONSUMER_SECRET: Optional[str] = None
    MPESA_SHORTCODE: Optional[str] = None          # paybill/till number
    MPESA_PASSKEY: Optional[str] = None            # Daraja lipa-na-mpesa passkey
    MPESA_ENV: str = "sandbox"                    # sandbox | live
    # Public base URL used to build the C2B callback/validation URLs that
    # Safaricom calls (e.g. https://api.yourdomain.com). In local dev the
    # sandbox dashboard can be pointed at a tunnelled URL.
    MPESA_CALLBACK_BASE_URL: Optional[str] = None

    FLUTTERWAVE_SECRET_KEY: Optional[str] = None
    FLUTTERWAVE_PUBLIC_KEY: Optional[str] = None
    FLUTTERWAVE_WEBHOOK_SECRET_HASH: Optional[str] = None
    # Base URL of the site (used for Flutterwave redirect_url + hosted page).
    FRONTEND_BASE_URL: str = "http://localhost:3000"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Create settings instance
settings = Settings()


def get_settings() -> Settings:
    """
    Get application settings.
    """
    return settings