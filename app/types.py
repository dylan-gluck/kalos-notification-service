from pydantic import BaseModel
from typing import Optional, Union, List
from enum import Enum


class NotificationType(str, Enum):
    CHANGE = "change"
    LEARNING = "learning"
    UPDATE = "update"


class NotificationRequest(BaseModel):
    type: NotificationType
    customer: str
    campaign: Optional[str] = None
    data: Union[str, List[str]]
    links: List[str] = []


class NotificationResponse(BaseModel):
    status: int
    success: bool
    message_id: Optional[str] = None
    error: Optional[str] = None
