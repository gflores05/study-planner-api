from src.application.ports.outbound.ai.prompt_provider import Prompts
from src.application.use_cases.study_plan.generate_study_plan_use_case import (
  StudyPlanPromptParams,
)


class FakeStudyPlanPromptProvider:
  async def get_prompts(self, params: StudyPlanPromptParams) -> Prompts:
    return Prompts(system="", human="")
