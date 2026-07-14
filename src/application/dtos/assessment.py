from enum import Enum

from pydantic import BaseModel

from src.application.dtos.question import QuestionDTO, QuestionResponseDTO


class AssessmentStatusDTO(Enum):
  PENDING = "PENDING"
  IN_PROGRESS = "IN_PROGRESS"
  COMPLETED = "COMPLETED"
  UNKNOWN = "UNKNOWN"


class AssessmentDTO(BaseModel):
  id: str
  status: AssessmentStatusDTO
  score: int | None
  questions: list[QuestionDTO]
  started_on: str | None
  completed_on: str | None
  topic_id: str


class AnswerQuestionRequestDTO(BaseModel):
  question_id: str
  selected_answer: str


class StartAssessmentResponseDTO(BaseModel):
  assessment_id: str


class CompleteAssessmentResponseDTO(BaseModel):
  assessment_id: str


class AnswerQuestionResponseDTO(BaseModel):
  assessment_id: str
  question_id: str


class AssessmentResponseDTO(BaseModel):
  id: str
  questions: list[QuestionResponseDTO]
