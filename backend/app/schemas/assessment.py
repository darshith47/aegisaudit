from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.assessment import AssessmentStatus
from app.schemas.scope import ScopeResponse


class AssessmentCreate(BaseModel):
    title: str
    description: Optional[str] = None
    target: str
    engine: str  # hashcat, john, hydra
    scope_id: int


class AssessmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str]
    target: str
    engine: str
    status: AssessmentStatus
    scope_id: int
    created_at: datetime
    updated_at: datetime
    scope: Optional[ScopeResponse] = None
