from sqlalchemy import Column, Integer

from models.bookstore.media_base import MediaBase

class Movie(MediaBase):
    __tablename__ = "movies"

    in_stock         = Column(Integer, nullable = False)