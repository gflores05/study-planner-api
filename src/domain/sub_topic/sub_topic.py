from dataclasses import dataclass
from datetime import datetime

from src.domain.sub_topic.value_objects.sub_topic_id import SubTopicId
from src.domain.sub_topic.value_objects.sub_topic_title import SubTopicTitle
from src.domain.topic.value_objects.topic_id import TopicId
from src.domain.value_objects.non_empty_string import NonEmptyString
from src.shared.aggregate_root import AggregateRoot


@dataclass(kw_only=True)
class SubTopic(AggregateRoot[SubTopicId]):
  title: SubTopicTitle
  study_material: list[NonEmptyString]
  topic_id: TopicId

  @staticmethod
  def create(
    title: SubTopicTitle, study_material: list[NonEmptyString], topic_id: TopicId
  ) -> "SubTopic":
    return SubTopic(
      id=SubTopicId.create(),
      title=title,
      study_material=study_material,
      topic_id=topic_id,
    )

  @staticmethod
  def reconstitute(
    id: SubTopicId,
    created_on: datetime,
    modified_on: datetime,
    version: int,
    title: SubTopicTitle,
    study_material: list[NonEmptyString],
    topic_id: TopicId,
  ) -> "SubTopic":
    return SubTopic(
      id=id,
      created_on=created_on,
      modified_on=modified_on,
      version=version,
      title=title,
      study_material=study_material,
      topic_id=topic_id,
    )
