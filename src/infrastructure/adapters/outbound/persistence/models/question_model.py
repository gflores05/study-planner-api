import uuid
from dataclasses import dataclass

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.adapters.outbound.persistence.models.base import DbModel
from src.infrastructure.adapters.outbound.persistence.util.jsonb_dataclass import (
  JSONBDataClassArray,
)


@dataclass
class AnswerModel:
  text: str
  option: str


class QuestionModel(DbModel):
  __tablename__ = "question"

  text: Mapped[str] = mapped_column(String(100), nullable=False)
  options: Mapped[list[AnswerModel]] = mapped_column(
    JSONBDataClassArray(AnswerModel), nullable=False
  )
  answer: Mapped[str] = mapped_column(String(1), nullable=False)
  selected_answer: Mapped[str] = mapped_column(String(1), nullable=False)
  assessment_id: Mapped[uuid.UUID] = mapped_column(
    ForeignKey("assessment.id"), nullable=False
  )
