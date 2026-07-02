from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.question.question import Question
from src.domain.question.value_objects.question_id import QuestionId
from src.infrastructure.adapters.outbound.persistence.mappers.question_mapper import (
  map_question_domain_to_model,
  map_question_model_to_domain,
)
from src.infrastructure.adapters.outbound.persistence.models.question_model import (
  QuestionModel,
)
from src.shared.option import Option


class QuestionRepository:
  def __init__(self, session: AsyncSession):
    self._session = session

  async def get(self, id: QuestionId) -> Option[Question]:
    result = await self._session.execute(
      select(QuestionModel).where(QuestionModel.id == id)
    )

    row = result.scalar_one_or_none()

    if not row:
      return Option.nothing()
    return Option.some(map_question_model_to_domain(row))

  async def save(self, question: Question):
    question.increment_version()
    model = map_question_domain_to_model(question)
    await self._session.merge(model)
    await self._session.flush()
