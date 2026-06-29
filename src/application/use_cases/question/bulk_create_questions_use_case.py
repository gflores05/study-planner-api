import asyncio

from src.application.dtos.question import QuestionDTO
from src.application.mappers.question_mapper import map_question_dto_to_domain
from src.application.ports.outbound.messaging.event_publisher import EventPublisher
from src.application.ports.outbound.repositories.question_repository import (
  QuestionRepository,
)
from src.application.use_cases.use_case_event_publisher import UseCaseEventPublisher
from src.util.result_util import traverse


class BulkCreateQuestionsUseCase(UseCaseEventPublisher):
  def __init__(
    self, question_repository: QuestionRepository, event_publisher: EventPublisher
  ):
    self.event_publisher = event_publisher
    self.question_repository = question_repository

  async def execute(self, dtos: list[QuestionDTO]) -> None:
    questions = traverse(
      [map_question_dto_to_domain(dto) for dto in dtos]
    ).unwrap_or_raise()

    async with asyncio.TaskGroup() as tg:
      for question in questions:
        tg.create_task(self._save_question(question=question))

  async def _save_question(self, question):
    await self.question_repository.save(question=question)

    await self._publish_events(question)
