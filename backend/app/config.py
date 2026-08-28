from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "AegisAudit"
    ENVIRONMENT: str = "development"

    # Database & Redis
    DATABASE_URL: str = "sqlite:///./aegisaudit.db"
    REDIS_URL: str = "redis://localhost:6379/0"

    # Security & Auth
    JWT_SECRET: str = "CHANGE_ME_FOR_LOCAL_DEVELOPMENT_SECRET_KEY_32_CHARS_MIN"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Security Engine Execution
    MOCK_ENGINE: bool = True

    # Resource Constraints
    MAX_CONCURRENT_JOBS: int = 2
    MAX_JOB_RUNTIME_SECONDS: int = 1800
    MAX_WORDLIST_SIZE_MB: int = 1024

    # Logging
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
