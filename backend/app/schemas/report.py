from datetime import datetime

from pydantic import BaseModel


class ReportRequest(BaseModel):
    assessment_id: int
    format: str = "markdown"  # markdown or html


class ReportResponse(BaseModel):
    assessment_id: int
    title: str
    target: str
    generated_at: datetime
    format: str
    content: str
