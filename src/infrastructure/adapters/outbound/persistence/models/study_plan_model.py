from typing import Literal

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.adapters.outbound.persistence.models.topic_model import (
  TopicModel,
)
from src.infrastructure.config.database import DbModel

DbStudyPlanLevel = Literal[
  "Elementary School", "High School", "Preparatory", "University", "Postgraduate"
]


class StudyPlanModel(DbModel):
  __tablename__ = "study_plan"

  subject: Mapped[str] = mapped_column(String(100), nullable=False)
  level: Mapped[DbStudyPlanLevel] = mapped_column(String(24), nullable=False)
  status: Mapped[str] = mapped_column(String(16), nullable=False)
  grade: Mapped[int] = mapped_column(Integer, nullable=False)
  topics: Mapped[list[TopicModel]] = relationship(back_populates="topic")
