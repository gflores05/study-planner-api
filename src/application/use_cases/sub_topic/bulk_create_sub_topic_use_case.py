import asyncio

from src.application.dtos.sub_topic import SubTopicDTO
from src.application.mappers.sub_topic_mapper import map_sub_topic_dto_to_domain
from src.application.ports.outbound.messaging.event_publisher import EventPublisher
from src.application.ports.outbound.repositories.sub_topic_respository import (
  SubTopicRepository,
)
from src.application.use_cases.use_case_event_publisher import UseCaseEventPublisher
from src.domain.sub_topic.sub_topic import SubTopic
from src.util.result_util import traverse


class BulkCreateSubTopicUseCase(UseCaseEventPublisher):
  def __init__(
    self, sub_topic_repository: SubTopicRepository, event_publisher: EventPublisher
  ):
    self.event_publisher = event_publisher
    self.sub_topic_repository = sub_topic_repository

  async def execute(self, dtos: list[SubTopicDTO]) -> None:
    sub_topics = traverse(
      [map_sub_topic_dto_to_domain(dto) for dto in dtos]
    ).unwrap_or_raise()

    async with asyncio.TaskGroup() as tg:
      for subtopic in sub_topics:
        tg.create_task(self._save_sub_topic(subtopic=subtopic))

  async def _save_sub_topic(self, subtopic: SubTopic):
    await self.sub_topic_repository.save(subtopic)

    await self._publish_events(subtopic)
