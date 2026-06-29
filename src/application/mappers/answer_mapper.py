from src.application.dtos.answer import AnswerDTO
from src.domain.answer.answer import Answer
from src.domain.answer.value_objects.answer_option import AnswerOption
from src.domain.value_objects.non_empty_string import NonEmptyString
from src.shared.result import Result
from src.shared.validation_error import ValidationError


def map_answer_dto_to_domain(dto: AnswerDTO) -> Result[Answer, ValidationError]:
  return Result.ok(
    Answer.create(
      text=NonEmptyString.parse(dto.text).unwrap_or_raise(),
      option=AnswerOption.parse(dto.option).unwrap_or_raise(),
    )
  )


def map_answer_domain_to_dto(domain: Answer) -> AnswerDTO:
  return AnswerDTO(id=str(domain.id), text=str(domain.text), option=str(domain.option))
