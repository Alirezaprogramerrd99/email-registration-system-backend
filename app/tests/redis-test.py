import redis
r = redis.Redis(
    host='localhost',
    port=6379,
    password='96243097'
)
r.mset({"Croatia": "Zagreb", "Bahamas": "Nassau"})

print(str(r.get("Bahamas")))