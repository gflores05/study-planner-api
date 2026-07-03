from dataclasses import dataclass

from src.shared.result import Result
from src.shared.validation_error import ValidationError


@dataclass(frozen=True)
class QuestionText:
  value: str

  @staticmethod
  def parse(value: str) -> Result["QuestionText", ValidationError]:
    if len(value) == 0:
      return Result.fail(ValidationError("EmptyText", value=value))

    return Result.ok(QuestionText(value=value))

  def __str__(self) -> str:
    return self.value
