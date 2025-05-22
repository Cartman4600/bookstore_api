from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_coffee_shop_db
from models.coffee_shop.americano import Americano
from schemas.coffee_shop.americano import AmericanoCreate, AmericanoRead, AmericanoUpdate
from auth import verify_token

router = APIRouter()

# erstellen
@router.post("/", 
             response_model = AmericanoRead, 
             status_code    = status.HTTP_201_CREATED, 
             dependencies   = [Depends(verify_token)]
             )
def create_americano(americano: AmericanoCreate, db: Session = Depends(get_coffee_shop_db)):
    db_americano = Americano(**americano.model_dump())
    db.add(db_americano)
    db.commit()
    db.refresh(db_americano)
    return db_americano

# alle lesen
@router.get("/", response_model = List[AmericanoRead])
def read_americanos(skip: int = 0, limit: int = 100, db: Session = Depends(get_coffee_shop_db)):
    americanos = db.query(Americano).offset(skip).limit(limit).all()
    return americanos

# lesen nur einer
@router.get("/{americano_id}", response_model = AmericanoRead)
def read_americano(americano_id: int, db: Session = Depends(get_coffee_shop_db)):
    americano = db.query(Americano).filter(Americano.id == americano_id).first()
    if not americano:
        raise HTTPException(status_code = 404, detail = f"Americano with id {americano_id} not found")
    return americano

# ändern
@router.put("/{americano_id}", 
            response_model = AmericanoRead, 
            dependencies   = [Depends(verify_token)]
            )
def update_americano(americano_id: int, americano_update: AmericanoUpdate, db: Session = Depends(get_coffee_shop_db)):
    americano = db.query(Americano).filter(Americano.id == americano_id).first()
    if not americano:
        raise HTTPException(status_code = 404, detail = f"Americano with id {americano_id} not found")
    for key, value in americano_update.model_dump(exclude_unset = True).items():
        setattr(americano, key, value)
    db.commit()
    db.refresh(americano)
    return americano

# löschen
@router.delete("/{americano_id}", 
               status_code  = status.HTTP_204_NO_CONTENT, 
               dependencies = [Depends(verify_token)]
               )
def delete_americano(americano_id: int, db: Session = Depends(get_coffee_shop_db)):
    americano = db.query(Americano).filter(Americano.id == americano_id).first()
    if not americano:
        raise HTTPException(status_code = 404, detail = f"Americano with id {americano_id} not found")
    db.delete(americano)
    db.commit()
    return None