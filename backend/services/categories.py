from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from sqlalchemy import update
from models.category import Category
from schemas.categories import CategoryCreateRequest, CategoryPutRequest


async def get_categories(session: AsyncSession, start: int = 1, end: int = 50) -> List[Category]:
    page = end - start + 1
    result = await session.execute(select(Category).offset(page * (start // page)).limit(page))

    return [
        Category(id=res.id, key=res.key, name=res.name, parent_id=res.parent_id)
        for res in result.scalars().all()
    ]


async def set_category(session: AsyncSession, category_id: int, category: CategoryPutRequest) -> Category:
    result = (await session.execute(
        update(Category)
        .where(Category.id == category_id)
        .values(name=category.name)
        .returning(Category)
    )).scalar()
    await session.commit()
    return Category(id=result.id, key=result.key, name=result.name, parent_id=result.parent_id)


async def get_category(session: AsyncSession, category_id: int) -> Category:
    result = (await session.execute(select(Category).where(Category.id == category_id))).scalar()
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid category id")

    return Category(id=result.id, key=result.key, name=result.name, parent_id=result.parent_id)


async def add_category(session: AsyncSession, category: CategoryCreateRequest) -> Category:
    parent = await get_category(session, category.parent_id)
    if parent is None:
        raise ValueError("Invalid parent id")

    new_category = Category(id=category.id, name=category.name, parent_id=category.parent_id)
    new_category.key = f"{category.id}-{parent.key}"

    session.add(new_category)
    await session.commit()

    return new_category
