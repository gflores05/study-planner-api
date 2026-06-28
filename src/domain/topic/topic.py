from dataclasses import dataclass
from datetime import datetime

from src.domain.assessment.assessment import Assessment
from src.domain.study_plan.value_objects.study_plan_id import StudyPlanId
from src.domain.sub_topic.sub_topic import SubTopic
from src.domain.topic.domain_events import TopicAssessmentAdded, TopicSubTopicsAdded
from src.domain.topic.value_objects.topic_id import TopicId
from src.domain.topic.value_objects.topic_title import TopicTitle
from src.shared.aggregate_root import AggregateRoot


@dataclass(kw_only=True)
class Topic(AggregateRoot[TopicId]):
  title: TopicTitle
  sub_topics: list[SubTopic]
  assessment: Assessment
  study_plan_id: StudyPlanId

  @staticmethod
  def create(
    title: TopicTitle,
    sub_topics: list[SubTopic],
    assessment: Assessment,
    study_plan_id: StudyPlanId,
  ) -> "Topic":
    return Topic(
      id=TopicId.create(),
      title=title,
      sub_topics=sub_topics,
      assessment=assessment,
      study_plan_id=study_plan_id,
    )

  @staticmethod
  def reconstitute(
    id: TopicId,
    title: TopicTitle,
    sub_topics: list[SubTopic],
    assessment: Assessment,
    study_plan_id: StudyPlanId,
  ) -> "Topic":
    return Topic(
      id=id,
      title=title,
      sub_topics=sub_topics,
      assessment=assessment,
      study_plan_id=study_plan_id,
    )

  def add_sub_topics(self, generated_on: datetime):
    self.modified_on = generated_on

    self.add_domain_event(
      TopicSubTopicsAdded(
        topic_id=self.id, sub_topics=self.sub_topics, generated_on=generated_on
      )
    )

  def add_assessment(self, generated_on: datetime):
    self.modified_on = generated_on

    self.add_domain_event(
      TopicAssessmentAdded(
        topic_id=self.id, assessment=self.assessment, generated_on=generated_on
      )
    )
