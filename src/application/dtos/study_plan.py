from dataclasses import dataclass
from enum import Enum
from typing import Literal

from pydantic import BaseModel

from src.application.dtos.topic import TopicAIDTO, TopicDTO, TopicResponseDTO

StudyPlanLevelDto = Literal[
  "Elementary School", "High School", "Preparatory", "University", "Postgraduate"
]


class StudyPlanStatusDTO(Enum):
  PENDING = "PENDING"
  GENERATING = "GENERATING"
  COMPLETED = "COMPLETED"
  UNKNOWN = "UNKNOWN"
  FAILED = "FAILED"


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


class StudyPlanDTO(BaseModel):
  id: str
  subject: str
  level: StudyPlanLevelDto
  grade: int
  topics: list[TopicDTO]
  status: StudyPlanStatusDTO
