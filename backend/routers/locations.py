from typing import Annotated, List, Dict

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from deps.pagination import ModelTotalCount

from deps.sql_session import get_sql_session
from models.location import Location
from schemas.locations import LocationCreateRequest, LocationResponse, LocationPutRequest
from services.locations import get_locations, get_location, add_location, set_location
from services.nodes import add_nodes_pack, delete_table, delete_instance

router = APIRouter(tags=["locations"])


@router.post("/location")
async def create_location(
        request: LocationCreateRequest, session: AsyncSession = Depends(get_sql_session)
) -> LocationResponse:
    try:
        location = await add_location(session, request)
    except (IntegrityError, ValueError) as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid parent id\nMore info:\n\n{err}"
        )

    return LocationResponse(
        id=location.id, key=location.key, name=location.name, parent_id=location.parent_id
    )


@router.post("/location/csv")
async def upload_csv(file: UploadFile, session: AsyncSession = Depends(get_sql_session)):
    try:
        await add_nodes_pack(session, file, Location)
    except IntegrityError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid parent id\nMore info:\n\n{err}"
        )

    return {"status": status.HTTP_200_OK}


@router.get("/location")
async def read_locations(
        total: Annotated[int, Depends(ModelTotalCount(Location))],
        _start: int = 1,
        _end: int = 50,
        session: AsyncSession = Depends(get_sql_session),
) -> List[LocationResponse]:
    locations = await get_locations(session, start=_start, end=_end)
    return [
        LocationResponse(id=location.id, key=location.key, name=location.name, parent_id=location.parent_id)
        for location in locations
    ]


@router.get("/location/{location_id}")
async def read_location(
        location_id: int, session: AsyncSession = Depends(get_sql_session)
) -> LocationResponse:
    location = await get_location(session, location_id)
    return LocationResponse(
        id=location.id, key=location.key, name=location.name, parent_id=location.parent_id
    )


@router.put("/location/{location_id}")
async def update_location(
        location_id: int, location: LocationPutRequest, session: AsyncSession = Depends(get_sql_session)
) -> LocationResponse:
    try:
        result = await set_location(session, location_id, location)
    except IntegrityError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid parent id\nMore info:\n\n{err}"
        )
    return LocationResponse(
        id=result.id, key=result.key, name=result.name, parent_id=result.parent_id
    )


@router.delete("/location")
async def delete_all_locations(session: AsyncSession = Depends(get_sql_session)) -> Dict:
    await delete_table(session, Location)
    return {"status": status.HTTP_200_OK}


@router.delete("/location/{location_id}")
async def delete_location(location_id: int, session: AsyncSession = Depends(get_sql_session)):
    await delete_instance(session, location_id, Location)
    return {"status": status.HTTP_200_OK}
