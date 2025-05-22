from typing import Annotated, Optional
from pydantic import BaseModel, Field, ConfigDict

class BackstockBase(BaseModel):
    name: Annotated[str, Field(max_length = 255)]
    in_stock: Annotated[int, Field(ge = 0)]

class BackstockCreate(BackstockBase):
    # erbt von BackstockBase alles.
    pass

class BackstockUpdate(BackstockBase):
    name: Annotated[Optional[str], Field(max_length = 255)] = None
    in_stock: Annotated[Optional[int], Field(ge = 0)]       = None

class BackstockRead(BaseModel):
    id: int
    name: Annotated[str, Field(max_length = 255)]
    in_stock: Annotated[int, Field(ge = 0)]

    model_config = ConfigDict(from_attributes = True)
