from typing import Annotated, Optional
from pydantic import Field
from schemas.bookstore.media_base import MediaCreate, MediaUpdate, MediaRead

class MovieCreate(MediaCreate):
    in_stock: Annotated[int, Field(ge = 0)]

class MovieUpdate(MediaUpdate):
    in_stock: Annotated[Optional[int], Field(ge = 0)] = None

class MovieRead(MediaRead):
    id: int
    title: Annotated[str, Field(max_length = 255)]
    publication_year: Annotated[int, Field(gt = 0)]
    publisher: Annotated[str, Field(max_length = 255)]
    price: Annotated[float, Field(ge = 0)]
    in_stock: Annotated[int, Field(ge = 0)]
