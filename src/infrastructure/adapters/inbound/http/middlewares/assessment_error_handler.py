from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.application.use_cases.assessment.error import (
  AssessmentInvalidInputError,
  AssessmentInvalidStatusError,
  AssessmentNotFoundError,
  AssessmentQuestionNotFoundError,
)


def assessment_error_handler(request: Request, ex: Exception):
  match ex:
    case AssessmentInvalidInputError():
      return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": str(ex), "field": ex.field, "value": ex.value},
      )
    case AssessmentNotFoundError():
      return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": str(ex), "id": ex.assessment_id},
      )
    case AssessmentQuestionNotFoundError():
      return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": str(ex), "id": ex.question_id},
      )
    case AssessmentInvalidStatusError():
      return JSONResponse(
        status_code=status.HTTP_412_PRECONDITION_FAILED,
        content={
          "message": str(ex),
          "id": ex.assessment_id,
          "current_status": ex.current_status,
          "required_status": ex.required_status,
        },
      )
  return JSONResponse(
    status_code=500,
    content={"message": "Server Error"},
  )
