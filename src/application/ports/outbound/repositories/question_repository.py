from typing import Protocol

from src.domain.question.question import Question
from src.domain.question.value_objects.question_id import QuestionId
from src.shared.option import Option


class QuestionRepository(Protocol):
  async def get(self, id: QuestionId) -> Option[Question]: ...
  async def save(self, question: Question) -> None: ...
