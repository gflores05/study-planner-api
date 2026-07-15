from src.application.dtos.topic import TopicDTO
from src.application.mappers.assessment_mapper import (
  map_assessment_domain_to_dto,
  map_assessment_dto_to_domain,
)
from src.application.mappers.sub_topic_mapper import (
  map_sub_topic_domain_to_dto,
  map_sub_topic_dto_to_domain,
)
from src.domain.study_plan.value_objects.study_plan_id import StudyPlanId
from src.domain.topic.topic import Topic
from src.domain.topic.value_objects.topic_title import TopicTitle
from src.shared.option import Option
from src.shared.result import Result
from src.shared.validation_error import ValidationError
from src.util.result_util import traverse


def map_topic_dto_to_domain(dto: TopicDTO) -> Result[Topic, ValidationError]:
  return Result.ok(
    Topic.create(
      title=TopicTitle.parse(dto.title).unwrap_or_raise(),
      sub_topics=traverse(
        [map_sub_topic_dto_to_domain(st) for st in dto.sub_topics]
      ).unwrap_or_raise(),
      assessment=map_assessment_dto_to_domain(dto.assessment).to_option()
      if dto.assessment is not None
      else Option.nothing(),
      study_plan_id=StudyPlanId.parse(dto.study_plan_id).unwrap_or_raise(),
    )
  )


def map_topic_domain_to_dto(domain: Topic, include_children: bool = True) -> TopicDTO:
  return TopicDTO(
    id=str(domain.id),
    title=str(domain.title),
    sub_topics=[map_sub_topic_domain_to_dto(st) for st in domain.sub_topics]
    if include_children
    else [],
    assessment=map_assessment_domain_to_dto(domain.assessment.get())
    if include_children and domain.assessment.is_some
    else None,
    study_plan_id=str(domain.study_plan_id),
  )
