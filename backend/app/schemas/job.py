from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any
from app.models.job import JobStatus


class JobCreate(BaseModel):
    assessment_id: int
    parameters: Optional[Dict[str, Any]] = None


class JobResponse(BaseModel):
    id: int
    assessment_id: int
    engine_name: str
    status: JobStatus
    progress: float
    parameters: Dict[str, Any]
    output: str
    mock_mode: bool
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True
