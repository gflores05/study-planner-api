from datetime import datetime

from pydantic import BaseModel


class MessageEvent(BaseModel):
  event_name: str
  event_id: str
  occurred_on: datetime
