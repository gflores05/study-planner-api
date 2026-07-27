import re
from dataclasses import dataclass

from src.shared.result import Result
from src.shared.validation_error import ValidationError


@dataclass(frozen=True)
class Email:
  value: str

  @staticmethod
  def parse(value: str) -> Result["Email", ValidationError]:
    if (
      re.fullmatch(r"^((?!\.)[\w\-_.]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W])$", value) is None
    ):
      return Result.fail(ValidationError("InvalidEmail", value=value))

    return Result.ok(Email(value=value))

  def __str__(self) -> str:
    return self.value
