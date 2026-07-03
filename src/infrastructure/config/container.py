from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.ports.inbound.study_plan.request_study_plan_use_case import (
  RequestStudyPlanUseCasePort,
)
from src.application.ports.outbound.messaging.event_publisher import EventPublisherPort
from src.application.use_cases.study_plan.request_study_plan_use_case import (
  RequestStudyPlanUseCaseAdapter,
)
from src.infrastructure.adapters.outbound.persistence.repositories.study_plan_repository import (
  StudyPlanRepository,
)
from src.infrastructure.config.database import get_session
from src.infrastructure.config.messaging import get_event_publisher


def request_study_plan_use_case(
  session: AsyncSession = Depends(get_session),
  event_publisher: EventPublisherPort = Depends(get_event_publisher),
) -> RequestStudyPlanUseCasePort:
  return RequestStudyPlanUseCaseAdapter(
    study_plan_repository=StudyPlanRepository(session=session),
    event_publisher=event_publisher,
  )
