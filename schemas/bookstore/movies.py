from typing import Annotated, Optional
from pydantic import BaseModel, Field, ConfigDict

class MovieBase(BaseModel):
    title: Annotated[str, Field(max_length=255)]
    publication_year: Annotated[int, Field(gt=0)]
    publisher: Annotated[str, Field(max_length=255)]
    price: Annotated[float, Field(ge=0)]
    in_stock: Annotated[int, Field(ge=0)]

class MovieCreate(MovieBase):
    # erbt von MovieBase alles.
    pass

class MovieUpdate(MovieBase):
    title: Annotated[Optional[str], Field(max_length=255)] = None
    publication_year: Annotated[Optional[int], Field(gt=0)] = None
    publisher: Annotated[Optional[str], Field(max_length=255)] = None
    price: Annotated[Optional[float], Field(ge=0)] = None
    in_stock: Annotated[Optional[int], Field(ge=0)] = None

class MovieRead(BaseModel):
    id: int
    title: Annotated[str, Field(max_length=255)]
    publication_year: Annotated[int, Field(gt=0)]
    publisher: Annotated[str, Field(max_length=255)]
    price: Annotated[float, Field(ge=0)]
    in_stock: Annotated[int, Field(ge=0)]

    model_config = ConfigDict(from_attributes = True)
