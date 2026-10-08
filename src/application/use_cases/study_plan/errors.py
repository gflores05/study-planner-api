class StudyPlanError(Exception):
  def __init__(self, *args: object) -> None:
    super().__init__(*args)

  def to_dict(self) -> dict[str, object]:
    return self.__dict__


class StudyPlanInvalidInputError(StudyPlanError):
  def __init__(self, value: str, field: str) -> None:
    super().__init__("StudyPlanInvalidInput")
    self.value = value
    self.field = field

  def to_dict(self) -> dict[str, object]:
    return {"message": str(self), "value": self.value, "field": self.field}


class StudyPlanNotFoundError(StudyPlanError):
  def __init__(self, study_plan_id: str) -> None:
    super().__init__("StudyPlanNotFoundError")
    self.study_plan_id = study_plan_id

  def to_dict(self) -> dict[str, object]:
    return {"message": str(self), "study_plan_id": self.study_plan_id}


class StudyPlanInvalidStatusError(StudyPlanError):
  def __init__(
    self, study_plan_id: str, current_status: str, required_status: str
  ) -> None:
    super().__init__("StudyPlanInvalidStatusError")
    self.study_plan_id = study_plan_id
    self.current_status = current_status
    self.required_status = required_status

  def to_dict(self) -> dict[str, object]:
    return {
      "message": str(self),
      "study_plan_id": self.study_plan_id,
      "current_status": self.current_status,
      "required_status": self.required_status,
    }


class StudyPlanInternalError(StudyPlanError):
  def __init__(self, message: str) -> None:
    super().__init__("StudyPlanInternalError")
    self.message = message

  def to_dict(self) -> dict[str, object]:
    return {"message": str(self), "error": self.message}
