from sqlalchemy import Column, Integer, String

from database import Base_Coffee_Shop

class Backstock(Base_Coffee_Shop):
    __tablename__ = "backstock"

    id       = Column(Integer, primary_key = True)
    name     = Column(String(255), nullable = False)
    in_stock = Column(Integer, nullable = False)