from dataclasses import dataclass

from src.domain.assessment.assessment import Assessment
from src.domain.sub_topic.value_objects.sub_topic_id import SubTopicId
from src.domain.sub_topic.value_objects.sub_topic_title import SubTopicTitle
from src.domain.value_objects.non_empty_string import NonEmptyString
from src.shared.aggregate_root import AggregateRoot


@dataclass(kw_only=True)
class SubTopic(AggregateRoot[SubTopicId]):
  title: SubTopicTitle
  study_material: list[NonEmptyString]
  assessment: Assessment

  @staticmethod
  def create(
    title: SubTopicTitle,
    study_material: list[NonEmptyString],
    assessment: Assessment,
  ) -> "SubTopic":
    return SubTopic(
      id=SubTopicId.create(),
      title=title,
      study_material=study_material,
      assessment=assessment,
    )

  @staticmethod
  def reconstitute(
    id: SubTopicId,
    title: SubTopicTitle,
    study_material: list[NonEmptyString],
    assessment: Assessment,
  ) -> "SubTopic":
    return SubTopic(
      id=id, title=title, study_material=study_material, assessment=assessment
    )
