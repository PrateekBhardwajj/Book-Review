from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import json
import models
from database import SessionLocal, engine
from redis_client import get_books_from_cache, set_books_in_cache

# Create DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Book Review Service", version="1.0")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic Schemas
class BookCreate(BaseModel):
    title: str
    author: str

class BookOut(BaseModel):
    id: int
    title: str
    author: str

    model_config = {"from_attributes": True}

class ReviewCreate(BaseModel):
    content: str
    rating: int
    book_id: int

class ReviewOut(BaseModel):
    id: int
    content: str
    rating: int
    book_id: int

    model_config = {"from_attributes": True}

# ROUTES

# 1️⃣ Add new book
@app.post("/books/", response_model=BookOut)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    # Invalidate the cache
    set_books_in_cache(None)
    return db_book

# 2️⃣ List all books (with Redis cache)
@app.get("/books/", response_model=List[BookOut])
def get_books(db: Session = Depends(get_db)):
    # 1. Try cache
    cached_data = get_books_from_cache()
    if cached_data:
        return json.loads(cached_data)
    
    # 2. Cache miss - read from DB
    books = db.query(models.Book).all()
    serialized = [BookOut.model_validate(book).model_dump() for book in books]

    # 3. Store in cache
    set_books_in_cache(json.dumps(serialized))
    
    return serialized

# 3️⃣ Post a review
@app.post("/reviews/", response_model=ReviewOut)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    # Check book exists
    book = db.query(models.Book).filter(models.Book.id == review.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db_review = models.Review(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

# 4️⃣ List all reviews for a book
@app.get("/books/{book_id}/reviews", response_model=List[ReviewOut])
def get_reviews(book_id: int, db: Session = Depends(get_db)):
    reviews = db.query(models.Review).filter(models.Review.book_id == book_id).all()
    return reviews
