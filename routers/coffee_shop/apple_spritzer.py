from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_coffee_shop_db
from models.coffee_shop.apple_spritzer import AppleSpritzer
from schemas.coffee_shop.apple_spritzer import AppleSpritzerCreate, AppleSpritzerRead, AppleSpritzerUpdate
from auth import verify_token

router = APIRouter()

# erstellen
@router.post("/", 
             response_model = AppleSpritzerRead, 
             status_code    = status.HTTP_201_CREATED, 
             dependencies   = [Depends(verify_token)]
             )
def create_apple_spritzer(apple_spritzer: AppleSpritzerCreate, db: Session = Depends(get_coffee_shop_db)):
    db_apple_spritzer = AppleSpritzer(**apple_spritzer.model_dump())
    db.add(db_apple_spritzer)
    db.commit()
    db.refresh(db_apple_spritzer)
    return db_apple_spritzer

# alle lesen
@router.get("/", response_model = List[AppleSpritzerRead])
def read_apple_spritzers(skip: int = 0, limit: int = 100, db: Session = Depends(get_coffee_shop_db)):
    apple_spritzers = db.query(AppleSpritzer).offset(skip).limit(limit).all()
    return apple_spritzers

# lesen nur einer
@router.get("/{apple_spritzer_id}", response_model = AppleSpritzerRead)
def read_apple_spritzer(apple_spritzer_id: int, db: Session = Depends(get_coffee_shop_db)):
    apple_spritzer = db.query(AppleSpritzer).filter(AppleSpritzer.id == apple_spritzer_id).first()
    if not apple_spritzer:
        raise HTTPException(status_code = 404, detail = f"Apple spritzer with id {apple_spritzer_id} not found")
    return apple_spritzer

# ändern
@router.put("/{apple_spritzer_id}", 
            response_model = AppleSpritzerRead, 
            dependencies   = [Depends(verify_token)]
            )
def update_apple_spritzer(apple_spritzer_id: int, apple_spritzer_update: AppleSpritzerUpdate, db: Session = Depends(get_coffee_shop_db)):
    apple_spritzer = db.query(AppleSpritzer).filter(AppleSpritzer.id == apple_spritzer_id).first()
    if not apple_spritzer:
        raise HTTPException(status_code = 404, detail = f"Apple spritzer with id {apple_spritzer_id} not found")
    for key, value in apple_spritzer_update.model_dump(exclude_unset = True).items():
        setattr(apple_spritzer, key, value)
    db.commit()
    db.refresh(apple_spritzer)
    return apple_spritzer

# löschen
@router.delete("/{apple_spritzer_id}", 
               status_code  = status.HTTP_204_NO_CONTENT, 
               dependencies = [Depends(verify_token)]
               )
def delete_apple_spritzer(apple_spritzer_id: int, db: Session = Depends(get_coffee_shop_db)):
    apple_spritzer = db.query(AppleSpritzer).filter(AppleSpritzer.id == apple_spritzer_id).first()
    if not apple_spritzer:
        raise HTTPException(status_code = 404, detail = f"Apple spritzer with id {apple_spritzer_id} not found")
    db.delete(apple_spritzer)
    db.commit()
    return None