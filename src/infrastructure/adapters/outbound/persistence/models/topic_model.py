import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.adapters.outbound.persistence.models.assessment_model import (
  AssessmentModel,
)
from src.infrastructure.adapters.outbound.persistence.models.sub_topic_model import (
  SubTopicModel,
)
from src.infrastructure.config.database import DbModel


class TopicModel(DbModel):
  __tablename__ = "topic"

  title: Mapped[str] = mapped_column(String(100), nullable=False)
  study_plan_id: Mapped[uuid.UUID] = mapped_column(
    ForeignKey("study_plan.id"), nullable=False
  )
  sub_topics: Mapped[list[SubTopicModel]] = relationship(back_populates="sub_topic")
  assessment: Mapped[AssessmentModel] = relationship(back_populates="Assessment")
