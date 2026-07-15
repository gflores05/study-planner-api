from src.application.dtos.topic import TopicDTO
from src.application.mappers.topic_mapper import map_topic_domain_to_dto
from src.application.ports.outbound.repositories.topic_repository import (
  TopicRepository,
)
from src.application.use_cases.topic.error import (
  TopicInvalidInputError,
  TopicNotFoundError,
)
from src.domain.topic.value_objects.topic_id import TopicId


class GetTopicUseCaseAdapter:
  def __init__(self, topic_repository: TopicRepository):
    self.topic_repository = topic_repository

  async def execute(self, id: str, include_children: bool) -> TopicDTO:
    topic_id = TopicId.parse(id).unwrap_or_map_and_raise(
      lambda problem: TopicInvalidInputError(value=str(problem.value), field="topic_id")
    )

    topic = (await self.topic_repository.get(topic_id, include_children)).get_or_raise(
      TopicNotFoundError(topic_id=id)
    )

    return map_topic_domain_to_dto(topic, include_children=include_children)
