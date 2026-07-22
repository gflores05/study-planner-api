from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.application.dtos.assessment import (
  AnswerQuestionRequestDTO,
  AnswerQuestionResponseDTO,
  AssessmentDTO,
  CompleteAssessmentResponseDTO,
  StartAssessmentResponseDTO,
)
from src.application.use_cases.assessment.answer_question_use_case import (
  AnswerQuestionUseCaseAdapter,
)
from src.application.use_cases.assessment.complete_assessment_use_case import (
  CompleteAssessmentUseCaseAdapter,
)
from src.application.use_cases.assessment.get_assessment_use_case import (
  GetAssessmentUseCaseAdapter,
)
from src.application.use_cases.assessment.start_assessment_use_case import (
  StartAssessmentUseCaseAdapter,
)
from src.infrastructure.config.container import Container

router = APIRouter(prefix="/v1/assessment", tags=["assessment"])


@router.get("/{id}", response_model=AssessmentDTO)
@inject
async def get_assessment(
  id: str,
  use_case: Annotated[
    GetAssessmentUseCaseAdapter, Depends(Provide[Container.get_assessment_use_case])
  ],
) -> AssessmentDTO:
  return await use_case.execute(id=id)


@router.post("/{id}/start", response_model=StartAssessmentResponseDTO)
@inject
async def start_assessment(
  id: str,
  use_case: Annotated[
    StartAssessmentUseCaseAdapter, Depends(Provide[Container.start_assessment_use_case])
  ],
) -> StartAssessmentResponseDTO:
  return await use_case.execute(id=id)


@router.post("/{id}/answer", response_model=AnswerQuestionResponseDTO)
@inject
async def answer_question(
  id: str,
  body: AnswerQuestionRequestDTO,
  use_case: Annotated[
    AnswerQuestionUseCaseAdapter, Depends(Provide[Container.answer_question_use_case])
  ],
) -> AnswerQuestionResponseDTO:
  return await use_case.execute(id, body)


@router.post("/{id}/complete", response_model=CompleteAssessmentResponseDTO)
@inject
async def complete_assessment(
  id: str,
  use_case: Annotated[
    CompleteAssessmentUseCaseAdapter,
    Depends(Provide[Container.complete_assessment_use_case]),
  ],
) -> CompleteAssessmentResponseDTO:
  return await use_case.execute(id=id)
