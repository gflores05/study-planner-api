from src.application.dtos.topic import TopicDTO
from src.application.mappers.assessment_mapper import map_assessment_dto_to_domain
from src.application.mappers.sub_topic_mapper import map_sub_topic_dto_to_domain
from src.domain.study_plan.value_objects.study_plan_id import StudyPlanId
from src.domain.topic.topic import Topic
from src.domain.topic.value_objects.topic_title import TopicTitle
from src.shared.result import Result
from src.shared.validation_error import ValidationError
from src.util.result_util import reduce_result


def map_topic_dto_to_domain(dto: TopicDTO) -> Result[Topic, ValidationError]:
  title_result = TopicTitle.parse(dto.title)

  if title_result.is_failure:
    return Result.fail(title_result.error)

  sub_topics_result = reduce_result(
    [map_sub_topic_dto_to_domain(st) for st in dto.sub_topics]
  )

  if sub_topics_result.is_failure:
    return Result.fail(sub_topics_result.error)

  assessment_result = map_assessment_dto_to_domain(dto.assessment)

  if assessment_result.is_failure:
    return Result.fail(assessment_result.error)

  study_plan_id_result = StudyPlanId.parse(dto.study_plan_id)

  if study_plan_id_result.is_failure:
    return Result.fail(study_plan_id_result.error)

  return Result.ok(
    Topic.create(
      title=title_result.value,
      sub_topics=sub_topics_result.value,
      assessment=assessment_result.value,
      study_plan_id=study_plan_id_result.value,
    )
  )
