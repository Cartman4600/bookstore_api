from sqlalchemy import Column, Integer, String, Numeric

from database import Base_Bookstore

class Ebook(Base_Bookstore):
    __tablename__ = "ebooks"

    id               = Column(Integer, primary_key = True)
    title            = Column(String(255), nullable = False)
    author           = Column(String(255), nullable = False)
    publication_year = Column(Integer, nullable = False)
    publisher        = Column(String(255), nullable = False)
    pages            = Column(Integer, nullable = False)
    price            = Column(Numeric(10, 2), nullable = False)