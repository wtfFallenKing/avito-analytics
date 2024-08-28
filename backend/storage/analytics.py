import datetime
from asyncio import sleep
from pprint import pprint
from typing import Callable

from redis.asyncio import Redis
from redis import exceptions

MAX_RETRY_COUNT = 3


def retries(func: Callable):
    async def _wrapper(*args, **kwargs):
        retry = kwargs.pop("retry", 0)
        try:
            await func(*args, **kwargs, retry=retry)
        except exceptions.ConnectionError:
            print(f"{func.__name__}, retry={retry}")
            await sleep(0.5)
            await func(*args, **kwargs, retry=retry + 1)

    return _wrapper


def put_dict_in_order(data: dict, need_sort=True, count=30):
    data = list(map(lambda x: (x[0].decode('utf8'), int(x[1])), data.items()))
    if need_sort:
        data = sorted(data, key=lambda x: -x[1])

    return {k: v for k, v in data[:count] if k != "-1"}


async def get_analytics(client: Redis):
    obj = dict()

    obj["total_requests"] = int(await client.get("total_requests") or 0)
    obj["dates"] = put_dict_in_order(await client.hgetall("dates") or {}, need_sort=False, count=30)
    obj["locations"] = put_dict_in_order(await client.hgetall("locations") or {}, need_sort=True, count=15)
    obj["categories"] = put_dict_in_order(await client.hgetall("categories") or {}, need_sort=True, count=15)

    return obj


async def add_updates(client: Redis, location_id: int, category_id: int):
    await update_date_request(client)
    await update_total_requests(client)
    await update_locations_requests(client, location_id)
    await update_categories_requests(client, category_id)


@retries
async def update_total_requests(client: Redis, retry=0):
    if retry > MAX_RETRY_COUNT:
        return

    if not await client.get("total_requests"):
        await client.set("total_requests", 0)
    await client.incrby(name="total_requests", amount=1)


@retries
async def update_date_request(client: Redis, retry=0):
    key = datetime.date.today().strftime("%d.%m.%Y")
    if retry > MAX_RETRY_COUNT:
        return

    if not await client.hget("dates", "-1"):
        await client.hset("dates", mapping={"-1": -1})
    if not await client.hget("dates", key):
        await client.hset("dates", key=key, value=0)
    await client.hincrby(name="dates", key=key, amount=1)


@retries
async def update_locations_requests(client: Redis, location_id: int, retry=0):
    if retry > MAX_RETRY_COUNT:
        return

    if not await client.hget("locations", "-1"):
        await client.hset("locations", mapping={"-1": -1})
    if not await client.hget("locations", str(location_id)):
        await client.hset("locations", key=str(location_id), value=0)
    await client.hincrby(name="locations", key=str(location_id), amount=1)


@retries
async def update_categories_requests(client: Redis, category_id: int, retry=0):
    if retry > MAX_RETRY_COUNT:
        return

    if not await client.hget("categories", "-1"):
        await client.hset("categories", mapping={"-1": -1})
    if not await client.hget("categories", str(category_id)):
        await client.hset("categories", key=str(category_id), value=0)
    await client.hincrby(name="categories", key=str(category_id), amount=1)
