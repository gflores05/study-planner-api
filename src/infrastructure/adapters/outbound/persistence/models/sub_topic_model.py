import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.config.database import DbModel


class SubTopicModel(DbModel):
  __tablename__ = "sub_topic"

  title: Mapped[str] = mapped_column(String(100), nullable=False)
  study_material: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
  topic_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("topic.id"), nullable=False)
