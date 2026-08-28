from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any


class AuditLogResponse(BaseModel):
    id: int
    user_id: Optional[int]
    action: str
    resource: str
    details: Dict[str, Any]
    ip_address: Optional[str]
    timestamp: datetime

    class Config:
        from_attributes = True
