from fastapi import APIRouter, Depends, HTTPException
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from deps.redis_session import get_redis_session
import storage.storage_settings as storage_settings
from deps.sql_session import get_sql_session
from models.matrix import MatrixTypeEnum
from schemas.storage import SetDiscountsRequest, StorageConfResponse
from services.matrices import get_matrix, get_matrix__id_in
from services.storage_logs import add_storage_log
from storage.analytics import get_analytics

router = APIRouter(tags=["storage"])


@router.post("/storage/baseline")
async def set_baseline(
        baseline: int,
        redis_session: Redis = Depends(get_redis_session),
        session: AsyncSession = Depends(get_sql_session),
):
    matrix = await get_matrix(session, baseline)
    if not matrix.type == MatrixTypeEnum.BASE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid baseline matrix id")

    await storage_settings.set_baseline(redis_session, baseline)
    await add_storage_log(session, await storage_settings.get_storage_conf(redis_session))
    return {"status": status.HTTP_200_OK}


@router.post("/storage/discounts")
async def set_discounts(
        discount: SetDiscountsRequest,
        redis_session: Redis = Depends(get_redis_session),
        session: AsyncSession = Depends(get_sql_session),
):
    discounts = await get_matrix__id_in(session, ides=discount.discounts)

    await storage_settings.add_discounts(redis_session, list(map(lambda x: x.id, discounts)))
    await add_storage_log(session, await storage_settings.get_storage_conf(redis_session))
    return {"status": status.HTTP_200_OK}


@router.get("/storage/configuration")
async def read_storage(
        redis_session: Redis = Depends(get_redis_session),
) -> StorageConfResponse:
    return await storage_settings.get_storage_conf(redis_session)


@router.get("/storage/analytics")
async def read_analytics(redis_session: Redis = Depends(get_redis_session)):
    return await get_analytics(redis_session)
