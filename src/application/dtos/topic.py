from dataclasses import dataclass

from pydantic import BaseModel, Field

from src.application.dtos.assessment import AssessmentDTO, AssessmentResponseDTO
from src.application.dtos.question import QuestionAIDTO
from src.application.dtos.sub_topic import (
  SubTopicAIDTO,
  SubTopicDTO,
  SubTopicResponseDTO,
)


class TopicDTO(BaseModel):
  id: str
  title: str
  sub_topics: list[SubTopicDTO]
  assessment: AssessmentDTO | None
  study_plan_id: str
  created_on: str
  created_by_user_id: str


class TopicAIDTO(BaseModel):
  t: str = Field(description="The topic title")
  st: list[SubTopicAIDTO] = Field(description="List of sub-topics")
  qs: list[QuestionAIDTO] = Field(
    description="List of 15 questions to evaluate the topic"
  )


@dataclass
class TopicResponseDTO:
  id: str
  assessment: AssessmentResponseDTO
  sub_topics: list[SubTopicResponseDTO]
