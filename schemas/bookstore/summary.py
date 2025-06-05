from pydantic import BaseModel
from typing import List

class Summary(BaseModel):
    id           : int
    title        : str
    in_stock     : int
    total_price  : float
    product_type : str

class SummaryResponse(BaseModel):
    total_value  : float
    value_books  : float
    value_movies : float
    items        : List[Summary]