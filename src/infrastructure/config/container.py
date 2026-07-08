from dependency_injector import containers, providers

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
from src.application.use_cases.study_plan.generate_study_plan_use_case import (
  GenerateStudyPlanUseCaseAdapter,
)
from src.application.use_cases.study_plan.get_study_plan_use_case import (
  GetStudyPlanUseCaseAdapter,
)
from src.application.use_cases.study_plan.request_study_plan_use_case import (
  RequestStudyPlanUseCaseAdapter,
)
from src.infrastructure.adapters.outbound.ai.ai_agent import AIAgent
from src.infrastructure.adapters.outbound.ai.study_plan_prompt_provider import (
  StudyPlanPromptProvider,
)
from src.infrastructure.adapters.outbound.messaging.event_consumer import EventConsumer
from src.infrastructure.adapters.outbound.messaging.event_handlers.study_plan_event_handler import (
  study_plan_requested_event_handler_factory,
)
from src.infrastructure.adapters.outbound.messaging.event_publisher import (
  EventPublisher,
)
from src.infrastructure.adapters.outbound.persistence.repositories.assessment_repository import (
  AssessmentRepository,
)
from src.infrastructure.adapters.outbound.persistence.repositories.question_repository import (
  QuestionRepository,
)
from src.infrastructure.adapters.outbound.persistence.repositories.study_plan_repository import (
  StudyPlanRepository,
)
from src.infrastructure.adapters.outbound.persistence.repositories.sub_topic_repository import (
  SubTopicRepository,
)
from src.infrastructure.adapters.outbound.persistence.repositories.topic_repository import (
  TopicRepository,
)
from src.infrastructure.config.database import Database
from src.infrastructure.config.messaging import MessageBroker
from src.infrastructure.config.settings import Settings


class Container(containers.DeclarativeContainer):
  aaaconfig = providers.Configuration()

  settings = providers.Singleton(Settings)

  db = providers.Singleton(
    Database,
    database_url=settings.provided.database_url,
    db_echo=settings.provided.database_echo,
  )

  message_broker = providers.Singleton(
    MessageBroker,
    rabbitmq_url=settings.provided.rabbitmq_url,
    prefetch_count=settings.provided.rabbitmq_prefetch_count,
  )
  event_queue_name = providers.Object("domain_events_service")
  routing_keys = providers.Object(["study_plan.*"])
  event_consumer = providers.Factory(
    EventConsumer,
    queue_name=event_queue_name,
    routing_keys=routing_keys,
    message_broker=message_broker,
  )
  event_publisher = providers.Factory(EventPublisher, message_broker=message_broker)

  study_plan_repository = providers.Factory(StudyPlanRepository, db=db)
  topic_repository = providers.Factory(TopicRepository, db=db)
  sub_topic_repository = providers.Factory(SubTopicRepository, db=db)
  assessment_repository = providers.Factory(AssessmentRepository, db=db)
  question_repository = providers.Factory(QuestionRepository, db=db)

  ai_agent = providers.Factory(
    AIAgent,
    google_agent_model=settings.provided.google_agent_model,
    exa_api_key=settings.provided.exa_api_key,
  )

  study_plan_prompt_provider = providers.Factory(StudyPlanPromptProvider)

  request_study_plan_use_case = providers.Factory(
    RequestStudyPlanUseCaseAdapter,
    study_plan_repository=study_plan_repository,
    event_publisher=event_publisher,
  )

  generate_study_plan_use_case = providers.Factory(
    GenerateStudyPlanUseCaseAdapter,
    study_plan_repository=study_plan_repository,
    topic_repository=topic_repository,
    sub_topic_repository=sub_topic_repository,
    assessment_repository=assessment_repository,
    question_repository=question_repository,
    event_publisher=event_publisher,
    ai_agent=ai_agent,
    study_plan_prompt_provider=study_plan_prompt_provider,
  )

  get_study_plan_use_case = providers.Factory(
    GetStudyPlanUseCaseAdapter, study_plan_repository=study_plan_repository
  )

  get_assessment_use_Case = providers.Factory(
    GetAssessmentUseCaseAdapter, assessment_repository=assessment_repository
  )

  start_assessment_use_case = providers.Factory(
    StartAssessmentUseCaseAdapter,
    assessment_repository=assessment_repository,
    event_publisher=event_publisher,
  )

  answer_question_use_case = providers.Factory(
    AnswerQuestionUseCaseAdapter,
    assessment_repository=assessment_repository,
    question_repository=question_repository,
    event_publisher=event_publisher,
  )

  complete_assessment_use_case = providers.Factory(
    CompleteAssessmentUseCaseAdapter,
    event_publisher=event_publisher,
    assessment_repository=assessment_repository,
  )

  study_plan_requested_event_handler = providers.Callable(
    study_plan_requested_event_handler_factory, use_case=generate_study_plan_use_case
  )
