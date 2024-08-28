from typing import Annotated, List, Optional, Dict

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from redis.asyncio import Redis
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from deps.pagination import ModelTotalCount
from deps.redis_session import get_redis_session
from deps.sql_session import get_sql_session
from models import Matrix
from models.matriciets_logs import MatrixLogsTypeEnum
from schemas.matrices import (
    MatrixResponse,
    MatrixCreateRequest,
    MatrixTypePydantic,
    MatrixPutRequest,
)
from services.matrices import get_matrices, get_matrix, add_matrix, delete_matrix_by_id, set_matrix
from services.matrix_logs import add_matrix_log
from services.nodes import add_prices, delete_table
from storage.storage_settings import get_storage_conf

router = APIRouter(tags=["matrices"])


@router.post("/matrix")
async def create_matrix(
        name: str,
        file: UploadFile,
        segment_id: Optional[int] = None,
        session: AsyncSession = Depends(get_sql_session),
) -> MatrixResponse:
    try:
        # cat loc price
        matrix = await add_matrix(
            session,
            MatrixCreateRequest(
                type=(MatrixTypePydantic.DISCOUNT if segment_id is not None else MatrixTypePydantic.BASE),
                name=name,
                segment_id=segment_id,
            ),
        )  # add metadata
        await add_prices(session, file, matrix)  # add data
        await add_matrix_log(session, matrix_id=matrix.id, matrix_type=MatrixLogsTypeEnum.CREATE)

    except IntegrityError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid parent id\nMore info:\n\n{err}",
        )

    return MatrixResponse(id=matrix.id, name=matrix.name, type=matrix.type, segment_id=matrix.segment_id)


@router.get("/matrix")
async def read_matrices(
        total: Annotated[int, Depends(ModelTotalCount(Matrix))],
        _start: int = 1,
        _end: int = 50,
        session: AsyncSession = Depends(get_sql_session),
) -> List[MatrixResponse]:
    matrices = await get_matrices(session, start=_start, end=_end)
    return [
        MatrixResponse(id=matrix.id, name=matrix.name, type=matrix.type, segment_id=matrix.segment_id)
        for matrix in matrices
    ]


@router.get("/matrix/{matrix_id}")
async def read_matrix(matrix_id: int, session: AsyncSession = Depends(get_sql_session)) -> MatrixResponse:
    matrix = await get_matrix(session, matrix_id)
    return MatrixResponse(id=matrix.id, name=matrix.name, type=matrix.type, segment_id=matrix.segment_id)


@router.put("/matrix/{matrix_id}")
async def update_matrix(
        matrix_id: int, matrix: MatrixPutRequest, session: AsyncSession = Depends(get_sql_session)
) -> MatrixResponse:
    try:
        result = await set_matrix(session, matrix_id, matrix)
        await add_matrix_log(session, matrix_id=matrix_id, matrix_type=MatrixLogsTypeEnum.UPDATE)
    except IntegrityError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid parent id\nMore info:\n\n{err}"
        )
    return MatrixResponse(id=result.id, name=result.name, type=result.type, segment_id=result.segment_id)


@router.delete("/matrix")
async def delete_all_matrices(session: AsyncSession = Depends(get_sql_session)) -> Dict:
    await delete_table(session, Matrix)
    return {"status": status.HTTP_200_OK}


@router.delete("/matrix/{matrix_id}")
async def delete_matrix(
        matrix_id: int,
        session: AsyncSession = Depends(get_sql_session),
        redis_session: Redis = Depends(get_redis_session),
):
    try:
        storage = await get_storage_conf(redis_session, need_raise=False)
        if matrix_id == storage.baseline or matrix_id in storage.discounts:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"You are trying to delete matrix from storage, please set it before deletion",
            )

        await add_matrix_log(session, matrix_id=matrix_id, matrix_type=MatrixLogsTypeEnum.DELETE)
        await delete_matrix_by_id(session, matrix_id)
    except IntegrityError as err:
        print(err)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Matrix wasn't found")

    return {"status": status.HTTP_200_OK}
