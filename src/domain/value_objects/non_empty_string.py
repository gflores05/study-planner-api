from dataclasses import dataclass

from shared.result import Result
from src.shared.validation_error import ValidationError


@dataclass(frozen=True)
class NonEmptyString:
  value: str

  @staticmethod
  def parse(value: str) -> Result["NonEmptyString", ValidationError]:
    if len(value) == 0:
      return Result.fail(ValidationError("EmptyValue", value=value))

    return Result.ok(NonEmptyString(value=value))

  def __str__(self) -> str:
    return self.value
