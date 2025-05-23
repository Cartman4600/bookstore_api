from typing import Annotated, Optional
from pydantic import Field
from schemas.bookstore.media_base import MediaCreate, MediaUpdate, MediaRead

class EbookCreate(MediaCreate):
    author: Annotated[str, Field(max_length = 255)]
    pages:  Annotated[int, Field(gt = 0)]

class EbookUpdate(MediaUpdate):
    author: Annotated[Optional[str], Field(max_length=255)] = None
    pages:  Annotated[Optional[int], Field(gt=0)]           = None

class EbookRead(MediaRead):
    id:               int
    title:            Annotated[str,   Field(max_length = 255)]
    author:           Annotated[str,   Field(max_length = 255)]
    publication_year: Annotated[int,   Field(gt = 0)]
    publisher:        Annotated[str,   Field(max_length = 255)]
    pages:            Annotated[int,   Field(gt = 0)]
    price:            Annotated[float, Field(ge = 0)]
