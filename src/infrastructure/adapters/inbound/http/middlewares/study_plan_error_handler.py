from fastapi import Request
from fastapi.responses import JSONResponse

from src.domain.study_plan.study_plan import StudyPlanError


def study_plan_error_handler(request: Request, ex: Exception):
  if isinstance(ex, StudyPlanError):
    match str(ex.tag):
      case "StudyPlanNotPending":
        return JSONResponse(
          status_code=412,
          content={"message": str(ex), id: ex.study_plan_id},
        )
  return JSONResponse(
    status_code=500,
    content={"message": "Server Error"},
  )
