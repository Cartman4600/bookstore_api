from sqlalchemy import Column, Integer, String

from models.bookstore.media_base import MediaBase

class Book(MediaBase):
    __tablename__ = "books"

    author           = Column(String(255), nullable = False)
    publisher        = Column(String(255), nullable = False)
    pages            = Column(Integer,     nullable = False)
    in_stock         = Column(Integer,     nullable = False)