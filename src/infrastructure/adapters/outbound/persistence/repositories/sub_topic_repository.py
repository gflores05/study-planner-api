from sqlalchemy import select

from src.application.ports.outbound.messaging.domain_event_publisher import (
  DomainEventPublisherPort,
)
from src.domain.sub_topic.sub_topic import SubTopic
from src.domain.sub_topic.value_objects.sub_topic_id import SubTopicId
from src.infrastructure.adapters.outbound.persistence.mappers.sub_topic_mapper import (
  map_sub_topic_domain_to_model,
  map_sub_topic_model_to_domain,
)
from src.infrastructure.adapters.outbound.persistence.models.sub_topic_model import (
  SubTopicModel,
)
from src.infrastructure.config.database import Database
from src.shared.option import Option


class SubTopicRepository:
  def __init__(self, db: Database, domain_event_publisher: DomainEventPublisherPort):
    self._db = db
    self._domain_event_publisher = domain_event_publisher

  async def get(self, id: SubTopicId) -> Option[SubTopic]:
    async with self._db.get_session() as session:
      result = await session.execute(
        select(SubTopicModel).where(SubTopicModel.id == str(id))
      )

      row = result.scalar_one_or_none()

      if not row:
        return Option.nothing()
      return Option.some(map_sub_topic_model_to_domain(row))

  async def save(self, sub_topic: SubTopic):
    sub_topic.increment_version()
    model = map_sub_topic_domain_to_model(sub_topic)

    async with self._db.get_session() as session:
      await session.merge(model)
      await session.flush()

    await self._domain_event_publisher.publish_events(sub_topic)
