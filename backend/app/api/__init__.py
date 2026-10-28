from fastapi import APIRouter

from app.api.assessments import router as assessments_router
from app.api.audit import router as audit_router
from app.api.auth import router as auth_router
from app.api.engines import router as engines_router
from app.api.findings import router as findings_router
from app.api.jobs import router as jobs_router
from app.api.reports import router as reports_router
from app.api.scope import router as scope_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth_router)
api_router.include_router(scope_router)
api_router.include_router(assessments_router)
api_router.include_router(jobs_router)
api_router.include_router(findings_router)
api_router.include_router(reports_router)
api_router.include_router(audit_router)
api_router.include_router(engines_router)
