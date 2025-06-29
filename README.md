# 📚 Book Review Service

A FastAPI-powered REST API for managing books and their reviews. Supports SQLAlchemy for database ORM and Redis for caching.

This project lets you add new books, list all books (with Redis caching for speed), post reviews for books, and retrieve all reviews for a given book.

---

## Project Structure

/BOOK REVIEW/
├── main.py          - FastAPI app with routes
├── models.py        - SQLAlchemy models
├── database.py      - DB session/engine setup
└── redis_client.py  - Redis get/set helpers


---

## How it Works

Books are stored in a relational database using SQLAlchemy models. Reviews are linked to books via a foreign key relationship. The GET /books/ endpoint uses Redis to cache the list of books, speeding up repeat reads. Whenever a new book is added, the cache is invalidated automatically so users always see up-to-date results.

---

## API Endpoints

POST /books/
Adds a new book.

Request JSON:
{
  "title": "Book Title",
  "author": "Author Name"
}

Response JSON:
{
  "id": 1,
  "title": "Book Title",
  "author": "Author Name"
}

GET /books/
Returns all books (cached in Redis).

Response JSON:
[
  {
    "id": 1,
    "title": "Book Title",
    "author": "Author Name"
  }
]

POST /reviews/
Adds a new review.

Request JSON:
{
  "content": "Great book!",
  "rating": 5,
  "book_id": 1
}

Response JSON:
{
  "id": 1,
  "content": "Great book!",
  "rating": 5,
  "book_id": 1
}

GET /books/{book_id}/reviews
Returns all reviews for the given book.

Response JSON:
[
  {
    "id": 1,
    "content": "Great book!",
    "rating": 5,
    "book_id": 1
  }
]

---

## Quick Start

1. Clone the repo:
git clone https://github.com/PrateekBhardwajj/Book-Review.git
cd Book-Review

2. Install requirements:
pip install -r requirements.txt

3. Make sure Redis is running locally:
redis-server

4. Run the FastAPI server:
uvicorn main:app --reload

Your API will be live at:
http://127.0.0.1:8000

Test your API in the browser with:
http://127.0.0.1:8000/docs
or
http://127.0.0.1:8000/redoc

---

## Database

Uses SQLAlchemy with your choice of SQLite, Postgres, MySQL etc. Default setup uses SQLite for easy local testing.

---

## Redis Cache

The GET /books/ endpoint response is cached in Redis to improve performance. The cache automatically invalidates when you add a new book, ensuring data consistency while reducing database load.

---

## Contributing

Fork the repo, make your changes, and open a pull request.

---

