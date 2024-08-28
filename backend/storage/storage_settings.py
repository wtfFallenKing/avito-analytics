from typing import List

from fastapi import HTTPException
from redis.asyncio import Redis
from starlette import status

from schemas.storage import StorageConfResponse


async def get_storage_conf(client: Redis, need_raise=True) -> StorageConfResponse:
    if not await client.get("baseline"):
        if need_raise:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Storage wasn't set yet")
        return StorageConfResponse(baseline=-1, discounts=[])

    return StorageConfResponse(
        baseline=await client.get("baseline"),
        discounts=await client.smembers("discounts") or []
    )


async def set_baseline(client: Redis, baseline_id: int):
    await client.set("baseline", baseline_id)


async def add_discounts(client: Redis, discount_ids: List[int]):
    await client.delete("discounts")

    discount_ids = set(discount_ids)
    if discount_ids:
        await client.sadd("discounts", *discount_ids)


async def remove_discounts(client: Redis, discount_ids: List[int]):
    await client.srem("discounts", *set(discount_ids))
