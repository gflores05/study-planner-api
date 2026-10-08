from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.application.ports.outbound.messaging.domain_event_publisher import (
  DomainEventPublisherPort,
)
from src.domain.study_plan.study_plan import StudyPlan
from src.domain.study_plan.value_objects.study_plan_id import StudyPlanId
from src.infrastructure.adapters.outbound.persistence.mappers.study_plan_mapper import (
  map_study_plan_domain_to_model,
  map_study_plan_model_to_domain,
)
from src.infrastructure.adapters.outbound.persistence.models.assessment_model import (
  AssessmentModel,
)
from src.infrastructure.adapters.outbound.persistence.models.study_plan_model import (
  StudyPlanModel,
)
from src.infrastructure.adapters.outbound.persistence.models.topic_model import (
  TopicModel,
)
from src.infrastructure.config.database import Database
from src.shared.option import Option


class StudyPlanRepository:
  def __init__(self, db: Database, domain_event_publisher: DomainEventPublisherPort):
    self._db = db
    self._domain_event_publisher = domain_event_publisher

  async def get(self, id: StudyPlanId) -> Option[StudyPlan]:
    async with self._db.get_session() as session:
      result = await session.execute(
        select(StudyPlanModel)
        .where(StudyPlanModel.id == str(id))
        .options(
          selectinload(StudyPlanModel.topics)
          .selectinload(TopicModel.assessment)
          .selectinload(AssessmentModel.questions),
          selectinload(StudyPlanModel.topics).selectinload(TopicModel.sub_topics),
        )
      )

      row = result.scalar_one_or_none()

      if not row:
        return Option.nothing()
      return Option.some(map_study_plan_model_to_domain(row))

  async def save(self, study_plan: StudyPlan):
    study_plan.increment_version()
    model = map_study_plan_domain_to_model(study_plan)

    async with self._db.get_session() as session:
      await session.merge(model)
      await session.flush()

    await self._domain_event_publisher.publish_events(study_plan)
