from typing import List, Optional

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration and typed environment settings."""

    # 1. Application Settings
    APP_NAME: str = "AegisAudit"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    # 2. Database & Redis Settings
    DATABASE_URL: str = "sqlite:///./aegisaudit.db"
    REDIS_URL: str = "redis://redis:6379/0"

    # 3. Security & Authentication Settings
    JWT_SECRET: str = "CHANGE_ME_FOR_LOCAL_DEVELOPMENT_SECRET_KEY_32_CHARS_MIN"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: Optional[int] = None
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000"

    # 4. Security Engine Settings
    MOCK_ENGINE: bool = True
    HASHCAT_PATH: str = "/usr/bin/hashcat"
    JOHN_PATH: str = "/usr/sbin/john"
    HYDRA_PATH: str = "/usr/bin/hydra"
    WORDLIST_PATH: str = "/usr/share/wordlists/rockyou.txt"

    # 5. Resource Constraints & Limits
    MAX_CONCURRENT_JOBS: int = 2
    JOB_TIMEOUT_SECONDS: int = 1800
    MAX_JOB_RUNTIME_SECONDS: Optional[int] = None
    MAX_WORDLIST_SIZE_MB: int = 1024

    # 6. Frontend Integration
    VITE_API_URL: str = "http://localhost:8000"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @model_validator(mode="after")
    def validate_and_sync(self) -> "Settings":
        """Synchronize aliases and enforce strict production security barriers."""
        # Synchronize token expiry settings
        if self.JWT_ACCESS_TOKEN_EXPIRE_MINUTES is None:
            self.JWT_ACCESS_TOKEN_EXPIRE_MINUTES = self.ACCESS_TOKEN_EXPIRE_MINUTES
        else:
            self.ACCESS_TOKEN_EXPIRE_MINUTES = self.JWT_ACCESS_TOKEN_EXPIRE_MINUTES

        # Synchronize job timeout settings
        if self.MAX_JOB_RUNTIME_SECONDS is None:
            self.MAX_JOB_RUNTIME_SECONDS = self.JOB_TIMEOUT_SECONDS
        else:
            self.JOB_TIMEOUT_SECONDS = self.MAX_JOB_RUNTIME_SECONDS

        # Refuse to start in production if JWT_SECRET is default or contains CHANGE_ME
        if self.ENVIRONMENT.lower() == "production":
            insecure_markers = [
                "change_me",
                "secret_key_32_chars_min",
                "changeme",
            ]
            secret_lower = self.JWT_SECRET.lower()
            if (
                not self.JWT_SECRET
                or len(self.JWT_SECRET) < 32
                or any(marker in secret_lower for marker in insecure_markers)
            ):
                raise ValueError(
                    "FATAL SECURITY BARRIER: AegisAudit refuses to start in ENVIRONMENT=production "
                    "with default, insecure, or placeholder JWT_SECRET. "
                    "Generate a cryptographically secure key with: "
                    "python -c 'import secrets; print(secrets.token_urlsafe(64))'"
                )

        return self

    @property
    def cors_origins_list(self) -> List[str]:
        """Return parsed list of authorized CORS origins."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


settings = Settings()
