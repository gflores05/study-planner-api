from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Literal

from src.domain.study_plan.domain_events import StudyPlanGenerated, StudyPlanRequested
from src.domain.study_plan.value_objects.grade import Grade
from src.domain.study_plan.value_objects.study_plan_id import StudyPlanId
from src.domain.study_plan.value_objects.subject import Subject
from src.domain.topic.topic import Topic
from src.domain.topic.value_objects.topic_title import TopicTitle
from src.shared.aggregate_root import AggregateRoot
from src.shared.result import Result, Unit


@dataclass
class AddTopicParams:
  title: TopicTitle


class StudyPlanError(Exception):
  def __init__(self, tag: Literal["StudyPlanNotPending"], study_plan_id: StudyPlanId):
    super().__init__(tag)
    self.tag = tag
    self.study_plan_id = str(study_plan_id)


StudyPlanLevel = Literal[
  "Elementary School", "High School", "Preparatory", "University", "Postgraduate"
]


class StudyPlanStatus(Enum):
  PENDING = "PENDING"
  GENERATING = "GENERATING"
  COMPLETED = "COMPLETED"
  UNKNOWN = "UNKNOWN"


@dataclass(kw_only=True)
class StudyPlan(AggregateRoot[StudyPlanId]):
  subject: Subject
  level: StudyPlanLevel
  topics: list[Topic]
  grade: Grade
  status: StudyPlanStatus

  @staticmethod
  def create(subject: Subject, level: StudyPlanLevel, grade: Grade) -> "StudyPlan":
    return StudyPlan(
      id=StudyPlanId.create(),
      subject=subject,
      topics=[],
      level=level,
      status=StudyPlanStatus.PENDING,
      grade=grade,
    )

  @staticmethod
  def reconstitute(
    id: StudyPlanId,
    created_on: datetime,
    modified_on: datetime,
    version: int,
    subject: Subject,
    level: StudyPlanLevel,
    topics: list[Topic],
    status: StudyPlanStatus,
    grade: Grade,
  ) -> "StudyPlan":
    return StudyPlan(
      id=id,
      created_on=created_on,
      modified_on=modified_on,
      version=version,
      subject=subject,
      level=level,
      topics=topics,
      status=status,
      grade=grade,
    )

  def request(self, requested_on: datetime) -> Result[Unit, StudyPlanError]:
    if self.status != StudyPlanStatus.PENDING:
      return Result.fail(
        StudyPlanError(tag="StudyPlanNotPending", study_plan_id=self.id)
      )

    self.status = StudyPlanStatus.GENERATING

    self.add_domain_event(
      StudyPlanRequested(study_plan_id=self.id, requested_on=requested_on)
    )

    return Result.ok(Unit)

  def add_topic(self, params: AddTopicParams):
    topic = Topic.create(
      title=params.title,
      sub_topics=[],
      study_plan_id=self.id,
    )
    self.topics.append(topic)

    return topic

  def report_plan_generated(self, generated_on: datetime):
    self.modified_on = generated_on
    self.status = StudyPlanStatus.COMPLETED
    self.add_domain_event(
      StudyPlanGenerated(study_plan_id=self.id, generated_on=generated_on)
    )
