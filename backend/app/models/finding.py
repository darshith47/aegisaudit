import enum
from datetime import datetime
from sqlalchemy import String, Enum, DateTime, Text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, TYPE_CHECKING

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.assessment import Assessment
    from app.models.evidence import Evidence


class FindingSeverity(str, enum.Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class Finding(Base):
    __tablename__ = "findings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    assessment_id: Mapped[int] = mapped_column(Integer, ForeignKey("assessments.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    severity: Mapped[FindingSeverity] = mapped_column(Enum(FindingSeverity), nullable=False)
    vulnerability_type: Mapped[str] = mapped_column(String(128), nullable=False)
    target: Mapped[str] = mapped_column(String(255), nullable=False)
    details: Mapped[str] = mapped_column(Text, nullable=False)
    remediation: Mapped[str] = mapped_column(Text, nullable=True)
    evidence_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("evidence.id"), nullable=True)
    is_mock: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    assessment: Mapped["Assessment"] = relationship("Assessment", back_populates="findings")
    evidence: Mapped[Optional["Evidence"]] = relationship("Evidence", back_populates="findings")
