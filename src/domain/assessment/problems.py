from dataclasses import dataclass


@dataclass
class AssessmentInvalidStatusProblem:
  assessment_id: str
  current_status: str
  required_status: str


@dataclass
class AssessmentQuestionNotFoundProblem:
  assessment_id: str
  question_id: str


AssessmentProblem = AssessmentInvalidStatusProblem | AssessmentQuestionNotFoundProblem
