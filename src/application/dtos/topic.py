from dataclasses import dataclass

from src.application.dtos.assessment import AssessmentDTO
from src.application.dtos.sub_topic import SubTopicDTO


@dataclass
class TopicDTO:
  id: str
  title: str
  sub_topics: list[SubTopicDTO]
  assessment: AssessmentDTO
  study_plan_id: str
