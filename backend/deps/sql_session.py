from sqlalchemy.ext.asyncio import AsyncSession

from models.engine import async_session


async def get_sql_session() -> AsyncSession:
    async with async_session() as session:
        yield session
