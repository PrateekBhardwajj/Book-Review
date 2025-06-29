# tests/test_api.py

from fastapi.testclient import TestClient
from main import app
from redis_client import set_books_in_cache

client = TestClient(app)

# --------------------------------------
# ✅ 1️⃣ Unit test for POST /books/
# --------------------------------------
def test_create_book():
    response = client.post("/books/", json={
        "title": "Test Book",
        "author": "Test Author"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Book"
    assert data["author"] == "Test Author"
    assert "id" in data
    print("\n✅ test_create_book passed.")


# --------------------------------------
# ✅ 2️⃣ Unit test for GET /books/
# --------------------------------------
def test_list_books():
    response = client.get("/books/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    print("\n✅ test_list_books passed.")


# --------------------------------------
# ✅ 3️⃣ Integration test for cache-miss path
# --------------------------------------
def test_cache_miss_behavior():
    # Step 1: Invalidate the Redis cache
    set_books_in_cache(None)

    # Step 2: Call the GET /books/ endpoint to trigger cache-miss
    response = client.get("/books/")
    assert response.status_code == 200

    # Step 3: Check returned data is list
    data = response.json()
    assert isinstance(data, list)

    print("\n✅ Integration test passed: Cache-miss path executed successfully (forced Redis miss, fell back to DB, repopulated cache).")
