from dependency_injector import containers, providers

from src.application.messages.domain_event_publisher import DomainEventPublisher
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
from src.application.use_cases.topic.get_topic_use_case import GetTopicUseCaseAdapter
from src.application.use_cases.user.create_user_use_case import CreateUserUseCaseAdapter
from src.infrastructure.adapters.outbound.ai.study_plan_ai_service import (
  StudyPlanAIServiceOpenAIAdapter,
)
from src.infrastructure.adapters.outbound.auth.token_service import TokenService
from src.infrastructure.adapters.outbound.messaging.event_consumer import EventConsumer
from src.infrastructure.adapters.outbound.messaging.event_publisher import (
  EventPublisher,
)
from src.infrastructure.adapters.outbound.messaging.handlers.study_plan_command_handlers import (
  generate_study_plan_command_handler_factory,
  report_study_plan_error_command_handler_factory,
  report_study_plan_generated_command_handler_factory,
)
from src.infrastructure.adapters.outbound.messaging.handlers.study_plan_event_handlers import (
  study_plan_error_reported_event_handler_factory,
  study_plan_generated_event_handler_factory,
  study_plan_requested_event_handler_factory,
)
from src.infrastructure.adapters.outbound.persistence.lookups.user_lookup import (
  UserLookupAdapter,
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
from src.infrastructure.adapters.outbound.persistence.repositories.user_repository import (
  UserRepository,
)
from src.infrastructure.adapters.outbound.websockets.connection_manager import (
  RealtimeConnectionManager,
)
from src.infrastructure.config.database import Database
from src.infrastructure.config.messaging import MessageBroker
from src.infrastructure.config.settings import Settings


class Container(containers.DeclarativeContainer):
  config = providers.Configuration()

  settings = providers.Singleton(Settings)

  db = providers.Singleton(
    Database,
    database_url=settings.provided.database_url,
    db_echo=settings.provided.database_echo,
  )

  realtime_connection_manager = providers.Singleton(RealtimeConnectionManager)

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

  domain_event_publisher = providers.Factory(
    DomainEventPublisher, event_publisher=event_publisher
  )

  study_plan_repository = providers.Factory(
    StudyPlanRepository, db=db, domain_event_publisher=domain_event_publisher
  )
  topic_repository = providers.Factory(
    TopicRepository, db=db, domain_event_publisher=domain_event_publisher
  )
  sub_topic_repository = providers.Factory(
    SubTopicRepository, db=db, domain_event_publisher=domain_event_publisher
  )
  assessment_repository = providers.Factory(
    AssessmentRepository, db=db, domain_event_publisher=domain_event_publisher
  )
  question_repository = providers.Factory(
    QuestionRepository, db=db, domain_event_publisher=domain_event_publisher
  )
  user_repository = providers.Factory(
    UserRepository, db=db, domain_event_publisher=domain_event_publisher
  )

  user_lookup = providers.Factory(UserLookupAdapter, db=db)

  study_plan_ai_service = providers.Factory(
    StudyPlanAIServiceOpenAIAdapter, settings=settings
  )

  request_study_plan_use_case = providers.Factory(
    RequestStudyPlanUseCaseAdapter, study_plan_repository=study_plan_repository
  )

  generate_study_plan_use_case = providers.Factory(
    GenerateStudyPlanUseCaseAdapter,
    study_plan_repository=study_plan_repository,
    topic_repository=topic_repository,
    sub_topic_repository=sub_topic_repository,
    assessment_repository=assessment_repository,
    question_repository=question_repository,
    study_plan_ai_service=study_plan_ai_service,
  )

  get_study_plan_use_case = providers.Factory(
    GetStudyPlanUseCaseAdapter, study_plan_repository=study_plan_repository
  )

  get_assessment_use_case = providers.Factory(
    GetAssessmentUseCaseAdapter, assessment_repository=assessment_repository
  )

  start_assessment_use_case = providers.Factory(
    StartAssessmentUseCaseAdapter,
    assessment_repository=assessment_repository,
  )

  answer_question_use_case = providers.Factory(
    AnswerQuestionUseCaseAdapter,
    assessment_repository=assessment_repository,
    question_repository=question_repository,
  )

  complete_assessment_use_case = providers.Factory(
    CompleteAssessmentUseCaseAdapter,
    assessment_repository=assessment_repository,
  )

  get_topic_use_case = providers.Factory(
    GetTopicUseCaseAdapter, topic_repository=topic_repository
  )

  create_user_use_case = providers.Factory(
    CreateUserUseCaseAdapter, user_repository=user_repository, user_lookup=user_lookup
  )

  # Auth
  token_service = providers.Factory(TokenService, settings=settings)

  # Event Handlers
  study_plan_requested_event_handler = providers.Callable(
    study_plan_requested_event_handler_factory, event_publisher=event_publisher
  )

  study_plan_generated_event_handler = providers.Callable(
    study_plan_generated_event_handler_factory, event_publisher=event_publisher
  )

  study_plan_error_reported_event_handler = providers.Callable(
    study_plan_error_reported_event_handler_factory, event_publisher=event_publisher
  )

  # Command Handlers
  generate_study_plan_command_handler = providers.Callable(
    generate_study_plan_command_handler_factory, use_case=generate_study_plan_use_case
  )

  report_study_plan_generated_command_handler = providers.Callable(
    report_study_plan_generated_command_handler_factory,
    realtime_connection_manager=realtime_connection_manager,
  )

  report_study_plan_error_command_handler = providers.Callable(
    report_study_plan_error_command_handler_factory,
    realtime_connection_manager=realtime_connection_manager,
  )
