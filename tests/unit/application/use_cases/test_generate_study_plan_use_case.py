from src.application.dtos.study_plan import GeneratStudyPlanDTO
from src.application.use_cases.study_plan.generate_study_plan_use_case import (
  GenerateStudyPlanUseCase,
)
from src.domain.study_plan.study_plan import StudyPlan, StudyPlanStatus
from src.domain.study_plan.value_objects.subject import Subject
from src.util.date_util import utc_now
from tests.fakes.infrastructure.ai.fake_ai_agent import FakeAIAgent
from tests.fakes.infrastructure.ai.fake_study_plan_prompt_provider import (
  FakeStudyPlanPromptProvider,
)
from tests.fakes.infrastructure.messaging.fake_event_publisher import FakeEventPublisher
from tests.fakes.infrastructure.persistence.repositories.fake_assessment_repository import (
  FakeAssessmentRepository,
)
from tests.fakes.infrastructure.persistence.repositories.fake_question_repository import (
  FakeQuestionRepository,
)
from tests.fakes.infrastructure.persistence.repositories.fake_sub_topic_repository import (
  FakeSubTopicRepository,
)
from tests.fakes.infrastructure.persistence.repositories.fake_topic_repository import (
  FakeTopicRepository,
)
from tests.fakes.infrastructure.persistence.repositories.study_plan_fake_repository import (
  FakeStudyPlanRepository,
)


async def test_generate_study_plan():
  study_plan = StudyPlan.create(
    subject=Subject.parse("Maths").unwrap_or_raise(), level="University"
  )
  study_plan.request(requested_on=utc_now())

  study_plan_repository = FakeStudyPlanRepository(data=[study_plan])
  topic_repository = FakeTopicRepository([])
  sub_topic_repository = FakeSubTopicRepository([])
  assessment_repository = FakeAssessmentRepository([])
  question_repository = FakeQuestionRepository([])

  event_publisher = FakeEventPublisher()

  use_case = GenerateStudyPlanUseCase(
    study_plan_repository=study_plan_repository,
    topic_repository=topic_repository,
    sub_topic_repository=sub_topic_repository,
    assessment_repository=assessment_repository,
    question_repository=question_repository,
    event_publisher=event_publisher,
    ai_agent=FakeAIAgent(),
    study_plan_prompt_provider=FakeStudyPlanPromptProvider(),
  )

  response = await use_case.execute(
    GeneratStudyPlanDTO(study_plan_id=str(study_plan.id))
  )

  updated_study_plan = (await study_plan_repository.get(study_plan.id)).get_or_raise(
    ValueError("StudyPlan")
  )

  assert response.study_plan_id == str(study_plan.id)
  assert updated_study_plan.status == StudyPlanStatus.COMPLETED
  assert len(response.topics) == 2
  assert len(response.topics[0].sub_topics) == 3
  assert len(response.topics[1].sub_topics) == 3
