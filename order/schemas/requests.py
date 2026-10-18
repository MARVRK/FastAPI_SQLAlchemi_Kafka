from pydantic import BaseModel, ConfigDict
from typing import Literal

class ChangeOrderStatusRequest (BaseModel):
    model_config = ConfigDict (extra='forbid')
    status: Literal["cancelled"]
