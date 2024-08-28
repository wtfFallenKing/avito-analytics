from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.storage_logs import StorageLogs
from schemas.storage import StorageConfResponse


async def get_storage_logs(session: AsyncSession, start: int = 1, end: int = 50) -> List[StorageLogs]:
    page = end - start + 1
    result = await session.execute(
        select(StorageLogs)
        .offset(page * (start // page))
        .limit(page)
        .order_by(StorageLogs.happened_at.desc())
    )

    return [
        StorageLogs(id=res.id, baseline=res.baseline, discounts=res.discounts, happened_at=res.happened_at)
        for res in result.scalars().all()
    ]


async def add_storage_log(session: AsyncSession, storage: StorageConfResponse) -> StorageLogs:
    new_storage = StorageLogs(baseline=storage.baseline, discounts=storage.discounts)

    session.add(new_storage)
    await session.commit()

    return new_storage
