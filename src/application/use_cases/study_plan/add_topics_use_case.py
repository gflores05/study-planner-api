from src.application.dtos.study_plan import (
  AddStudyPlanTopics,
  StudyPlanResponseDTO,
)
from src.application.mappers.topic_mapper import map_topic_dto_to_domain
from src.application.ports.outbound.messaging.event_publisher import EventPublisher
from src.application.ports.outbound.repositories.study_plan_repository import (
  StudyPlanRepository,
)
from src.application.use_cases.use_case_event_publisher import UseCaseEventPublisher
from src.domain.study_plan.value_objects.study_plan_id import StudyPlanId
from src.util.date_util import utc_now
from src.util.result_util import reduce_result


class AddTopicsUseCase(UseCaseEventPublisher):
  def __init__(
    self,
    study_plan_repository: StudyPlanRepository,
    event_publisher: EventPublisher,
  ):
    self.study_plan_repository = study_plan_repository
    self.event_publisher = event_publisher

  async def execute(self, dto: AddStudyPlanTopics) -> StudyPlanResponseDTO:
    study_plan_result = await self.study_plan_repository.get(
      StudyPlanId(dto.study_plan_id)
    )

    if study_plan_result.is_nothing:
      raise ValueError("StudyPlanNotFound")

    study_plan = study_plan_result.get()

    topics_result = reduce_result([map_topic_dto_to_domain(t) for t in dto.topics])

    if topics_result.is_failure:
      raise topics_result.error

    study_plan.add_topics(topics=topics_result.value, generated_on=utc_now())

    await self.study_plan_repository.save(study_plan=study_plan)

    await self._publish_events(study_plan)

    return StudyPlanResponseDTO(study_plan_id=str(study_plan.id))
