from src.application.dtos.assessment import AssessmentDTO, AssessmentStatusDTO
from src.application.mappers.question_mapper import (
  map_question_domain_to_dto,
  map_question_dto_to_domain,
)
from src.domain.assessment.assessment import Assessment, AssessmentStatus
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


def map_assessment_domain_to_dto(domain: Assessment) -> AssessmentDTO:
  return AssessmentDTO(
    id=str(domain.id),
    status=map_assessment_status_domain_to_dto(domain.status),
    score=int(domain.score.get()) if domain.score.is_some else None,
    questions=[map_question_domain_to_dto(q) for q in domain.questions],
    started_on=domain.started_on.get().isoformat()
    if domain.started_on.is_some
    else None,
    completed_on=domain.completed_on.get().isoformat()
    if domain.completed_on.is_some
    else None,
    topic_id=str(domain.topic_id),
  )


def map_assessment_status_domain_to_dto(
  status: AssessmentStatus,
) -> AssessmentStatusDTO:
  match status:
    case AssessmentStatus.PENDING:
      return AssessmentStatusDTO.PENDING
    case AssessmentStatus.IN_PROGRESS:
      return AssessmentStatusDTO.IN_PROGRESS
    case AssessmentStatus.COMPLETED:
      return AssessmentStatusDTO.COMPLETED
