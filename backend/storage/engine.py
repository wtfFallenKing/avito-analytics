import redis.asyncio as redis

from config import get_config

config = get_config()

redis_url = f"redis://{config.REDIS_USER}:{config.REDIS_PASSWORD}@{config.REDIS_HOST}:{config.REDIS_PORT}"
pool = redis.ConnectionPool.from_url(redis_url)
