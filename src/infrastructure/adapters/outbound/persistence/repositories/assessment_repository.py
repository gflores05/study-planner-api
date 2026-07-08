from sqlalchemy import select

from src.domain.assessment.assessment import Assessment
from src.domain.assessment.value_objects.assessment_id import AssessmentId
from src.infrastructure.adapters.outbound.persistence.mappers.assessment_mapper import (
  map_assessment_domain_to_model,
  map_assessment_model_to_domain,
)
from src.infrastructure.adapters.outbound.persistence.models.assessment_model import (
  AssessmentModel,
)
from src.infrastructure.config.database import Database
from src.shared.option import Option


class AssessmentRepository:
  def __init__(self, db: Database):
    self._db = db

  async def get(self, id: AssessmentId) -> Option[Assessment]:
    async with self._db.get_session() as session:
      result = await session.execute(
        select(AssessmentModel).where(AssessmentModel.id == str(id))
      )

      row = result.scalar_one_or_none()

      if not row:
        return Option.nothing()
      return Option.some(map_assessment_model_to_domain(row))

  async def save(self, assessment: Assessment):
    async with self._db.get_session() as session:
      assessment.increment_version()
      model = map_assessment_domain_to_model(assessment)
      await session.merge(model)
      await session.flush()
