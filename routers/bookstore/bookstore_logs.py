from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from models.logs import Log
from schemas.logs import LogRead
from database import get_bookstore_db
from routers.crud_funtions import create_read_all_handler

router = APIRouter()

# Read all
read_all_items_handler = create_read_all_handler(Model     = Log,
                                                 db_getter = get_bookstore_db
                                                )

@router.get("/", response_model = List[LogRead])
def read_all_handler(skip:int   = None, 
                     limit:int  = None, 
                     db:Session = Depends(get_bookstore_db)
                    ):
    return read_all_items_handler(skip = skip, limit = limit, db = db)