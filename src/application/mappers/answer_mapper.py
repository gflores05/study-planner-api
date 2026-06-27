from src.application.dtos.answer import AnswerDTO
from src.domain.answer.answer import Answer
from src.domain.answer.value_objects.answer_option import AnswerOption
from src.domain.value_objects.non_empty_string import NonEmptyString
from src.shared.result import Result
from src.shared.validation_error import ValidationError


def map_answer_dto_to_domain(dto: AnswerDTO) -> Result[Answer, ValidationError]:
  text_result = NonEmptyString.parse(dto.text)

  if text_result.is_failure:
    return Result.fail(text_result.error)

  option_result = AnswerOption.parse(dto.option)

  if option_result.is_failure:
    return Result.fail(option_result.error)

  return Result.ok(
    Answer.create(
      text=text_result.value,
      option=option_result.value,
    )
  )
