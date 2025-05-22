from sqlalchemy import Column, Integer, Numeric, TIMESTAMP

from database import Base_Coffee_Shop

class Beverage(Base_Coffee_Shop):
    # __tablename__ = 'in der child -class setzen'
    __abstract__ = True # wird nicht als tabelle benötigt

    id         = Column(Integer, primary_key = True)
    price      = Column(Numeric(10, 2), nullable = False)
    order_date = Column(TIMESTAMP, nullable = False)