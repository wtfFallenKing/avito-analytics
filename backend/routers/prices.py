import asyncio
from typing import Annotated, List, Dict

from fastapi import APIRouter, Depends, HTTPException
from redis.asyncio import Redis
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from deps.pagination import ModelTotalCount

from deps.redis_session import get_redis_session
from deps.sql_session import get_sql_session
from models import Price
from schemas.prices import (
    PriceResponse,
    PriceReadRequest,
    PriceCreateRequest,
    PriceGetRequest,
    PriceGetResponse,
    PricePutRequest,
)
from services.nodes import delete_table
from services.prices import get_prices, get_price, add_price, get_target_price, set_price
from storage.analytics import add_updates

router = APIRouter(tags=["prices"])


@router.post("/price/target")
async def calculate_target_price(
    request: PriceGetRequest,
    session: AsyncSession = Depends(get_sql_session),
    redis_session: Redis = Depends(get_redis_session),
) -> PriceGetResponse:
    asyncio.create_task(add_updates(redis_session, request.location_id, request.category_id))

    return await get_target_price(
        session=session,
        user_id=request.user_id,
        category_id=request.category_id,
        location_id=request.location_id,
        redis_session=redis_session,
    )


@router.post("/price")
async def create_price(
    request: PriceCreateRequest, session: AsyncSession = Depends(get_sql_session)
) -> PriceResponse:
    try:
        price = await add_price(session, request)
    except IntegrityError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid parent id\nMore info:\n\n{err}"
        )

    return PriceResponse(
        price=price.price,
        matrix_id=price.matrix_id,
        location_id=price.location_id,
        category_id=price.category_id,
    )


@router.get("/price")
async def read_prices(
    total: Annotated[int, Depends(ModelTotalCount(Price))],
    _start: int = 1,
    _end: int = 50,
    session: AsyncSession = Depends(get_sql_session),
) -> List[PriceResponse]:
    prices = await get_prices(session, start=_start, end=_end)
    return [
        PriceResponse(
            price=price.price,
            matrix_id=price.matrix_id,
            location_id=price.location_id,
            category_id=price.category_id,
        )
        for price in prices
    ]


@router.get("/price/{matrix_id}")
async def read_prices_matrix(
    matrix_id: int,
    _start: int = 1,
    _end: int = 50,
    session: AsyncSession = Depends(get_sql_session),
) -> JSONResponse:
    data = [
        PriceResponse(
            price=price.price,
            matrix_id=price.matrix_id,
            location_id=price.location_id,
            category_id=price.category_id,
        ).dict()
        for price in await get_prices(session, matrix_id=matrix_id, start=_start, end=_end)
    ]

    total_count = (await session.execute(select(func.count("*")).select_from(Price).where(
        Price.matrix_id == matrix_id
    ))).scalar()
    return JSONResponse(
        content=data,
        headers={"Access-Control-Expose-Headers": "X-Total-Count", "X-Total-Count": str(total_count)},
    )


@router.get("/price/{category_id}/{location_id}/{matrix_id}")
async def read_price(
    category_id: int,
    location_id: int,
    matrix_id: int,
    session: AsyncSession = Depends(get_sql_session),
) -> PriceResponse:
    price = await get_price(
        session, PriceReadRequest(category_id=category_id, location_id=location_id, matrix_id=matrix_id)
    )
    return PriceResponse(
        price=price.price,
        matrix_id=price.matrix_id,
        location_id=price.location_id,
        category_id=price.category_id,
    )


@router.put("/price")
async def update_price_router(location: PricePutRequest, session: AsyncSession = Depends(get_sql_session)):
    try:
        await set_price(session, location)
    except IntegrityError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid parent id\nMore info:\n\n{err}"
        )
    return {"status": status.HTTP_200_OK}


@router.delete("/price")
async def delete_all_prices(session: AsyncSession = Depends(get_sql_session)) -> Dict:
    await delete_table(session, Price)
    return {"status": status.HTTP_200_OK}


@router.delete("/price/{category_id}/{location_id}/{matrix_id}")
async def delete_price(
    category_id: int, location_id: int, matrix_id: int, session: AsyncSession = Depends(get_sql_session)
):
    try:
        await delete_price(
            session,
            PriceReadRequest(category_id=category_id, location_id=location_id, matrix_id=matrix_id),
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Price wasn't found",
        )

    return {"status": status.HTTP_200_OK}
