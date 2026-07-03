from dataclasses import dataclass

from src.shared.result import Result
from src.shared.validation_error import ValidationError


@dataclass(frozen=True)
class AssessmentScore:
  value: int

  @staticmethod
  def create(value: int) -> "Result[AssessmentScore, ValidationError]":
    if value < 0 or value > 10:
      return Result.fail(ValidationError("ScoreOutOfRange", value=value))

    return Result.ok(AssessmentScore(value=value))

  def __int__(self):
    return self.value
