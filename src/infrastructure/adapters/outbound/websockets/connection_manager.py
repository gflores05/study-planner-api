import logging
from collections import defaultdict

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class RealtimeConnectionManager:
  def __init__(self):
    # user_id → set of active WebSocket connections
    # supports multiple tabs/devices per user
    self._connections: dict[str, set[WebSocket]] = defaultdict(set)

  async def connect(self, websocket: WebSocket, user_id: str) -> None:
    await websocket.accept()
    self._connections[user_id].add(websocket)
    logger.info(f"User {user_id} connected. Total connections: {self._count()}")

  def disconnect(self, websocket: WebSocket, user_id: str) -> None:
    self._connections[user_id].discard(websocket)
    if not self._connections[user_id]:
      del self._connections[user_id]
    logger.info(f"User {user_id} disconnected. Total connections: {self._count()}")

  async def send_to_user(self, user_id: str, message: dict) -> None:
    """Send a message to all connections of a specific user."""
    connections = self._connections.get(user_id, set())
    disconnected = set()

    for websocket in connections:
      try:
        await websocket.send_json(message)
      except Exception:
        disconnected.add(websocket)

    # Clean up broken connections
    for websocket in disconnected:
      self.disconnect(websocket, user_id)

  async def broadcast(self, message: dict) -> None:
    """Send a message to ALL connected users."""
    for user_id in list(self._connections.keys()):
      await self.send_to_user(user_id, message)

  def is_connected(self, user_id: str) -> bool:
    return user_id in self._connections

  def _count(self) -> int:
    return sum(len(conns) for conns in self._connections.values())
