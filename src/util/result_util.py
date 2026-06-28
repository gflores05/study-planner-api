from src.shared.result import Result


def reduce_result[T, E](results: list[Result[T, E]]) -> Result[list[T], E]:
  fail = next((result for result in results if result.is_failure), None)

  if fail is not None:
    return Result.fail(fail.error)

  return Result.ok([result.value for result in results])
