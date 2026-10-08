from dataclasses import dataclass

from pydantic import BaseModel, Field

from src.application.dtos.answer import AnswerAIDTO, AnswerDTO


class QuestionDTO(BaseModel):
  id: str
  text: str
  options: list[AnswerDTO]
  answer: str
  selected_answer: str | None
  assessment_id: str
  created_by_user_id: str


class QuestionAIDTO(BaseModel):
  t: str = Field(description="The question text")
  os: list[AnswerAIDTO] = Field(description="List of 4 possible answer numbered a-d")
  a: str = Field(description="The letter of the correct answer")


@dataclass
class QuestionResponseDTO:
  id: str
