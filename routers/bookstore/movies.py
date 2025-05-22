from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_bookstore_db
from models.bookstore.movies import Movie
from schemas.bookstore.movies import MovieCreate, MovieUpdate, MovieRead
from auth import verify_token

router = APIRouter()

# erstellen
@router.post("/", 
             response_model = MovieRead, 
             status_code    = status.HTTP_201_CREATED, 
             dependencies   = [Depends(verify_token)]
             )
def create_movie(movie: MovieCreate, db: Session = Depends(get_bookstore_db)):
    db_movie = Movie(**movie.model_dump())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

# alle lesen
@router.get("/", response_model = List[MovieRead])
def read_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_bookstore_db)):
    movies = db.query(Movie).offset(skip).limit(limit).all()
    return movies

# lesen nur einer
@router.get("/{movie_id}", response_model = MovieRead)
def read_movie(movie_id: int, db: Session = Depends(get_bookstore_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code = 404, detail = f"Movie with id {movie_id} not found")
    return movie

# ändern
@router.put("/{movie_id}", 
            response_model = MovieRead, 
            dependencies   = [Depends(verify_token)]
            )
def update_movie(movie_id: int, movie_update: MovieUpdate, db: Session = Depends(get_bookstore_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code = 404, detail = f"Movie with id {movie_id} not found")
    for key, value in movie_update.model_dump(exclude_unset = True).items():
        setattr(movie, key, value)
    db.commit()
    db.refresh(movie)
    return movie

# löschen
@router.delete("/{movie_id}", 
               status_code  = status.HTTP_204_NO_CONTENT, 
               dependencies = [Depends(verify_token)]
               )
def delete_movie(movie_id: int, db: Session = Depends(get_bookstore_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code = 404, detail = f"Movie with id {movie_id} not found")
    db.delete(movie)
    db.commit()
    return None
