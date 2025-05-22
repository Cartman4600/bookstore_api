from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_bookstore_db
from models.bookstore.ebooks import Ebook
from schemas.bookstore.ebooks import EbookCreate, EbookUpdate, EbookRead
from auth import verify_token

router = APIRouter()

# erstellen
@router.post("/", 
             response_model = EbookRead, 
             status_code    = status.HTTP_201_CREATED, 
             dependencies   = [Depends(verify_token)]
             )
def create_ebook(ebook: EbookCreate, db: Session = Depends(get_bookstore_db)):
    db_ebook = Ebook(**ebook.model_dump())
    db.add(db_ebook)
    db.commit()
    db.refresh(db_ebook)
    return db_ebook

# alle lesen
@router.get("/", response_model = List[EbookRead])
def read_ebooks(skip: int = 0, limit: int = 100, db: Session = Depends(get_bookstore_db)):
    ebooks = db.query(Ebook).offset(skip).limit(limit).all()
    return ebooks

# lesen nur einer
@router.get("/{ebook_id}", response_model = EbookRead)
def read_ebook(ebook_id: int, db: Session = Depends(get_bookstore_db)):
    ebook = db.query(Ebook).filter(Ebook.id == ebook_id).first()
    if not ebook:
        raise HTTPException(status_code = 404, detail = f"Ebook with id {ebook_id} not found")
    return ebook

# ändern
@router.put("/{ebook_id}", 
            response_model = EbookRead, 
            dependencies   = [Depends(verify_token)]
            )
def update_ebook(ebook_id: int, ebook_update: EbookUpdate, db: Session = Depends(get_bookstore_db)):
    ebook = db.query(Ebook).filter(Ebook.id == ebook_id).first()
    if not ebook:
        raise HTTPException(status_code = 404, detail = f"Ebook with id {ebook_id} not found")
    for key, value in ebook_update.model_dump(exclude_unset = True).items():
        setattr(ebook, key, value)
    db.commit()
    db.refresh(ebook)
    return ebook

# löschen
@router.delete("/{ebook_id}", 
               status_code  = status.HTTP_204_NO_CONTENT, 
               dependencies = [Depends(verify_token)]
               )
def delete_ebook(ebook_id: int, db: Session = Depends(get_bookstore_db)):
    ebook = db.query(Ebook).filter(Ebook.id == ebook_id).first()
    if not ebook:
        raise HTTPException(status_code = 404, detail = f"Ebook with id {ebook_id} not found")
    db.delete(ebook)
    db.commit()
    return None
