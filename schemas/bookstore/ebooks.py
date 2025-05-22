from typing import Annotated, Optional
from pydantic import BaseModel, Field, ConfigDict

class EbookBase(BaseModel):
    title: Annotated[str, Field(max_length=255)]
    author: Annotated[str, Field(max_length=255)]
    publication_year: Annotated[int, Field(gt=0)]
    publisher: Annotated[str, Field(max_length=255)]
    pages: Annotated[int, Field(gt=0)]
    price: Annotated[float, Field(ge=0)]

class EbookCreate(EbookBase):
    # erbt von EbookBase alles.
    pass

class EbookUpdate(EbookBase):
    title: Annotated[Optional[str], Field(max_length=255)] = None
    author: Annotated[Optional[str], Field(max_length=255)] = None
    publication_year: Annotated[Optional[int], Field(gt=0)] = None
    publisher: Annotated[Optional[str], Field(max_length=255)] = None
    pages: Annotated[Optional[int], Field(gt=0)] = None
    price: Annotated[Optional[float], Field(ge=0)] = None

class EbookRead(BaseModel):
    id: int
    title: Annotated[str, Field(max_length=255)]
    author: Annotated[str, Field(max_length=255)]
    publication_year: Annotated[int, Field(gt=0)]
    publisher: Annotated[str, Field(max_length=255)]
    pages: Annotated[int, Field(gt=0)]
    price: Annotated[float, Field(ge=0)]

    model_config = ConfigDict(from_attributes = True)
