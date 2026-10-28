from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import require_role
from app.db.session import get_db
from app.models.audit import AuditLog
from app.models.user import User, UserRole
from app.schemas.audit import AuditLogResponse

router = APIRouter(prefix="/audit", tags=["Compliance & Audit Logs"])


@router.get("/", response_model=List[AuditLogResponse])
def list_audit_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.AUDITOR])),
) -> List[AuditLog]:
    """View immutable security audit log trail."""
    return db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(100).all()
