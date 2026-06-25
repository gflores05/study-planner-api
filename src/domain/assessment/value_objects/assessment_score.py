from dataclasses import dataclass

from shared.result import Result


@dataclass(frozen=True)
class AssessmentScore:
  value: int

  @staticmethod
  def create(value: int) -> Result["AssessmentScore"]:
    if value < 0 or value > 10:
      return Result.fail("The score should be between 0 and 10 points")

    return Result.ok(AssessmentScore(value=value))
