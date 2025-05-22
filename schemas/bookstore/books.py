from typing import Annotated, Optional
from pydantic import BaseModel, Field, ConfigDict

class BookBase(BaseModel):
    title: Annotated[str, Field(max_length = 255)]
    author: Annotated[str, Field(max_length = 255)]
    publication_year: Annotated[int, Field(gt = 0)]       # gt - greater then 0
    publisher: Annotated[str, Field(max_length = 255)]
    pages: Annotated[int, Field(gt = 0)]
    price: Annotated[float, Field(ge = 0)]                # ge - greater or euqal
    in_stock: Annotated[int, Field(ge = 0)]

class BookCreate(BookBase):
    # erbt von BookBase alles.
    pass

class BookUpdate(BookBase):
    title: Annotated[Optional[str], Field(max_length = 255)]     = None
    author: Annotated[Optional[str], Field(max_length = 255)]    = None
    publication_year: Annotated[Optional[int], Field(gt = 0)]	 = None
    publisher: Annotated[Optional[str], Field(max_length = 255)] = None
    pages: Annotated[Optional[int], Field(gt = 0)]               = None
    price: Annotated[Optional[float], Field(ge = 0)]             = None
    in_stock: Annotated[Optional[int], Field(ge = 0)]            = None

class BookRead(BaseModel):
    id: int
    title: Annotated[str, Field(max_length = 255)]
    author: Annotated[str, Field(max_length = 255)]
    publication_year: Annotated[int, Field(gt = 0)]
    publisher: Annotated[str, Field(max_length = 255)]
    pages: Annotated[int, Field(gt = 0)]
    price: Annotated[float, Field(ge = 0)]
    in_stock: Annotated[int, Field(ge = 0)]

    model_config = ConfigDict(from_attributes = True)
