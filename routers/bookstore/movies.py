from fastapi import APIRouter, Depends, status
from typing import List, Union
from sqlalchemy.orm import Session

from database import get_bookstore_db
from models.bookstore.movies import Movie
from schemas.bookstore.movies import MovieCreate, MovieUpdate, MovieRead
from auth import verify_token
from routers.crud_funtions import (create_post_handler, 
                                   create_read_one_handler, 
                                   create_read_all_handler, 
                                   create_update_handler, 
                                   create_delete_handler
                                  )

router = APIRouter()

# Create
post_item_handler = create_post_handler(Model     = Movie, 
                                        Schema    = MovieCreate, 
                                        db_getter = get_bookstore_db
                                       )

@router.post("/", 
             response_model = MovieRead, 
             status_code    = status.HTTP_201_CREATED, 
             dependencies   = [Depends(verify_token)]
             )
def post_handler(item:Union[MovieCreate, List[MovieCreate]],
                 db: Session = Depends(get_bookstore_db)
                ):
    return post_item_handler(item = item, db = db)
    

# Read all
read_all_items_handler = create_read_all_handler(Model    = Movie,
                                                db_getter = get_bookstore_db
                                               )

@router.get("/", response_model = List[MovieRead])
def read_all_handler(skip:int   = 0, 
                     limit:int  = 100, 
                     db:Session = Depends(get_bookstore_db)
                    ):
    return read_all_items_handler(skip = skip, limit = limit, db = db)

# Read one
read_one_item_handler = create_read_one_handler(Model     = Movie,
                                                db_getter = get_bookstore_db
                                               )

@router.get("/{item_id}", response_model = MovieRead)
def read_one_handler(item_id:int, 
                     db: Session = Depends(get_bookstore_db)
                    ):
    return read_one_item_handler( item_id = item_id, db = db)

# Update
update_item_handler = create_update_handler(Model     = Movie, 
                                            Schema    = MovieUpdate, 
                                            db_getter = get_bookstore_db
                                           )

@router.put("/{item_id}", 
            response_model = MovieRead,
            dependencies   = [Depends(verify_token)]
            )
def update_handler(item_id:int,
                   update_data:MovieUpdate, 
                   db:Session = Depends(get_bookstore_db)
                  ):
    return update_item_handler(item_id     = item_id,
                               update_data = update_data,
                               db          = db
                              )

# Delete
delete_item_handler = create_delete_handler(Model = Movie, db_getter = get_bookstore_db)

@router.delete("/{item_id}", 
               status_code  = status.HTTP_204_NO_CONTENT, 
               dependencies = [Depends(verify_token)]
              )
def delete_handler(item_id:int, 
                   db:Session = Depends(get_bookstore_db)
                  ):
    
    return delete_item_handler(item_id = item_id, db = db)