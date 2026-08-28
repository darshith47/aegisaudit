from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.scope import Scope
from app.models.user import User, UserRole
from app.schemas.scope import ScopeCreate, ScopeResponse, ScopeValidationRequest, ScopeValidationResult
from app.core.security import get_current_user, require_role
from app.core.scope_engine import ScopeEngine

router = APIRouter(prefix="/scope", tags=["Scope Management"])


@router.post("/", response_model=ScopeResponse, status_code=status.HTTP_201_CREATED)
def create_scope(
    scope_in: ScopeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.AUDITOR]))
):
    """Define a new authorized assessment target scope policy."""
    scope = Scope(
        name=scope_in.name,
        description=scope_in.description,
        allowed_targets=scope_in.allowed_targets,
        allowed_ports=scope_in.allowed_ports,
        allowed_protocols=scope_in.allowed_protocols
    )
    db.add(scope)
    db.commit()
    db.refresh(scope)
    return scope


@router.get("/", response_model=List[ScopeResponse])
def list_scopes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """List all authorized target scope policies."""
    return db.query(Scope).order_by(Scope.id.desc()).all()


@router.get("/{scope_id}", response_model=ScopeResponse)
def get_scope(scope_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get scope policy by ID."""
    scope = db.query(Scope).filter(Scope.id == scope_id).first()
    if not scope:
        raise HTTPException(status_code=404, detail="Scope policy not found.")
    return scope


@router.post("/validate", response_model=ScopeValidationResult)
def validate_target_scope(
    val_req: ScopeValidationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Validate whether a target IP/domain/port/protocol is permitted by scope policy."""
    scope = db.query(Scope).filter(Scope.id == val_req.scope_id).first()
    if not scope:
        raise HTTPException(status_code=404, detail="Scope policy not found.")

    is_allowed, reason = ScopeEngine.validate_target(
        scope=scope,
        target=val_req.target,
        port=val_req.port,
        protocol=val_req.protocol
    )

    return ScopeValidationResult(
        is_allowed=is_allowed,
        scope_id=val_req.scope_id,
        target=val_req.target,
        reason=reason
    )
