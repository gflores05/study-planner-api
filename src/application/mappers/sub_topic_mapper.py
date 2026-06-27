from src.application.dtos.sub_topic import SubTopicDTO
from src.domain.sub_topic.sub_topic import SubTopic
from src.domain.sub_topic.value_objects.sub_topic_title import SubTopicTitle
from src.domain.topic.value_objects.topic_id import TopicId
from src.domain.value_objects.non_empty_string import NonEmptyString
from src.shared.result import Result
from src.shared.validation_error import ValidationError
from src.util.result_util import reduce_result


def map_sub_topic_dto_to_domain(dto: SubTopicDTO) -> Result[SubTopic, ValidationError]:
  title_result = SubTopicTitle.parse(dto.title)

  if title_result.is_failure:
    return Result.fail(title_result.error)

  study_material_result = reduce_result(
    [NonEmptyString.parse(material) for material in dto.study_material]
  )

  if study_material_result.is_failure:
    return Result.fail(study_material_result.error)

  topic_id_result = TopicId.parse(dto.topic_id)

  if topic_id_result.is_failure:
    return Result.fail(topic_id_result.error)

  return Result.ok(
    SubTopic.create(
      title=title_result.value,
      study_material=study_material_result.value,
      topic_id=topic_id_result.value,
    )
  )
