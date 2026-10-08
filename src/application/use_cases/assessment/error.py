class AssessmentError(Exception):
  def __init__(self, *args: object) -> None:
    super().__init__(*args)

  def to_dict(self):
    return {"message": str(self)}


class AssessmentInvalidInputError(AssessmentError):
  def __init__(self, value: str, field: str):
    super().__init__("AssessmentInvalidInput")
    self.value = value
    self.field = field

  def to_dict(self):
    return {"message": str(self), "field": self.field, "value": self.value}


class AssessmentNotFoundError(AssessmentError):
  def __init__(self, assessment_id: str):
    super().__init__("AssessmentNotFoundError")
    self.assessment_id = assessment_id

  def to_dict(self):
    return {"message": str(self), "assessment_id": self.assessment_id}


class AssessmentInvalidStatusError(AssessmentError):
  def __init__(self, assessment_id: str, current_status: str, required_status: str):
    super().__init__("AssessmentInvalidStatusProblem")
    self.assessment_id = assessment_id
    self.current_status = current_status
    self.required_status = required_status

  def to_dict(self):
    return {
      "message": str(self),
      "assessment_id": self.assessment_id,
      "current_status": self.current_status,
      "required_status": self.required_status,
    }


class AssessmentQuestionNotFoundError(AssessmentError):
  def __init__(self, assessment_id: str, question_id: str):
    super().__init__("AssessmentQuestionNotFoundError")
    self.assessment_id = assessment_id
    self.question_id = question_id

  def to_dict(self):
    return {
      "message": str(self),
      "assessment_id": self.assessment_id,
      "question_id": self.question_id,
    }


class AssessmentUnknownError(AssessmentError):
  def __init__(self):
    super().__init__("AssessmentUnknownError")

  def to_dict(self):
    return {"message": str(self)}
