from typing import AsyncGenerator

from sqlalchemy.orm import DeclarativeBase, declared_attr

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.config import settings
from utils.case_converter import camel_case_to_snake_case


class Base(DeclarativeBase):

    @declared_attr
    def __tablename__(cls):
        return f'{camel_case_to_snake_case(cls.__name__.lower())}s'


class DatabaseHelper:
    def __init__(
        self,
        url: str,
        echo: bool = False,
        echo_pool: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
    ):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
        )

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session

    async def dispose(self) -> None:
        await self.engine.dispose()


db_helper = DatabaseHelper(
    url=str(settings.database_url)
)