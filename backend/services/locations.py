from typing import List

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from models.location import Location
from schemas.locations import LocationCreateRequest, LocationPutRequest


async def get_locations(session: AsyncSession, start: int = 1, end: int = 50) -> List[Location]:
    page = end - start + 1
    result = await session.execute(select(Location).offset(page * (start // page)).limit(page))

    return [
        Location(id=res.id, key=res.key, name=res.name, parent_id=res.parent_id)
        for res in result.scalars().all()
    ]


async def set_location(session: AsyncSession, location_id: int, location: LocationPutRequest):
    result = (await session.execute(
        update(Location)
        .where(Location.id == location_id)
        .values(name=location.name)
        .returning(Location)
    )).scalar()
    await session.commit()

    return Location(id=result.id, key=result.key, name=result.name, parent_id=result.parent_id)


async def get_location(session: AsyncSession, location_id: int) -> Location:
    result = (await session.execute(select(Location).where(Location.id == location_id))).scalar()
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid location id")

    return Location(id=result.id, key=result.key, name=result.name, parent_id=result.parent_id)


async def add_location(session: AsyncSession, location: LocationCreateRequest) -> Location:
    parent = await get_location(session, location.parent_id)
    if parent is None:
        raise ValueError("Invalid parent id")

    new_location = Location(id=location.id, name=location.name, parent_id=location.parent_id)
    new_location.key = f"{location.id}-{parent.key}"

    session.add(new_location)
    await session.commit()

    return new_location
