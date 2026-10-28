from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.finding import FindingSeverity


class FindingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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
