from sqlalchemy import Column, Integer, String

from models.bookstore.media_base import MediaBase

class Ebook(MediaBase):
    __tablename__ = "ebooks"

    author           = Column(String(255), nullable = False)
    pages            = Column(Integer, nullable = False)