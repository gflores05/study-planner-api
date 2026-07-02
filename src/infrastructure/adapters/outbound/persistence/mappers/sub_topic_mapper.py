import uuid

from src.domain.sub_topic.sub_topic import SubTopic
from src.domain.sub_topic.value_objects.sub_topic_id import SubTopicId
from src.domain.sub_topic.value_objects.sub_topic_title import SubTopicTitle
from src.domain.topic.value_objects.topic_id import TopicId
from src.domain.value_objects.non_empty_string import NonEmptyString
from src.infrastructure.adapters.outbound.persistence.models.sub_topic_model import (
  SubTopicModel,
)


def map_sub_topic_model_to_domain(model: SubTopicModel) -> SubTopic:
  return SubTopic.reconstitute(
    id=SubTopicId.parse(str(model.id)).unwrap_or_raise(),
    created_on=model.created_on,
    modified_on=model.modified_on,
    version=model.version,
    title=SubTopicTitle.parse(model.title).unwrap_or_raise(),
    study_material=[
      NonEmptyString.parse(sm).unwrap_or_raise() for sm in model.study_material
    ],
    topic_id=TopicId.parse(str(model.topic_id)).unwrap_or_raise(),
  )


def map_sub_topic_domain_to_model(domain: SubTopic) -> SubTopicModel:
  return SubTopicModel(
    id=uuid.UUID(str(domain.id)),
    created_on=domain.created_on,
    modified_on=domain.modified_on,
    version=domain.version,
    title=str(domain.title),
    study_material=[str(sm) for sm in domain.study_material],
    topic_id=uuid.UUID(str(domain.topic_id)),
  )
