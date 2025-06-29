import requests

BASE_URL = "http://127.0.0.1:8000"

books = [
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    {"title": "1984", "author": "George Orwell"},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee"},
    {"title": "Pride and Prejudice", "author": "Jane Austen"},
    {"title": "Moby-Dick", "author": "Herman Melville"},
    {"title": "Brave New World", "author": "Aldous Huxley"},
    {"title": "The Catcher in the Rye", "author": "J.D. Salinger"},
    {"title": "Crime and Punishment", "author": "Fyodor Dostoevsky"}
]

# 1️⃣ Create books
book_ids = []
for book in books:
    resp = requests.post(f"{BASE_URL}/books/", json=book)
    print(f"Added book: {resp.json()}")
    book_ids.append(resp.json()["id"])

# 2️⃣ Create reviews
reviews = [
    {"content": "Amazing read, timeless classic.", "rating": 5, "book_id": book_ids[0]},
    {"content": "Chillingly relevant political allegory.", "rating": 5, "book_id": book_ids[1]},
    {"content": "Heartbreaking and profound.", "rating": 5, "book_id": book_ids[2]},
    {"content": "Beautifully written romance.", "rating": 4, "book_id": book_ids[3]},
    {"content": "Dense but rewarding read.", "rating": 4, "book_id": book_ids[4]},
    {"content": "Fascinating dystopian vision.", "rating": 5, "book_id": book_ids[5]},
    {"content": "Complex teen angst captured perfectly.", "rating": 4, "book_id": book_ids[6]},
    {"content": "Dark, psychological, gripping.", "rating": 5, "book_id": book_ids[7]},
    {"content": "A bit slow at times, but worth it.", "rating": 3, "book_id": book_ids[4]},
    {"content": "Very thought-provoking.", "rating": 5, "book_id": book_ids[1]},
]

for review in reviews:
    resp = requests.post(f"{BASE_URL}/reviews/", json=review)
    print(f"Added review: {resp.json()}")
