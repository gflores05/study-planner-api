from src.application.dtos.assessment import AssessmentDTO
from src.application.mappers.question_mapper import map_question_dto_to_domain
from src.domain.assessment.assessment import Assessment
from src.domain.topic.value_objects.topic_id import TopicId
from src.shared.result import Result
from src.shared.validation_error import ValidationError
from src.util.result_util import reduce_result


def map_assessment_dto_to_domain(
  dto: AssessmentDTO,
) -> Result[Assessment, ValidationError]:
  questions_result = reduce_result(
    [map_question_dto_to_domain(questionDTO) for questionDTO in dto.questions]
  )

  if questions_result.is_failure:
    return Result.fail(questions_result.error)

  topic_id_result = TopicId.parse(dto.topic_id)

  if topic_id_result.is_failure:
    return Result.fail(topic_id_result.error)

  return Result.ok(
    Assessment.create(questions=questions_result.value, topic_id=topic_id_result.value)
  )
