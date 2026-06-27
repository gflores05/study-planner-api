from src.application.dtos.question import QuestionDTO
from src.application.mappers.answer_mapper import map_answer_dto_to_domain
from src.domain.answer.value_objects.answer_option import AnswerOption
from src.domain.assessment.value_objects.assessment_id import AssessmentId
from src.domain.question.question import Question
from src.domain.question.value_objects.question_text import QuestionText
from src.shared.result import Result
from src.shared.validation_error import ValidationError
from src.util.result_util import reduce_result


def map_question_dto_to_domain(dto: QuestionDTO) -> Result[Question, ValidationError]:
  text_result = QuestionText.parse(dto.text)

  if text_result.is_failure:
    return Result.fail(text_result.error)

  answer_result = AnswerOption.parse(dto.answer)

  if answer_result.is_failure:
    return Result.fail(answer_result.error)

  options_result = reduce_result(
    [map_answer_dto_to_domain(answerDTO) for answerDTO in dto.options]
  )

  if options_result.is_failure:
    return Result.fail(options_result.error)

  assessment_id_result = AssessmentId.parse(dto.assessment_id)

  if assessment_id_result.is_failure:
    return Result.fail(assessment_id_result.error)

  return Result.ok(
    Question.create(
      text=text_result.value,
      options=options_result.value,
      answer=answer_result.value,
      assessment_id=assessment_id_result.value,
    )
  )
