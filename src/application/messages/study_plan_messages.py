from src.application.ports.outbound.messaging.message import MessageEvent


# Events
class StudyPlanRequestedEventMessage(MessageEvent):
  event_name: str = "StudyPlanRequestedEvent"
  study_plan_id: str


class StudyPlanGeneratedEventMessage(MessageEvent):
  event_name: str = "StudyPlanGeneratedEvent"
  study_plan_id: str


# Commands
class GenerateStudyPlanCommandMessage(MessageEvent):
  event_name: str = "GenerateStudyPlanCommand"
  study_plan_id: str


class ReportStudyPlanGeneratedCommandMessage(MessageEvent):
  event_name: str = "ReportStudyPlanGeneratedCommand"
  study_plan_id: str
