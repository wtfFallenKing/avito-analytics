from typing import Annotated, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from deps.pagination import ModelTotalCount
from deps.sql_session import get_sql_session
from models import Matrix
from schemas.matrix_logs import MatrixLogResponse
from services.matrix_logs import get_matrices_logs, get_matrix_logs

router = APIRouter(tags=["logs"])


@router.get("/matrix_logs")
async def read_matrices_logs(
    total: Annotated[int, Depends(ModelTotalCount(Matrix))],
    _start: int = 1,
    _end: int = 50,
    session: AsyncSession = Depends(get_sql_session),
) -> List[MatrixLogResponse]:
    matrices = await get_matrices_logs(session, start=_start, end=_end)
    return [
        MatrixLogResponse(
            id=matrix.id, matrix_id=matrix.matrix_id, type=matrix.type, happened_at=matrix.happened_at
        )
        for matrix in matrices
    ]


@router.get("/matrix_logs/{matrix_id}")
async def read_matrix_logs(
    total: Annotated[int, Depends(ModelTotalCount(Matrix))],
    matrix_id: int,
    _start: int = 1,
    _end: int = 50,
    session: AsyncSession = Depends(get_sql_session),
) -> List[MatrixLogResponse]:
    matrices = await get_matrix_logs(session, matrix_id)
    return [
        MatrixLogResponse(
            id=matrix.id, matrix_id=matrix.matrix_id, type=matrix.type, happened_at=matrix.happened_at
        )
        for matrix in matrices
    ]
