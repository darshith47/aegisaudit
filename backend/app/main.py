from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any, Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.config import settings
from app.core.security import get_password_hash
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.scope import Scope
from app.models.user import User, UserRole


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Database tables initialization and default demonstration seed setup."""
    Base.metadata.create_all(bind=engine)

    # Seed default demonstration accounts & sample scope
    db = SessionLocal()
    try:
        demo_accounts = [
            ("admin", "admin@aegisaudit.local", "DemoAdmin2026!", UserRole.ADMIN),
            ("auditor", "auditor@aegisaudit.local", "DemoAuditor2026!", UserRole.AUDITOR),
            ("viewer", "viewer@aegisaudit.local", "DemoViewer2026!", UserRole.VIEWER),
        ]
        for username, email, raw_pwd, role in demo_accounts:
            existing = db.query(User).filter(User.username == username).first()
            if not existing:
                user = User(
                    username=username,
                    email=email,
                    hashed_password=get_password_hash(raw_pwd),
                    role=role,
                    is_active=True,
                )
                db.add(user)

        scope = db.query(Scope).first()
        if not scope:
            demo_scope = Scope(
                name="Internal Lab Network Scope",
                description="Authorized lab targets for credential auditing",
                allowed_targets="10.0.0.0/24, 192.168.1.0/24, 127.0.0.1, localhost, demo.lab",
                allowed_ports="22,80,443,3389,8080",
                allowed_protocols="ssh,http,https,rdp,ftp",
            )
            db.add(demo_scope)

        db.commit()
    finally:
        db.close()

    yield


app = FastAPI(
    title="AegisAudit API",
    description="Authorized Credential Security Assessment Platform REST API Engine",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS
origins = settings.cors_origins_list if settings.cors_origins_list else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API v1 router
app.include_router(api_router)


@app.get("/health", tags=["Health"])
def health_check() -> Dict[str, Any]:
    """Health check endpoint."""
    return {
        "status": "online",
        "app": settings.APP_NAME,
        "version": "0.1.0",
        "mock_engine": settings.MOCK_ENGINE,
        "environment": settings.ENVIRONMENT,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
