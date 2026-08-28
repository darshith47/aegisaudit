from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse, Response
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.assessment import Assessment
from app.models.user import User
from app.schemas.report import ReportRequest, ReportResponse
from app.core.security import get_current_user
from app.services.report_generator import ExecutiveReportGenerator

router = APIRouter(prefix="/reports", tags=["Executive Security Reports"])


@router.post("/generate", response_model=ReportResponse)
def generate_report(
    req: ReportRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate executive audit report in Markdown or HTML format."""
    assessment = db.query(Assessment).filter(Assessment.id == req.assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found.")

    if req.format.lower() == "html":
        content = ExecutiveReportGenerator.generate_html_report(db, req.assessment_id)
    else:
        content = ExecutiveReportGenerator.generate_markdown_report(db, req.assessment_id)

    return ReportResponse(
        assessment_id=assessment.id,
        title=assessment.title,
        target=assessment.target,
        generated_at=datetime.utcnow(),
        format=req.format,
        content=content
    )


@router.get("/{assessment_id}/html", response_class=HTMLResponse)
def view_html_report(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Render executive audit report directly as HTML page."""
    return ExecutiveReportGenerator.generate_html_report(db, assessment_id)
