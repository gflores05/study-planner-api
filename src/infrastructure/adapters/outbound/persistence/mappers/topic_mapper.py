import uuid

from src.domain.study_plan.value_objects.study_plan_id import StudyPlanId
from src.domain.topic.topic import Topic
from src.domain.topic.value_objects.topic_id import TopicId
from src.domain.topic.value_objects.topic_title import TopicTitle
from src.infrastructure.adapters.outbound.persistence.mappers.assessment_mapper import (
  map_assessment_domain_to_model,
  map_assessment_model_to_domain,
)
from src.infrastructure.adapters.outbound.persistence.mappers.sub_topic_mapper import (
  map_sub_topic_domain_to_model,
  map_sub_topic_model_to_domain,
)
from src.infrastructure.adapters.outbound.persistence.models.topic_model import (
  TopicModel,
)


def map_topic_model_to_domain(model: TopicModel) -> Topic:
  return Topic.reconstitute(
    id=TopicId.parse(str(model.id)).unwrap_or_raise(),
    created_on=model.created_on,
    modified_on=model.modified_on,
    version=model.version,
    title=TopicTitle.parse(model.title).unwrap_or_raise(),
    assessment=map_assessment_model_to_domain(model.assessment),
    sub_topics=[map_sub_topic_model_to_domain(st) for st in model.sub_topics],
    study_plan_id=StudyPlanId.parse(str(model.study_plan_id)).unwrap_or_raise(),
  )


def map_topic_domain_to_model(domain: Topic) -> TopicModel:
  return TopicModel(
    id=uuid.UUID(str(domain.id)),
    created_on=domain.created_on,
    modified_on=domain.modified_on,
    version=domain.version,
    title=str(domain.title),
    assessment=map_assessment_domain_to_model(domain.assessment.get())
    if domain.assessment.is_some
    else None,
    sub_topics=[map_sub_topic_domain_to_model(st) for st in domain.sub_topics],
    study_plan_id=uuid.UUID(str(domain.study_plan_id)),
  )
