from datetime import datetime
from sqlalchemy import String, DateTime, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, TYPE_CHECKING

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.assessment import Assessment


class Scope(Base):
    __tablename__ = "scopes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    allowed_targets: Mapped[str] = mapped_column(Text, nullable=False)  # Comma-separated IPs, CIDRs, hostnames
    allowed_ports: Mapped[str] = mapped_column(String(255), default="22,80,443,3389,8080")
    allowed_protocols: Mapped[str] = mapped_column(String(255), default="ssh,http,https,rdp,ftp")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    assessments: Mapped[List["Assessment"]] = relationship("Assessment", back_populates="scope")
