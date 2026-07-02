from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.topic.topic import Topic
from src.domain.topic.value_objects.topic_id import TopicId
from src.infrastructure.adapters.outbound.persistence.mappers.topic_mapper import (
  map_topic_domain_to_model,
  map_topic_model_to_domain,
)
from src.infrastructure.adapters.outbound.persistence.models.topic_model import (
  TopicModel,
)
from src.shared.option import Option


class TopicRepository:
  def __init__(self, session: AsyncSession):
    self._session = session

  async def get(self, id: TopicId) -> Option[Topic]:
    result = await self._session.execute(select(TopicModel).where(TopicModel.id == id))

    row = result.scalar_one_or_none()

    if not row:
      return Option.nothing()
    return Option.some(map_topic_model_to_domain(row))

  async def save(self, topic: Topic):
    topic.increment_version()
    model = map_topic_domain_to_model(topic)
    await self._session.merge(model)
    await self._session.flush()
