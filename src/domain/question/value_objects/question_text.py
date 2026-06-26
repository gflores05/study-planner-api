from dataclasses import dataclass

from shared.result import Result


@dataclass(frozen=True)
class QuestionText:
  value: str

  @staticmethod
  def create(value: str) -> Result["QuestionText"]:
    if len(value) == 0:
      return Result.fail("The question cannot be empty")

    return Result.ok(QuestionText(value=value))

  def __str__(self) -> str:
    return self.value
