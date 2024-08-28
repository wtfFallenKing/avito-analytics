from redis.asyncio import Redis

from storage.engine import pool


class RedisConnectionOpener:
    client: Redis

    async def __aenter__(self) -> Redis:
        self.client = Redis.from_pool(pool)
        return self.client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()


async def get_redis_session() -> Redis:
    async with RedisConnectionOpener() as client:
        yield client
