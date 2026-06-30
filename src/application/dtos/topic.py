from dataclasses import dataclass

from src.application.dtos.assessment import AssessmentDTO
from src.application.dtos.question import QuestionAIDTO
from src.application.dtos.sub_topic import SubTopicAIDTO, SubTopicDTO


@dataclass
class TopicDTO:
  id: str
  title: str
  sub_topics: list[SubTopicDTO]
  assessment: AssessmentDTO | None
  study_plan_id: str


@dataclass
class TopicAIDTO:
  t: str
  st: list[SubTopicAIDTO]
  qs: list[QuestionAIDTO]
