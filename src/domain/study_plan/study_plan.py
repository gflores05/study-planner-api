from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Literal

from src.domain.study_plan.domain_events import (
  StudyPlanErrorReported,
  StudyPlanGenerated,
  StudyPlanRequested,
)
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


class StudyPlanProblem:
  def __init__(
    self, current_status: str, required_status: str, study_plan_id: StudyPlanId
  ):
    self.current_status = current_status
    self.required_status = required_status
    self.study_plan_id = str(study_plan_id)


StudyPlanLevel = Literal[
  "Elementary School", "High School", "Preparatory", "University", "Postgraduate"
]


class StudyPlanStatus(Enum):
  PENDING = "PENDING"
  GENERATING = "GENERATING"
  COMPLETED = "COMPLETED"
  UNKNOWN = "UNKNOWN"
  FAILED = "FAILED"


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

  def request(self, requested_on: datetime) -> Result[Unit, StudyPlanProblem]:
    if self.status != StudyPlanStatus.PENDING:
      return Result.fail(
        StudyPlanProblem(
          current_status=self.status.value,
          required_status=StudyPlanStatus.PENDING.value,
          study_plan_id=self.id,
        )
      )

    self.status = StudyPlanStatus.GENERATING

    self.add_domain_event(
      StudyPlanRequested(study_plan_id=str(self.id), requested_on=requested_on)
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

  def report_plan_generated(
    self, generated_on: datetime
  ) -> Result[Unit, StudyPlanProblem]:
    if self.status != StudyPlanStatus.GENERATING:
      return Result.fail(
        StudyPlanProblem(
          current_status=self.status.value,
          required_status=StudyPlanStatus.GENERATING.value,
          study_plan_id=self.id,
        )
      )

    self.modified_on = generated_on
    self.status = StudyPlanStatus.COMPLETED
    self.add_domain_event(
      StudyPlanGenerated(study_plan_id=str(self.id), generated_on=generated_on)
    )

    return Result.ok(Unit)

  def report_failure(self, failed_on: datetime):
    self.modified_on = failed_on
    self.status = StudyPlanStatus.FAILED
    self.add_domain_event(
      StudyPlanErrorReported(study_plan_id=str(self.id), failed_on=failed_on)
    )
