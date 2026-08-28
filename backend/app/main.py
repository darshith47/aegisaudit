from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.api import api_router
from app.models.user import User, UserRole
from app.models.scope import Scope
from app.core.security import get_password_hash


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Database tables initialization and default seed data setup."""
    Base.metadata.create_all(bind=engine)

    # Seed default Admin User & Sample Scope if database is clean
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin = User(
                username="admin",
                email="admin@aegisaudit.local",
                hashed_password=get_password_hash("AdminPass2026!"),
                role=UserRole.ADMIN
            )
            db.add(admin)
            db.commit()

        scope = db.query(Scope).first()
        if not scope:
            demo_scope = Scope(
                name="Internal Lab Network Scope",
                description="Authorized lab targets for credential auditing",
                allowed_targets="10.0.0.0/24, 192.168.1.0/24, 127.0.0.1, localhost, demo.lab",
                allowed_ports="22,80,443,3389,8080",
                allowed_protocols="ssh,http,https,rdp,ftp"
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
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API v1 router
app.include_router(api_router)


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {
        "status": "online",
        "app": settings.APP_NAME,
        "version": "0.1.0",
        "mock_engine": settings.MOCK_ENGINE,
        "environment": settings.ENVIRONMENT
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
