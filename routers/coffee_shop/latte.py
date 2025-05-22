from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_coffee_shop_db
from models.coffee_shop.latte import Latte
from schemas.coffee_shop.latte import LatteCreate, LatteRead, LatteUpdate
from auth import verify_token

router = APIRouter()

# erstellen
@router.post("/", 
             response_model = LatteRead, 
             status_code    = status.HTTP_201_CREATED, 
             dependencies   = [Depends(verify_token)]
             )
def create_latte(latte: LatteCreate, db: Session = Depends(get_coffee_shop_db)):
    db_latte = Latte(**latte.model_dump())
    db.add(db_latte)
    db.commit()
    db.refresh(db_latte)
    return db_latte

# alle lesen
@router.get("/", response_model = List[LatteRead])
def read_lattes(skip: int = 0, limit: int = 100, db: Session = Depends(get_coffee_shop_db)):
    lattes = db.query(Latte).offset(skip).limit(limit).all()
    return lattes

# lesen nur einer
@router.get("/{latte_id}", response_model = LatteRead)
def read_latte(latte_id: int, db: Session = Depends(get_coffee_shop_db)):
    latte = db.query(Latte).filter(Latte.id == latte_id).first()
    if not latte:
        raise HTTPException(status_code = 404, detail = f"Latte with id {latte_id} not found")
    return latte

# ändern
@router.put("/{latte_id}", 
            response_model = LatteRead, 
            dependencies   = [Depends(verify_token)]
            )
def update_latte(latte_id: int, latte_update: LatteUpdate, db: Session = Depends(get_coffee_shop_db)):
    latte = db.query(Latte).filter(Latte.id == latte_id).first()
    if not latte:
        raise HTTPException(status_code = 404, detail = f"Latte spritzer with id {latte_id} not found")
    for key, value in latte_update.model_dump(exclude_unset = True).items():
        setattr(latte, key, value)
    db.commit()
    db.refresh(latte)
    return latte

# löschen
@router.delete("/{latte_id}", 
               status_code  = status.HTTP_204_NO_CONTENT, 
               dependencies = [Depends(verify_token)]
               )
def delete_latte(latte_id: int, db: Session = Depends(get_coffee_shop_db)):
    latte = db.query(Latte).filter(Latte.id == latte_id).first()
    if not latte:
        raise HTTPException(status_code = 404, detail = f"Latte spritzer with id {latte_id} not found")
    db.delete(latte)
    db.commit()
    return None