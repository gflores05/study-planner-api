from dataclasses import dataclass

from src.shared.result import Result
from src.shared.validation_error import ValidationError


@dataclass(frozen=True)
class Grade:
  value: int

  @staticmethod
  def parse(value: int) -> "Result[Grade, ValidationError]":
    if value < 1 or value > 12:
      return Result.fail(ValidationError("Grade", value=value))

    return Result.ok(Grade(value=value))

  def __int__(self):
    return self.value
