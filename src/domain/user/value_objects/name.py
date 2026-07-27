from dataclasses import dataclass

from src.shared.result import Result
from src.shared.validation_error import ValidationError


@dataclass(frozen=True)
class Name:
  value: str

  @staticmethod
  def parse(value: str) -> Result["Name", ValidationError]:
    if value is None or len(value) == 0:
      return Result.fail(ValidationError("InvalidName", value=value))

    return Result.ok(Name(value=value))

  def __str__(self) -> str:
    return self.value
