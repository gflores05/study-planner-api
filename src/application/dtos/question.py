from dataclasses import dataclass

from src.application.dtos.answer import AnswerDTO


@dataclass
class QuestionDTO:
  id: str
  text: str
  options: list[AnswerDTO]
  answer: str
  selected_answer: str | None
  assessment_id: str
