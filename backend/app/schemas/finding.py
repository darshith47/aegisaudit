from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.finding import FindingSeverity


class FindingResponse(BaseModel):
    id: int
    assessment_id: int
    title: str
    severity: FindingSeverity
    vulnerability_type: str
    target: str
    details: str
    remediation: Optional[str]
    evidence_id: Optional[int]
    is_mock: bool
    created_at: datetime

    class Config:
        from_attributes = True
