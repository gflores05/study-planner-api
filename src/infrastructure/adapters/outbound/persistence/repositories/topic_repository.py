from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.application.ports.outbound.messaging.domain_event_publisher import (
  DomainEventPublisherPort,
)
from src.domain.topic.topic import Topic
from src.domain.topic.value_objects.topic_id import TopicId
from src.infrastructure.adapters.outbound.persistence.mappers.topic_mapper import (
  map_topic_domain_to_model,
  map_topic_model_to_domain,
)
from src.infrastructure.adapters.outbound.persistence.models.assessment_model import (
  AssessmentModel,
)
from src.infrastructure.adapters.outbound.persistence.models.topic_model import (
  TopicModel,
)
from src.infrastructure.config.database import Database
from src.shared.option import Option


class TopicRepository:
  def __init__(self, db: Database, domain_event_publisher: DomainEventPublisherPort):
    self._db = db
    self._domain_event_publisher = domain_event_publisher

  async def get(self, id: TopicId, load_children: bool = True) -> Option[Topic]:
    async with self._db.get_session() as session:
      query = select(TopicModel).where(TopicModel.id == str(id))

      if load_children:
        query = query.options(
          selectinload(TopicModel.assessment).selectinload(AssessmentModel.questions),
          selectinload(TopicModel.sub_topics),
        )

      result = await session.execute(query)

      row = result.scalar_one_or_none()

      if not row:
        return Option.nothing()
      return Option.some(map_topic_model_to_domain(row, include_children=load_children))

  async def save(self, topic: Topic):
    topic.increment_version()
    model = map_topic_domain_to_model(topic)

    async with self._db.get_session() as session:
      await session.merge(model)
      await session.flush()

    await self._domain_event_publisher.publish_events(topic)
