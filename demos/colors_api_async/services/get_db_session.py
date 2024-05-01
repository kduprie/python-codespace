from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from database import sessionmanager

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with sessionmanager.session() as session:
        yield session
