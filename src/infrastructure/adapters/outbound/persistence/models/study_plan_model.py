from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.adapters.outbound.persistence.models.base import DbModel


class StudyPlanModel(DbModel):
  __tablename__ = "study_plan"

  subject: Mapped[str] = mapped_column(String(100), nullable=False)
  level: Mapped[str] = mapped_column(String(24), nullable=False)
  status: Mapped[str] = mapped_column(String(16), nullable=False)
