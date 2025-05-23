from fastapi import APIRouter, Depends, status
from typing import List, Union
from sqlalchemy.orm import Session

from database import get_coffee_shop_db
from models.coffee_shop.apple_spritzer import AppleSpritzer
from schemas.coffee_shop.apple_spritzer import AppleSpritzerCreate, AppleSpritzerRead, AppleSpritzerUpdate
from auth import verify_token
from routers.crud_funtions import (create_post_handler, 
                                   create_read_one_handler, 
                                   create_read_all_handler, 
                                   create_update_handler, 
                                   create_delete_handler
                                  )

router = APIRouter()

# Create
post_item_handler = create_post_handler(Model = AppleSpritzer, 
                                        Schema = AppleSpritzerCreate, 
                                        db_getter = get_coffee_shop_db
                                       )

@router.post("/", 
             response_model = AppleSpritzerRead, 
             status_code    = status.HTTP_201_CREATED, 
             dependencies   = [Depends(verify_token)]
             )
def post_handler(item:Union[AppleSpritzerCreate, List[AppleSpritzerCreate]],
                 db: Session = Depends(get_coffee_shop_db)):
    return post_item_handler(item = item, db = db)
    

# Read all
read_all_items_handler = create_read_all_handler(Model     = AppleSpritzer,
                                                db_getter = get_coffee_shop_db
                                               )

@router.get("/", response_model = List[AppleSpritzerRead])
def read_all_handler(skip:int   = 0, 
                     limit:int  = 100, 
                     db:Session = Depends(get_coffee_shop_db)
                    ):
    return read_all_items_handler(skip = skip, limit = limit, db = db)

# Read one
read_one_item_handler = create_read_one_handler(Model     = AppleSpritzer,
                                                db_getter = get_coffee_shop_db
                                               )

@router.get("/{item_id}", response_model = AppleSpritzerRead)
def read_one_handler(item_id:int, 
                     db: Session = Depends(get_coffee_shop_db)
                    ):
    return read_one_item_handler( item_id = item_id, db = db)

# Update
update_item_handler = create_update_handler(Model     = AppleSpritzer, 
                                            Schema    = AppleSpritzerUpdate, 
                                            db_getter = get_coffee_shop_db
                                           )

@router.put("/{item_id}", 
            response_model = AppleSpritzerRead,
            dependencies   = [Depends(verify_token)]
            )
def update_handler(item_id:int,
                   update_data:AppleSpritzerUpdate, 
                   db:Session = Depends(get_coffee_shop_db)
                  ):
    return update_item_handler(item_id     = item_id,
                               update_data = update_data,
                               db          = db
                              )

# Delete
delete_item_handler = create_delete_handler(Model = AppleSpritzer, db_getter = get_coffee_shop_db)

@router.delete("/{item_id}", 
               status_code  = status.HTTP_204_NO_CONTENT, 
               dependencies = [Depends(verify_token)]
              )
def delete_handler(item_id:int, 
                   db:Session = Depends(get_coffee_shop_db)
                  ):
    
    return delete_item_handler(item_id = item_id, db = db)