from typing import List

from fastapi import HTTPException
from redis.asyncio import Redis
from sqlalchemy import select, text, bindparam, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from models.price import Price
from schemas.prices import PriceCreateRequest, PriceGetResponse, PriceReadRequest, PricePutRequest
from schemas.storage import StorageConfResponse
from services.categories import get_category
from services.locations import get_location
from services.segments import get_segments_by_user_id
from storage.storage_settings import get_storage_conf
from typing import Optional


async def get_prices(
    session: AsyncSession,
    matrix_id: Optional[int] = None,
    start: int = 1,
    end: int = 50,
) -> List[Price]:
    page = end - start + 1
    query = select(Price).offset(page * (start // page)).limit(page)
    if matrix_id:
        query = query.where(Price.matrix_id == matrix_id)

    result = await session.execute(query)
    return [
        Price(
            price=res.price, matrix_id=res.matrix_id, location_id=res.location_id, category_id=res.category_id
        )
        for res in result.scalars().all()
    ]


async def delete_price(session: AsyncSession, req: PriceReadRequest):
    await session.execute(
        delete(Price).where(
            Price.matrix_id == req.matrix_id,
            Price.location_id == req.location_id,
            Price.category_id == req.category_id,
        )
    )
    await session.commit()


async def get_price(session: AsyncSession, req: PriceReadRequest) -> Price:
    result = (
        await session.execute(
            select(Price).where(
                Price.matrix_id == req.matrix_id,
                Price.location_id == req.location_id,
                Price.category_id == req.category_id,
            )
        )
    ).scalar()
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid price key")

    return Price(
        price=result.price,
        matrix_id=result.matrix_id,
        location_id=result.location_id,
        category_id=result.category_id,
    )


async def set_price(session: AsyncSession, price: PricePutRequest):
    await session.execute(
        update(Price)
        .where(
            Price.matrix_id == price.matrix_id,
            Price.location_id == price.location_id,
            Price.category_id == price.category_id,
        )
        .values(price=price.price)
    )
    await session.commit()


async def add_price(session: AsyncSession, price: PriceCreateRequest) -> Price:
    new_matrix = Price(
        price=price.price,
        matrix_id=price.matrix_id,
        location_id=price.location_id,
        category_id=price.category_id,
    )

    session.add(new_matrix)
    await session.commit()

    return new_matrix


async def get_target_price(
    session: AsyncSession, user_id: int, category_id: int, location_id: int, redis_session: Redis
) -> PriceGetResponse:
    locations = list(map(int, (await get_location(session, location_id)).key.split("-")))
    categories = list(map(int, (await get_category(session, category_id)).key.split("-")))

    segments = await get_segments_by_user_id(user_id)
    storage: StorageConfResponse = await get_storage_conf(redis_session)

    ides = [storage.baseline] + storage.discounts

    statement = text(
        """
        SELECT
            prices.location_id, prices.category_id, prices.matrix_id, matrices.segment_id, prices.price
        FROM prices
        INNER JOIN matrices ON prices.matrix_id = matrices.id
        WHERE
            prices.location_id IN :locations AND
            prices.category_id IN :categories AND
            prices.matrix_id IN :ides AND
            (matrices.segment_id IS NULL OR (matrices.segment_id IN :segments AND matrices.id in :ides))
        ORDER BY prices.location_id DESC, prices.category_id DESC, matrices.type DESC;
        """
    )
    statement = (
        statement.bindparams(bindparam("locations", expanding=True))
        .bindparams(bindparam("categories", expanding=True))
        .bindparams(bindparam("segments", expanding=True))
        .bindparams(bindparam("ides", expanding=True))
    )

    result = (
        await session.execute(
            statement,
            {
                "ides": ides or [],
                "locations": locations,
                "categories": categories,
                "segments": segments or [],
            },
        )
    ).first()  # .all()
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data was passed")

    return PriceGetResponse(
        location_id=result[0],
        category_id=result[1],
        matrix_id=result[2],
        segment_id=result[3],
        price=result[4],
    )
