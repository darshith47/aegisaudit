import enum
from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.finding import Finding
    from app.models.job import Job
    from app.models.scope import Scope


class AssessmentStatus(str, enum.Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Assessment(Base):
    __tablename__ = "assessments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    target: Mapped[str] = mapped_column(String(255), nullable=False)  # Target IP / domain / hash
    engine: Mapped[str] = mapped_column(String(64), nullable=False)  # hashcat, john, hydra
    status: Mapped[AssessmentStatus] = mapped_column(
        Enum(AssessmentStatus), default=AssessmentStatus.CREATED, nullable=False
    )
    scope_id: Mapped[int] = mapped_column(Integer, ForeignKey("scopes.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    scope: Mapped["Scope"] = relationship("Scope", back_populates="assessments")
    jobs: Mapped[List["Job"]] = relationship(
        "Job", back_populates="assessment", cascade="all, delete-orphan"
    )
    findings: Mapped[List["Finding"]] = relationship(
        "Finding", back_populates="assessment", cascade="all, delete-orphan"
    )
