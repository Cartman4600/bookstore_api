from sqlalchemy import Column, Integer, String, Numeric

from database import Base_Bookstore

class MediaBase(Base_Bookstore):
    # __tablename__ = 'in der child -class setzen'
    __abstract__ = True # wird nicht als tabelle benötigt

    id               = Column(Integer, primary_key = True)
    title            = Column(String(255), nullable = False)
    publication_year = Column(Integer, nullable = False)
    publisher        = Column(String(255), nullable = False)
    price            = Column(Numeric(10, 2), nullable = False)