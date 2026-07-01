import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.adapters.outbound.persistence.models.base import DbModel


class TopicModel(DbModel):
  __tablename__ = "topic"

  title: Mapped[str] = mapped_column(String(100), nullable=False)
  study_plan_id: Mapped[uuid.UUID] = mapped_column(
    ForeignKey("study_plan.id"), nullable=False
  )
