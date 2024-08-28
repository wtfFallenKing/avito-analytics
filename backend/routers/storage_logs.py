from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from deps.pagination import ModelTotalCount
from deps.sql_session import get_sql_session
from models import Matrix
from schemas.storage import StorageLogsResponse
from services.storage_logs import get_storage_logs

router = APIRouter(tags=["logs"])


@router.get("/storage_logs")
async def read_matrices_logs(
    total: Annotated[int, Depends(ModelTotalCount(Matrix))],
    _start: int = 1,
    _end: int = 50,
    session: AsyncSession = Depends(get_sql_session),
) -> List[StorageLogsResponse]:
    storage_logs = await get_storage_logs(session, start=_start, end=_end)
    return [
        StorageLogsResponse(
            id=storage_log.id,
            baseline=storage_log.baseline,
            discounts=storage_log.discounts,
            happened_at=storage_log.happened_at,
        )
        for storage_log in storage_logs
    ]
