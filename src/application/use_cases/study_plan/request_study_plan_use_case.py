from src.application.dtos.study_plan import (
  RequestStudyPlanDTO,
  StudyPlanResponseDTO,
)
from src.application.ports.outbound.messaging.event_publisher import EventPublisherPort
from src.application.ports.outbound.repositories.study_plan_repository import (
  StudyPlanRepository,
)
from src.application.use_cases.study_plan.errors import StudyPlanInvalidStatusError
from src.application.use_cases.use_case_event_publisher import UseCaseEventPublisher
from src.domain.study_plan.study_plan import StudyPlan
from src.domain.study_plan.value_objects.grade import Grade
from src.domain.study_plan.value_objects.subject import Subject
from src.util.date_util import utc_now


class RequestStudyPlanUseCaseAdapter(UseCaseEventPublisher):
  def __init__(
    self,
    study_plan_repository: StudyPlanRepository,
    event_publisher: EventPublisherPort,
  ):
    self.study_plan_repository = study_plan_repository
    self.event_publisher = event_publisher

  async def execute(self, dto: RequestStudyPlanDTO) -> StudyPlanResponseDTO:
    study_plan = StudyPlan.create(
      subject=Subject.parse(dto.subject).unwrap_or_raise(),
      level=dto.level,
      grade=Grade.parse(dto.grade).unwrap_or_raise(),
    )

    study_plan.request(utc_now()).unwrap_or_map_and_raise(
      lambda problem: StudyPlanInvalidStatusError(
        study_plan_id=problem.study_plan_id,
        current_status=problem.current_status,
        required_status="PENDING",
      )
    )

    await self.study_plan_repository.save(study_plan=study_plan)

    await self._publish_events(study_plan)

    return StudyPlanResponseDTO(study_plan_id=str(study_plan.id), topics=[])
