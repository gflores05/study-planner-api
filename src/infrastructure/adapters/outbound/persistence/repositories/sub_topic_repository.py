from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.sub_topic.sub_topic import SubTopic
from src.domain.sub_topic.value_objects.sub_topic_id import SubTopicId
from src.infrastructure.adapters.outbound.persistence.mappers.sub_topic_mapper import (
  map_sub_topic_domain_to_model,
  map_sub_topic_model_to_domain,
)
from src.infrastructure.adapters.outbound.persistence.models.sub_topic_model import (
  SubTopicModel,
)
from src.shared.option import Option


class SubTopicRepository:
  def __init__(self, session: AsyncSession):
    self._session = session

  async def get(self, id: SubTopicId) -> Option[SubTopic]:
    result = await self._session.execute(
      select(SubTopicModel).where(SubTopicModel.id == id)
    )

    row = result.scalar_one_or_none()

    if not row:
      return Option.nothing()
    return Option.some(map_sub_topic_model_to_domain(row))

  async def save(self, sub_topic: SubTopic):
    sub_topic.increment_version()
    model = map_sub_topic_domain_to_model(sub_topic)
    await self._session.merge(model)
    await self._session.flush()
