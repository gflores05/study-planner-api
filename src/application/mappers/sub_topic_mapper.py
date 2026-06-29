from src.application.dtos.sub_topic import SubTopicDTO
from src.domain.sub_topic.sub_topic import SubTopic
from src.domain.sub_topic.value_objects.sub_topic_title import SubTopicTitle
from src.domain.topic.value_objects.topic_id import TopicId
from src.domain.value_objects.non_empty_string import NonEmptyString
from src.shared.result import Result
from src.shared.validation_error import ValidationError
from src.util.result_util import traverse


def map_sub_topic_dto_to_domain(dto: SubTopicDTO) -> Result[SubTopic, ValidationError]:
  return Result.ok(
    SubTopic.create(
      title=SubTopicTitle.parse(dto.title).unwrap_or_raise(),
      study_material=traverse(
        [NonEmptyString.parse(material) for material in dto.study_material]
      ).unwrap_or_raise(),
      topic_id=TopicId.parse(dto.topic_id).unwrap_or_raise(),
    )
  )


def map_sub_topic_domain_to_dto(domain: SubTopic) -> SubTopicDTO:
  return SubTopicDTO(
    id=str(domain.id),
    title=str(domain.title),
    study_material=[str(sm) for sm in domain.study_material],
    topic_id=str(domain.topic_id),
  )
