from src.application.ports.outbound.messaging.message import MessageEvent


# Events
class StudyPlanRequestedEventMessage(MessageEvent):
  event_name: str = "StudyPlanRequestedEvent"
  study_plan_id: str
  requested_by_user_id: str


class StudyPlanGeneratedEventMessage(MessageEvent):
  event_name: str = "StudyPlanGeneratedEvent"
  study_plan_id: str
  generated_by_user_id: str


class StudyPlanErrorReportedEventMessage(MessageEvent):
  event_name: str = "StudyPlanErrorReportedEvent"
  study_plan_id: str
  reported_by_user_id: str
  error: str


# Commands
class GenerateStudyPlanCommandMessage(MessageEvent):
  event_name: str = "GenerateStudyPlanCommand"
  study_plan_id: str
  generated_by_user_id: str


class ReportStudyPlanGeneratedCommandMessage(MessageEvent):
  event_name: str = "ReportStudyPlanGeneratedCommand"
  study_plan_id: str
  reported_by_user_id: str


class ReportStudyPlanErrorCommandMessage(MessageEvent):
  event_name: str = "ReportStudyPlanErrorCommand"
  study_plan_id: str
  reported_by_user_id: str
  error: str
