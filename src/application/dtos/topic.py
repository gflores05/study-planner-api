from dataclasses import dataclass

from pydantic import BaseModel

from src.application.dtos.assessment import AssessmentDTO, AssessmentResponseDTO
from src.application.dtos.question import QuestionAIDTO
from src.application.dtos.sub_topic import (
  SubTopicAIDTO,
  SubTopicDTO,
  SubTopicResponseDTO,
)


@dataclass
class TopicDTO:
  id: str
  title: str
  sub_topics: list[SubTopicDTO]
  assessment: AssessmentDTO | None
  study_plan_id: str


class TopicAIDTO(BaseModel):
  t: str
  st: list[SubTopicAIDTO]
  qs: list[QuestionAIDTO]


@dataclass
class TopicResponseDTO:
  id: str
  assessment: AssessmentResponseDTO
  sub_topics: list[SubTopicResponseDTO]
