from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import JSONB
from database import Base_Bookstore

class Log(Base_Bookstore):
    __tablename__ = 'logs'

    id         = Column(Integer,     primary_key = True)
    table_name = Column(String(255), nullable = False)
    item_id    = Column(Integer,     nullable = False)
    operation  = Column(String(255), nullable = False)
    old_data   = Column(JSONB,       nullable = True)
    new_data   = Column(JSONB,       nullable = True)
    timestamp  = Column(TIMESTAMP,   nullable = False, server_default = func.now())