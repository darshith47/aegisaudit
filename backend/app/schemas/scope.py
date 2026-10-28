from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ScopeCreate(BaseModel):
    name: str = Field(..., description="Scope title or client identifier")
    description: Optional[str] = None
    allowed_targets: str = Field(
        ..., description="Comma-separated IP addresses, CIDRs, or hostnames"
    )
    allowed_ports: str = "22,80,443,3389,8080"
    allowed_protocols: str = "ssh,http,https,rdp,ftp"


class ScopeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str]
    allowed_targets: str
    allowed_ports: str
    allowed_protocols: str
    created_at: datetime


class ScopeValidationRequest(BaseModel):
    scope_id: int
    target: str
    port: Optional[int] = None
    protocol: Optional[str] = None


class ScopeValidationResult(BaseModel):
    is_allowed: bool
    scope_id: int
    target: str
    reason: str
