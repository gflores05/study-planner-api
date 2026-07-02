import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.adapters.outbound.persistence.models.base import DbModel
from src.infrastructure.adapters.outbound.persistence.models.question_model import (
  QuestionModel,
)


class AssessmentModel(DbModel):
  __tablename__ = "assessment"

  status: Mapped[str] = mapped_column(String(16), nullable=False)
  score: Mapped[int] = mapped_column(Integer, nullable=True)
  started_on: Mapped[datetime] = mapped_column(DateTime, nullable=True)
  completed_on: Mapped[datetime] = mapped_column(DateTime, nullable=True)
  topic_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("topic.id"), nullable=False)
  questions: Mapped[list[QuestionModel]] = relationship(back_populates="question")
