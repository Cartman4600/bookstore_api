from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_coffee_shop_db
from models.coffee_shop.lemonade import Lemonade
from schemas.coffee_shop.lemonade import LemonadeCreate, LemonadeRead, LemonadeUpdate
from auth import verify_token

router = APIRouter()

# erstellen
@router.post("/", 
             response_model = LemonadeRead, 
             status_code    = status.HTTP_201_CREATED, 
             dependencies   = [Depends(verify_token)]
             )
def create_lemonade(lemonade: LemonadeCreate, db: Session = Depends(get_coffee_shop_db)):
    db_lemonade = Lemonade(**lemonade.model_dump())
    db.add(db_lemonade)
    db.commit()
    db.refresh(db_lemonade)
    return db_lemonade

# alle lesen
@router.get("/", response_model = List[LemonadeRead])
def read_lemonades(skip: int = 0, limit: int = 100, db: Session = Depends(get_coffee_shop_db)):
    lemonade = db.query(Lemonade).offset(skip).limit(limit).all()
    return lemonade

# lesen nur einer
@router.get("/{lemonade_id}", response_model = LemonadeRead)
def read_lemonade(lemonade_id: int, db: Session = Depends(get_coffee_shop_db)):
    lemonade = db.query(Lemonade).filter(Lemonade.id == lemonade_id).first()
    if not lemonade:
        raise HTTPException(status_code = 404, detail = f"Lemonade with id {lemonade_id} not found")
    return lemonade

# ändern
@router.put("/{lemonade_id}", 
            response_model = LemonadeRead, 
            dependencies   = [Depends(verify_token)]
            )
def update_lemonade(lemonade_id: int, lemonade_update: LemonadeUpdate, db: Session = Depends(get_coffee_shop_db)):
    lemonade = db.query(Lemonade).filter(Lemonade.id == lemonade_id).first()
    if not lemonade:
        raise HTTPException(status_code = 404, detail = f"Lemonade with id {lemonade_id} not found")
    for key, value in lemonade_update.model_dump(exclude_unset = True).items():
        setattr(lemonade, key, value)
    db.commit()
    db.refresh(lemonade)
    return lemonade

# löschen
@router.delete("/{lemonade_id}", 
               status_code  = status.HTTP_204_NO_CONTENT, 
               dependencies = [Depends(verify_token)]
               )
def delete_lemonade(lemonade_id: int, db: Session = Depends(get_coffee_shop_db)):
    lemonade = db.query(Lemonade).filter(Lemonade.id == lemonade_id).first()
    if not lemonade:
        raise HTTPException(status_code = 404, detail = f"Lemonade with id {lemonade_id} not found")
    db.delete(lemonade)
    db.commit()
    return None