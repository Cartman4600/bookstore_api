from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from database import get_bookstore_db
from models.bookstore.books import Book
from models.bookstore.movies import Movie
from schemas.bookstore.summary import Summary

router = APIRouter()

@router.get("/", response_model = List[Summary])
def get_summary(db: Session = Depends(get_bookstore_db)):

    books = db.query(Book.id,
                     Book.title,
                     Book.in_stock,
                     (Book.in_stock * Book.price).label("total_price")
                    ).all()

    book_list = [Summary(id           = b.id, 
                         title        = b.title, 
                         in_stock     = b.in_stock, 
                         total_price  = b.total_price, 
                         product_type = "book"
                         ) 
                         for b in books
                ]

    movies = db.query(Movie.id,
                      Movie.title,
                      Movie.in_stock,
                      (Movie.in_stock * Movie.price).label("total_price")
                     ).all()

    movie_list = [Summary(id           = m.id, 
                          title        = m.title, 
                          in_stock     = m.in_stock, 
                          total_price  = m.total_price, 
                          product_type = "movie"
                          ) 
                          for m in movies
                 ]

    return book_list + movie_list

