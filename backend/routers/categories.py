from typing import List, Dict, Annotated

from fastapi import APIRouter, Depends, UploadFile, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from deps.pagination import ModelTotalCount
from deps.sql_session import get_sql_session
from models.category import Category
from schemas.categories import CategoryCreateRequest, CategoryResponse, CategoryPutRequest
from services.categories import get_categories, get_category, add_category, set_category
from services.nodes import add_nodes_pack, delete_table, delete_instance

router = APIRouter(tags=["categories"])


@router.post("/category")
async def create_category(
        request: CategoryCreateRequest, session: AsyncSession = Depends(get_sql_session)
) -> CategoryResponse:
    try:
        category = await add_category(session, request)
    except (IntegrityError, ValueError) as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid parent id\nMore info:\n\n{err}"
        )
    return CategoryResponse(
        id=category.id, key=category.key, name=category.name, parent_id=category.parent_id
    )


@router.post("/category/csv")
async def upload_csv(file: UploadFile, session: AsyncSession = Depends(get_sql_session)):
    try:
        await add_nodes_pack(session, file, Category)
    except IntegrityError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid parent id\nMore info:\n\n{err}"
        )

    return {"status": status.HTTP_200_OK}


@router.get("/category")
async def read_categories(
        total: Annotated[int, Depends(ModelTotalCount(Category))],
        _start: int = 1,
        _end: int = 50,
        session: AsyncSession = Depends(get_sql_session),
) -> List[CategoryResponse]:
    categories = await get_categories(session, start=_start, end=_end)
    return [
        CategoryResponse(id=category.id, key=category.key, name=category.name, parent_id=category.parent_id)
        for category in categories
    ]


@router.get("/category/{category_id}")
async def read_category(
        category_id: int, session: AsyncSession = Depends(get_sql_session)
) -> CategoryResponse:
    category = await get_category(session, category_id)
    return CategoryResponse(
        id=category.id, key=category.key, name=category.name, parent_id=category.parent_id
    )


@router.put("/category/{category_id}")
async def update_category(
        category_id: int, category: CategoryPutRequest, session: AsyncSession = Depends(get_sql_session)
) -> CategoryResponse:
    try:
        result = await set_category(session, category_id, category)
    except IntegrityError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid parent id\nMore info:\n\n{err}"
        )

    return CategoryResponse(
        id=result.id, key=result.key, name=result.name, parent_id=result.parent_id
    )


@router.delete("/category")
async def delete_all_categories(session: AsyncSession = Depends(get_sql_session)) -> Dict:
    await delete_table(session, Category)
    return {"status": status.HTTP_200_OK}


@router.delete("/category/{category_id}")
async def read_location(category_id: int, session: AsyncSession = Depends(get_sql_session)):
    await delete_instance(session, category_id, Category)
    return {"status": status.HTTP_200_OK}
