from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel

from src.application.dtos.topic import TopicAIDTO, TopicDTO, TopicResponseDTO

StudyPlanLevelDto = Literal[
  "Elementary School", "High School", "Preparatory", "University", "Postgraduate"
]


@dataclass
class RequestStudyPlanDTO:
  subject: str
  level: StudyPlanLevelDto
  grade: int


@dataclass
class StudyPlanResponseDTO:
  study_plan_id: str
  topics: list[TopicResponseDTO]


@dataclass
class GenerateStudyPlanDTO:
  study_plan_id: str


class StudyPlanAIGeneratedDTO(BaseModel):
  ts: list[TopicAIDTO]


@dataclass
class StudyPlanDTO:
  id: str
  subject: str
  level: StudyPlanLevelDto
  grade: int
  topics: list[TopicDTO]
