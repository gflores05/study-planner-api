from dataclasses import dataclass

from shared.result import Result


@dataclass(frozen=True)
class AnswerOption:
  value: str

  @staticmethod
  def create(value: str) -> Result["AnswerOption"]:
    if value not in {"a", "b", "c", "d"}:
      return Result.fail("The answer option should be a letter from a to d")

    return Result.ok(AnswerOption(value=value))

  def __eq__(self, other: "AnswerOption") -> bool:
    return self.value == other.value
