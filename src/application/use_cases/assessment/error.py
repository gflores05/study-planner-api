class AssessmentError(Exception):
  def __init__(self, *args: object) -> None:
    super().__init__(*args)


class AssessmentInvalidInputError(AssessmentError):
  def __init__(self, value: str, field: str):
    super().__init__("AssessmentInvalidInput")
    self.value = value
    self.field = field


class AssessmentNotFoundError(AssessmentError):
  def __init__(self, assessment_id: str):
    super().__init__("AssessmentNotFoundError")
    self.assessment_id = assessment_id


class AssessmentInvalidStatusError(AssessmentError):
  def __init__(self, assessment_id: str, current_status: str, required_status: str):
    super().__init__("AssessmentInvalidStatusProblem")
    self.assessment_id = assessment_id
    self.current_status = current_status
    self.required_status = required_status


class AssessmentQuestionNotFoundError(AssessmentError):
  def __init__(self, assessment_id: str, question_id: str):
    super().__init__("AssessmentQuestionNotFoundError")
    self.assessment_id = assessment_id
    self.question_id = question_id


class AssessmentUnknownError(AssessmentError):
  def __init__(self):
    super().__init__("AssessmentUnknownError")
