import secrets

import pytest
from pydantic import ValidationError

from app.config import Settings


def test_settings_development_default():
    s = Settings(ENVIRONMENT="development")
    assert s.APP_NAME == "AegisAudit"
    assert s.MOCK_ENGINE is True
    assert s.JWT_ACCESS_TOKEN_EXPIRE_MINUTES == 30
    assert s.ACCESS_TOKEN_EXPIRE_MINUTES == 30
    assert s.MAX_JOB_RUNTIME_SECONDS == 1800
    assert s.JOB_TIMEOUT_SECONDS == 1800
    assert len(s.cors_origins_list) >= 1


def test_settings_production_refuses_default_secret():
    with pytest.raises(ValidationError) as exc_info:
        Settings(
            ENVIRONMENT="production",
            JWT_SECRET="CHANGE_ME_FOR_LOCAL_DEVELOPMENT_SECRET_KEY_32_CHARS_MIN",
        )
    assert "FATAL SECURITY BARRIER" in str(exc_info.value)


def test_settings_production_refuses_short_secret():
    with pytest.raises(ValidationError) as exc_info:
        Settings(ENVIRONMENT="production", JWT_SECRET="short_insecure_key")
    assert "FATAL SECURITY BARRIER" in str(exc_info.value)


def test_settings_production_accepts_secure_secret():
    secure_key = secrets.token_urlsafe(64)
    s = Settings(ENVIRONMENT="production", JWT_SECRET=secure_key)
    assert s.ENVIRONMENT == "production"
    assert s.JWT_SECRET == secure_key
