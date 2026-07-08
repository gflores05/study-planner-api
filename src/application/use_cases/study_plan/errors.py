class StudyPlanError(Exception):
  def __init__(self, *args: object) -> None:
    super().__init__(*args)


class StudyPlanInvalidInputError(StudyPlanError):
  def __init__(self, value: str, field: str) -> None:
    super().__init__("StudyPlanInvalidInput")
    self.value = value
    self.field = field


class StudyPlanNotFoundError(StudyPlanError):
  def __init__(self, study_plan_id: str) -> None:
    super().__init__("StudyPlanNotFoundError")
    self.study_plan_id = study_plan_id


class StudyPlanInvalidStatusError(StudyPlanError):
  def __init__(
    self, study_plan_id: str, current_status: str, required_status: str
  ) -> None:
    super().__init__("StudyPlanInvalidStatusError")
    self.study_plan_id = study_plan_id
    self.current_status = current_status
    self.required_status = required_status
