from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.assessment import Assessment, AssessmentStatus
from app.models.scope import Scope
from app.models.user import User, UserRole
from app.schemas.assessment import AssessmentCreate, AssessmentResponse
from app.core.security import get_current_user, require_role
from app.adapters.registry import engine_registry

router = APIRouter(prefix="/assessments", tags=["Assessment Management"])


@router.post("/", response_model=AssessmentResponse, status_code=status.HTTP_201_CREATED)
def create_assessment(
    ass_in: AssessmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.AUDITOR]))
):
    """Create a new authorized security assessment."""
    scope = db.query(Scope).filter(Scope.id == ass_in.scope_id).first()
    if not scope:
        raise HTTPException(status_code=404, detail="Selected Scope policy does not exist.")

    # Check if engine exists in registry
    adapter = engine_registry.get_adapter(ass_in.engine)
    if not adapter:
        raise HTTPException(
            status_code=400,
            detail=f"Engine '{ass_in.engine}' is not supported. See /api/v1/engines for matrix."
        )

    assessment = Assessment(
        title=ass_in.title,
        description=ass_in.description,
        target=ass_in.target,
        engine=ass_in.engine.lower(),
        scope_id=ass_in.scope_id,
        status=AssessmentStatus.CREATED
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    return assessment


@router.get("/", response_model=List[AssessmentResponse])
def list_assessments(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """List all credential security assessments."""
    return db.query(Assessment).order_by(Assessment.id.desc()).all()


@router.get("/{assessment_id}", response_model=AssessmentResponse)
def get_assessment(assessment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get assessment details by ID."""
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found.")
    return assessment
