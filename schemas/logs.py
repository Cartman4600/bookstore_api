from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class LogRead(BaseModel):
    id:         int
    table_name: str
    item_id:    int
    operation:  str
    old_data: Optional[dict]
    new_data: Optional[dict]
    timestamp:  datetime

    model_config = ConfigDict(from_attributes = True)