from dotenv import load_dotenv
from langsmith import Client

from src.application.ports.outbound.ai.prompt_provider import Prompts
from src.application.use_cases.study_plan.generate_study_plan_use_case import (
  StudyPlanPromptParams,
)

load_dotenv()


class StudyPlanPromptProvider:
  def __init__(self) -> None:
    self._client = Client()

  async def get_prompts(self, params: StudyPlanPromptParams) -> Prompts:
    prompt = self._client.pull_prompt(
      "generate_study_plan",
    )

    content = prompt.invoke(
      {"grade": params.grade, "level": params.level, "subject": params.subject}
    )

    messages = content.to_messages()

    return Prompts(system=messages[0].text, human=messages[1].text)
