from sqlalchemy import select

from src.application.ports.outbound.messaging.domain_event_publisher import (
  DomainEventPublisherPort,
)
from src.domain.question.question import Question
from src.domain.question.value_objects.question_id import QuestionId
from src.infrastructure.adapters.outbound.persistence.mappers.question_mapper import (
  map_question_domain_to_model,
  map_question_model_to_domain,
)
from src.infrastructure.adapters.outbound.persistence.models.question_model import (
  QuestionModel,
)
from src.infrastructure.config.database import Database
from src.shared.option import Option


class QuestionRepository:
  def __init__(self, db: Database, domain_event_publisher: DomainEventPublisherPort):
    self._db = db
    self._domain_event_publisher = domain_event_publisher

  async def get(self, id: QuestionId) -> Option[Question]:
    async with self._db.get_session() as session:
      result = await session.execute(
        select(QuestionModel).where(QuestionModel.id == str(id))
      )

      row = result.scalar_one_or_none()

      if not row:
        return Option.nothing()
      return Option.some(map_question_model_to_domain(row))

  async def save(self, question: Question):
    question.increment_version()
    model = map_question_domain_to_model(question)

    async with self._db.get_session() as session:
      await session.merge(model)
      await session.flush()

    await self._domain_event_publisher.publish_events(question)
