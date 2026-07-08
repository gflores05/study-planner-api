from src.application.dtos.study_plan import GenerateStudyPlanDTO
from src.application.ports.inbound.study_plan.generate_study_plan_use_case import (
  GenerateStudyPlanUseCasePort,
)


async def study_plan_requested_event_handler_factory(
  use_case: GenerateStudyPlanUseCasePort,
):
  async def handle(payload: dict):
    await use_case.execute(GenerateStudyPlanDTO(study_plan_id=payload["study_plan_id"]))

  return handle
