from enum import Enum
from typing import Optional
from pydantic import BaseModel


class SpeakerAction(str, Enum):
    activate = "activate"
    deactivate = "deactivate"


class SpeakerUpdate(BaseModel):
    volume: Optional[int]
    action: Optional[SpeakerAction]
