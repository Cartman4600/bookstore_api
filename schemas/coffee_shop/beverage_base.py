from typing import Annotated, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

desc = "ISO 8601 Timestamp"

class BeverageBase(BaseModel):
    price:      Annotated[float,    Field(ge = 0)]
    order_date: Annotated[datetime, Field(description = desc)]

class BeverageCreate(BeverageBase):
    # erbt von BeverageBase alles.
    pass

class BeverageUpdate(BeverageBase):
    price:      Annotated[Optional[float],    Field(ge = 0)]             = None
    order_date: Annotated[Optional[datetime], Field(description = desc)] = None

class BeverageRead(BaseModel):
    id:         int
    price:      Annotated[float,    Field(ge = 0)]
    order_date: Annotated[datetime, Field(description = desc)]

    model_config = ConfigDict(from_attributes = True)