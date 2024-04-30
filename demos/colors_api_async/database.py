import contextlib
from typing import AsyncIterator, AsyncGenerator

from sqlalchemy.ext.asyncio import(
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

DATABASE_URL = "sqlite+aiosqlite:///./colors_api_async.sqlite3"

class DatabaseSessionManager:

    engine: AsyncEngine | None
    sessionmaker: async_sessionmaker[AsyncSession] | None

    def __init__(self) -> None:
        self.engine = create_async_engine(
            DATABASE_URL,
            connect_args={"check_same_thread": False},
            echo = True,
        )
        self.sessionmaker = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
        )

    async def close(self) -> None:
        if self.engine is None:
            raise Exception("Database Session Manager is not initialized")
        await self.engine.dispose()

        self.engine = None
        self.sessionmaker = None

    # cleans up stuff when you exit async block
    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self.engine is None:
            raise Exception("Database Session Manager is not initialized")

        async with self.engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self.engine is None or self.sessionmaker is None:
            raise Exception("Database Session Manager is not initialized")

        session = self.sessionmaker()

        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

sessionmanager = DatabaseSessionManager()

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with sessionmanager.session() as session:
        yield session
