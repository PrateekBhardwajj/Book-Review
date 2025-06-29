import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def get_books_from_cache():
    try:
        data = r.get('books_list')
        if data:
            print("✅ [CACHE HIT] Data served from Redis")
        else:
            print("❌ [CACHE MISS] No data in Redis")
        return data
    except redis.exceptions.ConnectionError:
        print("🚨 [CACHE ERROR] Redis server is DOWN! Skipping cache.")
        return None

def set_books_in_cache(data):
    try:
        if data is None:
            print("🗑️ [CACHE DELETE] Removing books_list from Redis")
            r.delete('books_list')
        else:
            r.set('books_list', data, ex=3600)
            print("✅ [CACHE SAVE] Data stored in Redis for 1 hour")
    except redis.exceptions.ConnectionError:
        print("🚨 [CACHE ERROR] Redis server is DOWN! Cannot save cache.")
