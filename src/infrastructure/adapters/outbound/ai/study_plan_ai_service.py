from langchain_core.prompts import (
  ChatPromptTemplate,
)
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from src.application.dtos.study_plan import (
  StudyPlanAIGeneratedDTO,
  StudyPlanAIGenerationDTO,
)
from src.infrastructure.adapters.outbound.ai.prompts import (
  GENERATE_STUDY_PLAN_PROMPT,
  SYSTEM_PROMPT,
)
from src.infrastructure.config.settings import Settings


class StudyPlanAIServiceOpenAIAdapter:
  def __init__(self, settings: Settings) -> None:
    self.settings = settings

  def _get_prompts(self):
    return ChatPromptTemplate.from_messages([SYSTEM_PROMPT, GENERATE_STUDY_PLAN_PROMPT])

  async def generate(self, params: StudyPlanAIGenerationDTO) -> StudyPlanAIGeneratedDTO:
    base_model = ChatOpenAI(
      model=self.settings.ai_model,
      temperature=self.settings.ai_temperature,
      api_key=SecretStr(self.settings.openai_api_key),
    )

    prompt = self._get_prompts()

    structured_model = base_model.with_structured_output(StudyPlanAIGeneratedDTO)

    chain = prompt | structured_model

    result = chain.invoke(params.model_dump())

    if isinstance(result, StudyPlanAIGeneratedDTO):
      return result
    return StudyPlanAIGeneratedDTO.model_validate(result)
