from typing import Any, Annotated
from fastapi import Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from deps.sql_session import get_sql_session


class ModelTotalCount:
    def __init__(self, model: type):
        self.model = model

    async def __call__(
        self, session: Annotated[AsyncSession, Depends(get_sql_session)], response: Response
    ) -> Any:
        response.headers.append("Access-Control-Expose-Headers", "X-Total-Count")
        total_count = (await session.execute(select(func.count("*")).select_from(self.model))).scalar()
        response.headers.append("X-Total-Count", str(total_count))
        return total_count
