from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from database import get_bookstore_db
from models.bookstore.books import Book
from models.bookstore.movies import Movie
from schemas.bookstore.summary import Summary, SummaryResponse

router = APIRouter()

@router.get("/", response_model = SummaryResponse)
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
                         product_type = "book") 
                 for b in books]

    value_books = sum(b.total_price for b in book_list)

    movies = db.query(Movie.id,
                      Movie.title,
                      Movie.in_stock,
                      (Movie.in_stock * Movie.price).label("total_price")
                     ).all()

    movie_list = [Summary(id           = m.id, 
                          title        = m.title, 
                          in_stock     = m.in_stock, 
                          total_price  = m.total_price, 
                          product_type = "movie") 
                  for m in movies]

    value_movies = sum(m.total_price for m in movie_list)

    all_items   = book_list + movie_list
    total_value = value_books + value_movies

    return SummaryResponse(total_value  = total_value,
                           value_books  = value_books,
                           value_movies = value_movies,
                           items        = all_items
                          )