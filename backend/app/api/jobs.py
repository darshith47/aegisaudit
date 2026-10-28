from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config import settings
from app.core.security import get_current_user, require_role
from app.db.session import get_db
from app.models.assessment import Assessment
from app.models.job import Job, JobStatus
from app.models.user import User, UserRole
from app.schemas.job import JobCreate, JobResponse
from app.services.job_runner import JobRunnerService

router = APIRouter(prefix="/jobs", tags=["Job Management & Worker Engine"])


@router.post("/launch", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def launch_job(
    job_in: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.AUDITOR])),
) -> Job:
    """Launch a security assessment job through the centralized execution pipeline."""
    assessment = db.query(Assessment).filter(Assessment.id == job_in.assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found.")

    new_job = Job(
        assessment_id=assessment.id,
        engine_name=assessment.engine,
        status=JobStatus.QUEUED,
        parameters=job_in.parameters or {},
        mock_mode=settings.MOCK_ENGINE,
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    # Execute job synchronously / background task runner
    executed_job = JobRunnerService.execute_job(db=db, job_id=new_job.id, user_id=current_user.id)
    return executed_job


@router.get("/", response_model=List[JobResponse])
def list_jobs(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> List[Job]:
    """List all assessment jobs."""
    return db.query(Job).order_by(Job.id.desc()).all()


@router.get("/{job_id}", response_model=JobResponse)
def get_job(
    job_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> Job:
    """Get job details and execution output by ID."""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")
    return job
