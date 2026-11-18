from dataclasses import dataclass

from src.shared.result import Result
from src.shared.validation_error import ValidationError

MAX_NAME_LENGTH = 100


@dataclass(frozen=True)
class Name:
  value: str

  @staticmethod
  def parse(value: str | None) -> Result[Name, ValidationError]:
    if value is None:
      return Result.fail(ValidationError("InvalidName", value=value))

    normalized = value.strip()

    if len(normalized) == 0 or len(normalized) > MAX_NAME_LENGTH:
      return Result.fail(ValidationError("InvalidName", value=value))

    return Result.ok(Name(value=normalized))

  def __str__(self) -> str:
    return self.value
