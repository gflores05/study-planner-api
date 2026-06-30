from dataclasses import dataclass

from src.application.dtos.answer import AnswerAIDTO, AnswerDTO


@dataclass
class QuestionDTO:
  id: str
  text: str
  options: list[AnswerDTO]
  answer: str
  selected_answer: str | None
  assessment_id: str


@dataclass
class QuestionAIDTO:
  t: str
  os: list[AnswerAIDTO]
  a: str
