import logging
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from src.infrastructure.adapters.outbound.websockets.connection_manager import (
  RealtimeConnectionManager,
)
from src.infrastructure.config.container import Container

logger = logging.getLogger(__name__)

router = APIRouter(tags=["websockets"])


@router.websocket("/ws/{user_id}")
@inject
async def websocket_endpoint(
  websocket: WebSocket,
  user_id: str,
  realtime_connection_manager: Annotated[
    RealtimeConnectionManager,
    Depends(Provide[Container.realtime_connection_manager]),
  ],
):
  await realtime_connection_manager.connect(websocket, user_id)

  try:
    while True:
      # Keep connection alive
      data = await websocket.receive_text()
      logger.info(f"Received from {user_id}: {data}")

  except WebSocketDisconnect:
    realtime_connection_manager.disconnect(websocket, user_id)
    logger.info(f"User {user_id} disconnected")
