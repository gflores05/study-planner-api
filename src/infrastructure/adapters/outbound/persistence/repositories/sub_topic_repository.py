from sqlalchemy import select

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
  def __init__(self, db: Database):
    self._db = db

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
    async with self._db.get_session() as session:
      sub_topic.increment_version()
      model = map_sub_topic_domain_to_model(sub_topic)
      await session.merge(model)
      await session.flush()
