from dataclasses import dataclass
from datetime import datetime

from src.domain.assessment.assessment import Assessment
from src.domain.study_plan.value_objects.study_plan_id import StudyPlanId
from src.domain.sub_topic.sub_topic import SubTopic
from src.domain.sub_topic.value_objects.sub_topic_title import SubTopicTitle
from src.domain.topic.domain_events import TopicAssessmentGenerated
from src.domain.topic.value_objects.topic_id import TopicId
from src.domain.topic.value_objects.topic_title import TopicTitle
from src.domain.value_objects.non_empty_string import NonEmptyString
from src.shared.aggregate_root import AggregateRoot
from src.shared.option import Option


@dataclass
class AddSubTopicParams:
  title: SubTopicTitle
  study_material: list[NonEmptyString]


@dataclass(kw_only=True)
class Topic(AggregateRoot[TopicId]):
  title: TopicTitle
  sub_topics: list[SubTopic]
  assessment: Option[Assessment]
  study_plan_id: StudyPlanId

  @staticmethod
  def create(
    title: TopicTitle,
    sub_topics: list[SubTopic],
    study_plan_id: StudyPlanId,
    assessment: Option[Assessment] = Option.nothing(),
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
      assessment=Option.some(assessment),
      study_plan_id=study_plan_id,
    )

  def add_sub_topic(self, params: AddSubTopicParams) -> SubTopic:
    sub_topic = SubTopic.create(
      title=params.title, study_material=params.study_material, topic_id=self.id
    )

    self.sub_topics.append(sub_topic)

    return sub_topic

  def generate_assessment(self, generated_on: datetime) -> Assessment:
    self.modified_on = generated_on
    self.assessment = Option.some(Assessment.create(questions=[], topic_id=self.id))

    self.add_domain_event(
      TopicAssessmentGenerated(
        topic_id=self.id, assessment=self.assessment.get(), generated_on=generated_on
      )
    )

    return self.assessment.get()
