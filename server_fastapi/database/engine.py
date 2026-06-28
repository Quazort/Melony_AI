from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from core.config import settings
from core.logger import get_logger


class DatabaseSessionManager:
    def __init__(self):
        self._engine = None
        self._sessionmaker = None
        self.db_url = settings.DATABASE_URL
        self.logger = get_logger("postgresql")

    def init(self):
        if self._engine is None:
            self._engine = create_async_engine(
                url=self.db_url,
                echo=True,
                pool_size=10,
                max_overflow=20
            )
            self._sessionmaker = async_sessionmaker(
                bind=self._engine,
                expire_on_commit=False,
                class_=AsyncSession,
                autoflush=True)
            self.logger.info("База данных PostgreSQL инициализирована")

    async def close(self):
        if self._engine is None:
            return
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None
        self.logger.info("База данных PostgreSQL закрыта")

    async def get_session(self):
        if self._sessionmaker is None:
            self.logger.error("База данных PostgreSQL инициализирована с ошибкой")
            raise IOError("База данных инициализирована с ошибкой!")
        async with self._sessionmaker() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                self.logger.error(f"Ошибка PostgreSQL: {e}")
                raise e


db_manager = DatabaseSessionManager()
