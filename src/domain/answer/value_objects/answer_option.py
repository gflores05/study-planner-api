from dataclasses import dataclass

from src.shared.result import Result
from src.shared.validation_error import ValidationError


@dataclass(frozen=True)
class AnswerOption:
  value: str

  @staticmethod
  def parse(value: str) -> "Result[AnswerOption, ValidationError]":
    if value not in {"a", "b", "c", "d"}:
      return Result.fail(ValidationError(message="InvalidAnswerOption", value=value))

    return Result.ok(AnswerOption(value=value))

  def __eq__(self, other: "AnswerOption") -> bool:
    return self.value == other.value

  def __str__(self) -> str:
    return self.value
