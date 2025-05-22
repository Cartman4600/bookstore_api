from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_bookstore_db
from models.bookstore.books import Book
from schemas.bookstore.books import BookCreate, BookUpdate, BookRead
from auth import verify_token

router = APIRouter()

# erstellen
@router.post("/", 
             response_model = BookRead, 
             status_code    = status.HTTP_201_CREATED, 
             dependencies   = [Depends(verify_token)]
             )
def create_book(book: BookCreate, db: Session = Depends(get_bookstore_db)):
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

# alle lesen
@router.get("/", response_model = List[BookRead])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_bookstore_db)):
    books = db.query(Book).offset(skip).limit(limit).all()
    return books

# lesen nur einer
@router.get("/{book_id}", response_model = BookRead)
def read_book(book_id: int, db: Session = Depends(get_bookstore_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code = 404, detail = f"Book with id {book_id} not found")
    return book

# ändern
@router.put("/{book_id}", 
            response_model = BookRead,
            dependencies   = [Depends(verify_token)]
            )
def update_book(book_id: int, book_update: BookUpdate, db: Session = Depends(get_bookstore_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code = 404, detail = f"Book with id {book_id} not found")
    for key, value in book_update.model_dump(exclude_unset = True).items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book

# löschen
@router.delete("/{book_id}", 
               status_code  = status.HTTP_204_NO_CONTENT, 
               dependencies = [Depends(verify_token)]
               )
def delete_book(book_id: int, db: Session = Depends(get_bookstore_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code = 404, detail = f"Book with id {book_id} not found")
    db.delete(book)
    db.commit()
    return None
