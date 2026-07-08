from dataclasses import dataclass

from pydantic import BaseModel

from src.application.dtos.answer import AnswerAIDTO, AnswerDTO


class QuestionDTO(BaseModel):
  id: str
  text: str
  options: list[AnswerDTO]
  answer: str
  selected_answer: str | None
  assessment_id: str


class QuestionAIDTO(BaseModel):
  t: str
  os: list[AnswerAIDTO]
  a: str


@dataclass
class QuestionResponseDTO:
  id: str
