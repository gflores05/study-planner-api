from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from src.application.dtos.study_plan import RequestStudyPlanDTO, StudyPlanLevelDto
from src.application.ports.inbound.study_plan.request_study_plan_use_case import (
  RequestStudyPlanUseCasePort,
)
from src.domain.study_plan.study_plan import StudyPlanError
from src.infrastructure.config.container import request_study_plan_use_case


class RequestStudyPlanRequest(BaseModel):
  subject: str
  level: str
  grade: int


class RequestStudyPlanResponse(BaseModel):
  study_plan_id: str


study_plan_router = APIRouter(prefix="/study-plan", tags=["study-plan"])


def map_level(level: str) -> StudyPlanLevelDto:
  match level:
    case "Elementary School":
      return "Elementary School"
    case "High School":
      return "High School"
    case "Preparatory":
      return "Preparatory"
    case "University":
      return "University"
    case "Postgraduate":
      return "Postgraduate"

  return "University"


@study_plan_router.post("/request", response_model=RequestStudyPlanResponse)
async def request_study_plan(
  req: RequestStudyPlanRequest,
  use_case: RequestStudyPlanUseCasePort = Depends(request_study_plan_use_case),
) -> RequestStudyPlanResponse:
  try:
    dto = await use_case.execute(
      dto=RequestStudyPlanDTO(
        subject=req.subject, level=map_level(req.level), grade=req.grade
      )
    )

    return RequestStudyPlanResponse(study_plan_id=dto.study_plan_id)

  except StudyPlanError as e:
    raise HTTPException(
      status_code=status.HTTP_412_PRECONDITION_FAILED,
      detail=str(e),
    )
