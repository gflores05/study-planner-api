class FakeStudyPlanPromptProvider:
  async def get_system_prompt(self, params: dict) -> str:
    return ""

  async def get_prompt(self, params: dict) -> str:
    return ""
