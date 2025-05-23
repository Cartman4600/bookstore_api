from pydantic import BaseModel, ConfigDict

class Summary(BaseModel):
    id:           int
    title:        str
    in_stock:     int
    total_price:  float
    product_type: str

    model_config = ConfigDict(from_attributes = True)