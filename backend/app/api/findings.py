from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.models.finding import Finding
from app.models.user import User
from app.schemas.finding import FindingResponse
from app.core.security import get_current_user

router = APIRouter(prefix="/findings", tags=["Findings & Evidence"])


@router.get("/", response_model=List[FindingResponse])
def list_findings(
    assessment_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List identified security findings, optionally filtered by assessment_id."""
    query = db.query(Finding)
    if assessment_id:
        query = query.filter(Finding.assessment_id == assessment_id)
    return query.order_by(Finding.id.desc()).all()


@router.get("/{finding_id}", response_model=FindingResponse)
def get_finding(finding_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get finding details by ID."""
    finding = db.query(Finding).filter(Finding.id == finding_id).first()
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found.")
    return finding
