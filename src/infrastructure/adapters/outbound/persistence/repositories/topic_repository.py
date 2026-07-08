from sqlalchemy import select

from src.domain.topic.topic import Topic
from src.domain.topic.value_objects.topic_id import TopicId
from src.infrastructure.adapters.outbound.persistence.mappers.topic_mapper import (
  map_topic_domain_to_model,
  map_topic_model_to_domain,
)
from src.infrastructure.adapters.outbound.persistence.models.topic_model import (
  TopicModel,
)
from src.infrastructure.config.database import Database
from src.shared.option import Option


class TopicRepository:
  def __init__(self, db: Database):
    self._db = db

  async def get(self, id: TopicId) -> Option[Topic]:
    async with self._db.get_session() as session:
      result = await session.execute(select(TopicModel).where(TopicModel.id == str(id)))

      row = result.scalar_one_or_none()

      if not row:
        return Option.nothing()
      return Option.some(map_topic_model_to_domain(row))

  async def save(self, topic: Topic):
    async with self._db.get_session() as session:
      topic.increment_version()
      model = map_topic_domain_to_model(topic)
      await session.merge(model)
      await session.flush()
