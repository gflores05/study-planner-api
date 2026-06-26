from dataclasses import dataclass
from typing import Literal

from src.application.dtos.topic import TopicDTO

StudyPlanLevelDto = Literal[
  "Elementary School", "High School", "Preparatory", "University", "Postgraduate"
]


@dataclass
class GenerateStudyPlanRequestDTO:
  subject: str
  level: StudyPlanLevelDto


@dataclass
class GenerateStudyPlanResponseDTO:
  study_plan_id: str


@dataclass
class StudyPlanDTO:
  id: str
  subject: str
  level: StudyPlanLevelDto
  topics: list[TopicDTO]
