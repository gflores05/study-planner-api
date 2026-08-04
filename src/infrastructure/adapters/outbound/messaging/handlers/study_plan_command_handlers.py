from src.application.dtos.study_plan import GenerateStudyPlanDTO
from src.application.messages.study_plan_messages import (
  GenerateStudyPlanCommandMessage,
  ReportStudyPlanErrorCommandMessage,
  ReportStudyPlanGeneratedCommandMessage,
)
from src.application.ports.inbound.study_plan.generate_study_plan_use_case import (
  GenerateStudyPlanUseCasePort,
)
from src.infrastructure.adapters.outbound.websockets.connection_manager import (
  RealtimeConnectionManager,
)


async def generate_study_plan_command_handler_factory(
  use_case: GenerateStudyPlanUseCasePort,
):
  async def handle(payload: dict):
    try:
      command = GenerateStudyPlanCommandMessage.model_validate(payload)

      await use_case.execute(GenerateStudyPlanDTO(study_plan_id=command.study_plan_id))
    except Exception as ex:
      print(ex)

  return handle


async def report_study_plan_generated_command_handler_factory(
  realtime_connection_manager: RealtimeConnectionManager,
):
  async def handle(payload: dict):
    command = ReportStudyPlanGeneratedCommandMessage.model_validate(payload)
    message = {
      "event": command.event_name,
      "payload": payload,
    }

    user_id = command.reported_by_user_id

    if user_id and realtime_connection_manager.is_connected(user_id):
      await realtime_connection_manager.send_to_user(user_id, message)

  return handle


async def report_study_plan_error_command_handler_factory(
  realtime_connection_manager: RealtimeConnectionManager,
):
  async def handle(payload: dict):
    command = ReportStudyPlanErrorCommandMessage.model_validate(payload)
    message = {
      "event": command.event_name,
      "payload": payload,
    }

    user_id = command.reported_by_user_id

    if user_id and realtime_connection_manager.is_connected(user_id):
      await realtime_connection_manager.send_to_user(user_id, message)

  return handle
