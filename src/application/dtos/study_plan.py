from dataclasses import dataclass
from typing import Literal

from src.application.dtos.topic import TopicDTO

StudyPlanLevelDto = Literal[
  "Elementary School", "High School", "Preparatory", "University", "Postgraduate"
]


@dataclass
class RequestStudyPlanDTO:
  subject: str
  level: StudyPlanLevelDto


@dataclass
class StudyPlanResponseDTO:
  study_plan_id: str


@dataclass
class AddStudyPlanTopics:
  study_plan_id: str
  topics: list[TopicDTO]


@dataclass
class StudyPlanDTO:
  id: str
  subject: str
  level: StudyPlanLevelDto
  topics: list[TopicDTO]
