import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.application.use_cases.assessment.error import (
  AssessmentError,
  AssessmentInvalidInputError,
  AssessmentInvalidStatusError,
  AssessmentNotFoundError,
  AssessmentQuestionNotFoundError,
)
from src.application.use_cases.study_plan.errors import (
  StudyPlanError,
  StudyPlanInternalError,
  StudyPlanInvalidInputError,
  StudyPlanInvalidStatusError,
  StudyPlanNotFoundError,
)
from src.application.use_cases.topic.error import (
  TopicError,
  TopicInvalidInputError,
  TopicNotFoundError,
  TopicUnknownError,
)
from src.application.use_cases.user.error import (
  UserAlreadyExists,
  UserError,
  UserInvalidCredentials,
  UserInvalidInputError,
  UserInvalidToken,
  UserNotFoundError,
  UserUnknownError,
)

logger = logging.getLogger(__name__)

_ASSESSMENT_STATUS_BY_ERROR: dict[type[AssessmentError], int] = {
  AssessmentInvalidInputError: status.HTTP_400_BAD_REQUEST,
  AssessmentNotFoundError: status.HTTP_404_NOT_FOUND,
  AssessmentQuestionNotFoundError: status.HTTP_404_NOT_FOUND,
  AssessmentInvalidStatusError: status.HTTP_412_PRECONDITION_FAILED,
}

_STUDY_PLAN_STATUS_BY_ERROR: dict[type[StudyPlanError], int] = {
  StudyPlanInvalidInputError: status.HTTP_400_BAD_REQUEST,
  StudyPlanNotFoundError: status.HTTP_404_NOT_FOUND,
  StudyPlanInvalidStatusError: status.HTTP_412_PRECONDITION_FAILED,
  StudyPlanInternalError: status.HTTP_500_INTERNAL_SERVER_ERROR,
}

_TOPIC_STATUS_BY_ERROR: dict[type[TopicError], int] = {
  TopicInvalidInputError: status.HTTP_400_BAD_REQUEST,
  TopicNotFoundError: status.HTTP_404_NOT_FOUND,
  TopicUnknownError: status.HTTP_500_INTERNAL_SERVER_ERROR,
}
_USER_STATUS_BY_ERROR: dict[type[UserError], int] = {
  UserError: status.HTTP_400_BAD_REQUEST,
  UserInvalidInputError: status.HTTP_400_BAD_REQUEST,
  UserNotFoundError: status.HTTP_404_NOT_FOUND,
  UserAlreadyExists: status.HTTP_409_CONFLICT,
  UserUnknownError: status.HTTP_500_INTERNAL_SERVER_ERROR,
  UserInvalidCredentials: status.HTTP_401_UNAUTHORIZED,
  UserInvalidToken: status.HTTP_401_UNAUTHORIZED,
}


def register_error_handlers(app: FastAPI) -> None:
  @app.exception_handler(AssessmentError)
  async def handle_assessment_error(
    request: Request, exc: AssessmentError
  ) -> JSONResponse:
    status_code = _ASSESSMENT_STATUS_BY_ERROR.get(type(exc), 500)
    logger.warning(
      "AssessmentError handling %s %s: %s", request.method, request.url.path, exc
    )
    return JSONResponse(
      status_code=status_code,
      content={
        "error": type(exc).__name__,
        "message": str(exc),
        "data": exc.to_dict(),
      },
    )

  @app.exception_handler(StudyPlanError)
  async def handle_study_plan_error(
    request: Request, exc: StudyPlanError
  ) -> JSONResponse:
    status_code = _STUDY_PLAN_STATUS_BY_ERROR.get(type(exc), 500)
    logger.warning(
      "StudyPlanError handling %s %s: %s", request.method, request.url.path, exc
    )
    return JSONResponse(
      status_code=status_code,
      content={
        "error": type(exc).__name__,
        "message": str(exc),
        "data": exc.to_dict(),
      },
    )

  @app.exception_handler(TopicError)
  async def handle_topic_error(request: Request, exc: TopicError) -> JSONResponse:
    status_code = _TOPIC_STATUS_BY_ERROR.get(type(exc), 500)
    logger.warning(
      "TopicError handling %s %s: %s", request.method, request.url.path, exc
    )
    return JSONResponse(
      status_code=status_code,
      content={
        "error": type(exc).__name__,
        "message": str(exc),
        "data": exc.to_dict(),
      },
    )

  @app.exception_handler(UserError)
  async def handle_user_error(request: Request, exc: UserError) -> JSONResponse:
    status_code = _USER_STATUS_BY_ERROR.get(type(exc), 500)
    logger.warning(
      "UserError handling %s %s: %s", request.method, request.url.path, exc
    )
    return JSONResponse(
      status_code=status_code,
      content={
        "error": type(exc).__name__,
        "message": str(exc),
        "data": exc.to_dict(),
      },
    )
