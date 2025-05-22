from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_coffee_shop_db
from models.coffee_shop.backstock import Backstock
from schemas.coffee_shop.backstock import BackstockCreate, BackstockRead, BackstockUpdate
from auth import verify_token

router = APIRouter()

# erstellen
@router.post("/", 
             response_model = BackstockRead, 
             status_code    = status.HTTP_201_CREATED, 
             dependencies   = [Depends(verify_token)]
             )
def create_backstock(backstock: BackstockCreate, db: Session = Depends(get_coffee_shop_db)):
    db_backstock = Backstock(**backstock.model_dump())
    db.add(db_backstock)
    db.commit()
    db.refresh(db_backstock)
    return db_backstock

# alle lesen
@router.get("/", response_model = List[BackstockRead])
def read_backstock(skip: int = 0, limit: int = 100, db: Session = Depends(get_coffee_shop_db)):
    backstock = db.query(Backstock).offset(skip).limit(limit).all()
    return backstock

# lesen nur einer
@router.get("/{backstock_id}", response_model = BackstockRead)
def read_backstock(backstock_id: int, db: Session = Depends(get_coffee_shop_db)):
    backstock = db.query(Backstock).filter(Backstock.id == backstock_id).first()
    if not backstock:
        raise HTTPException(status_code = 404, detail = f"Backstock with id {backstock_id} not found")
    return backstock

# ändern
@router.put("/{backstock_id}", 
            response_model = BackstockRead, 
            dependencies   = [Depends(verify_token)]
            )
def update_backstock(backstock_id: int, backstock_update: BackstockUpdate, db: Session = Depends(get_coffee_shop_db)):
    backstock = db.query(Backstock).filter(Backstock.id == backstock_id).first()
    if not backstock:
        raise HTTPException(status_code = 404, detail = f"Backstock with id {backstock_id} not found")
    for key, value in backstock_update.model_dump(exclude_unset = True).items():
        setattr(backstock, key, value)
    db.commit()
    db.refresh(backstock)
    return backstock

# löschen
@router.delete("/{backstock_id}", 
               status_code  = status.HTTP_204_NO_CONTENT, 
               dependencies = [Depends(verify_token)]
               )
def delete_backstock(backstock_id: int, db: Session = Depends(get_coffee_shop_db)):
    backstock = db.query(Backstock).filter(Backstock.id == backstock_id).first()
    if not backstock:
        raise HTTPException(status_code = 404, detail = f"Backstock with id {backstock_id} not found")
    db.delete(backstock)
    db.commit()
    return None