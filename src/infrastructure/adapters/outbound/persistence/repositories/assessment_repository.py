from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.application.ports.outbound.messaging.domain_event_publisher import (
  DomainEventPublisherPort,
)
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
  def __init__(self, db: Database, domain_event_publisher: DomainEventPublisherPort):
    self._db = db
    self._domain_event_publisher = domain_event_publisher

  async def get(self, id: AssessmentId) -> Option[Assessment]:
    async with self._db.get_session() as session:
      result = await session.execute(
        select(AssessmentModel)
        .where(AssessmentModel.id == str(id))
        .options(selectinload(AssessmentModel.questions))
      )

      row = result.scalar_one_or_none()

      if not row:
        return Option.nothing()
      return Option.some(map_assessment_model_to_domain(row))

  async def save(self, assessment: Assessment):
    assessment.increment_version()
    model = map_assessment_domain_to_model(assessment)

    async with self._db.get_session() as session:
      await session.merge(model)
      await session.flush()

    await self._domain_event_publisher.publish_events(assessment)
