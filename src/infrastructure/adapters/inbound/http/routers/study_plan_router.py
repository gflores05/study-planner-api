from typing import Annotated, Literal

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.application.dtos.study_plan import (
  RequestStudyPlanDTO,
  StudyPlanDTO,
  StudyPlanLevelDto,
)
from src.application.use_cases.study_plan.get_study_plan_use_case import (
  GetStudyPlanUseCaseAdapter,
)
from src.application.use_cases.study_plan.request_study_plan_use_case import (
  RequestStudyPlanUseCaseAdapter,
)
from src.infrastructure.config.container import Container


class RequestStudyPlanRequest(BaseModel):
  subject: str
  level: str
  grade: int


class RequestStudyPlanResponse(BaseModel):
  study_plan_id: str


StudyPlanLevel = Literal[
  "Elementary School", "High School", "Preparatory", "University", "Postgraduate"
]

router = APIRouter(prefix="/v1/study-plan", tags=["study-plan"])


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


@router.post("/request", response_model=RequestStudyPlanResponse)
@inject
async def request_study_plan(
  body: RequestStudyPlanRequest,
  use_case: Annotated[
    RequestStudyPlanUseCaseAdapter,
    Depends(Provide[Container.request_study_plan_use_case]),
  ],
) -> RequestStudyPlanResponse:
  dto = await use_case.execute(
    dto=RequestStudyPlanDTO(
      subject=body.subject, level=map_level(body.level), grade=body.grade
    )
  )

  return RequestStudyPlanResponse(study_plan_id=dto.study_plan_id)


@router.get("/{id}", response_model=StudyPlanDTO)
@inject
async def get_study_plan(
  id: str,
  use_case: Annotated[
    GetStudyPlanUseCaseAdapter, Depends(Provide[Container.get_study_plan_use_case])
  ],
) -> StudyPlanDTO:
  return await use_case.execute(id=id)
