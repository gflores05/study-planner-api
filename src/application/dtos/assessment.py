from dataclasses import dataclass
from enum import Enum

from src.application.dtos.question import QuestionDTO


class AssessmentStatusDTO(Enum):
  PENDING = "PENDING"
  IN_PROGRESS = "IN_PROGRESS"
  COMPLETED = "COMPLETED"


@dataclass
class AssessmentDTO:
  id: str
  status: AssessmentStatusDTO
  score: int | None
  questions: list[QuestionDTO]
  started_on: str | None
  completed_on: str | None
  topic_id: str


@dataclass
class AnswerQuestionRequestDTO:
  assessment_id: str
  question_id: str
  selected_answer: str
