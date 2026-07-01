from src.domain.question.question import Question
from src.domain.question.value_objects.question_id import QuestionId
from src.shared.option import Option


class FakeQuestionRepository:
  def __init__(self, data: list[Question]):
    self.data = data

  async def get(self, id: QuestionId) -> Option[Question]:
    return Option.of(next((sp for sp in self.data if sp.id == id), None))

  async def save(self, question: Question) -> None:
    exists = (await self.get(question.id)).is_some

    if exists:
      self.data = [st if st.id != question.id else question for st in self.data]
    else:
      self.data.append(question)
