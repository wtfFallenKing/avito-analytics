from typing import List

from fastapi import HTTPException
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from models.matrix import Matrix, MatrixTypeEnum
from schemas.matrices import MatrixCreateRequest, MatrixPutRequest


async def get_matrices(session: AsyncSession, start: int = 1, end: int = 50) -> List[Matrix]:
    page = end - start + 1
    result = await session.execute(select(Matrix).offset(page * (start // page)).limit(page))

    return [
        Matrix(id=res.id, name=res.name, type=res.type, segment_id=res.segment_id)
        for res in result.scalars().all()
    ]


async def get_matrix(session: AsyncSession, matrix_id: int) -> Matrix:
    result = (await session.execute(select(Matrix).where(Matrix.id == matrix_id))).scalar()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="matrix wasn't found")

    return Matrix(id=result.id, name=result.name, type=result.type, segment_id=result.segment_id)


async def set_matrix(session: AsyncSession, matrix_id: int, matrix: MatrixPutRequest):
    result = (await session.execute(
        update(Matrix)
        .where(Matrix.id == matrix_id)
        .values(
            name=matrix.name,
            segment_id=matrix.segment_id,
            type=MatrixTypeEnum.DISCOUNT if matrix.segment_id else MatrixTypeEnum.BASE,
        ).returning(Matrix)
    )).scalar()
    await session.commit()

    return Matrix(id=result.id, name=result.name, type=result.type, segment_id=result.segment_id)



async def get_matrix__id_in(
    session: AsyncSession, ides: List[int], matrix_type: str = MatrixTypeEnum.DISCOUNT
) -> List[Matrix]:
    result = await session.execute(select(Matrix).where(Matrix.id.in_(ides), Matrix.type == matrix_type))
    return [
        Matrix(id=res.id, name=res.name, type=res.type, segment_id=res.segment_id)
        for res in result.scalars().all()
    ]


async def add_matrix(session: AsyncSession, matrix: MatrixCreateRequest) -> Matrix:
    new_matrix = Matrix(name=matrix.name, type=matrix.type, segment_id=matrix.segment_id)

    session.add(new_matrix)
    await session.commit()

    return new_matrix


async def delete_matrix_by_id(session: AsyncSession, matrix_id: int):
    await session.execute(delete(Matrix).where(Matrix.id == matrix_id))
    await session.commit()
