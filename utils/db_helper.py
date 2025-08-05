from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from core.config import settings


class DbHelper:
    def __init__(self,
                 url: str,
                 echo: bool,
                 echo_pool: bool,
                 max_overflow: int,
                 pool_size: int):
        self.engine = create_async_engine(url=url,
                                          echo=echo,
                                          echo_pool=echo_pool,
                                          max_overflow=max_overflow,
                                          pool_size=pool_size)

        self.session_maker = async_sessionmaker(bind=self.engine,
                                                autoflush=False,
                                                expire_on_commit=False,
                                                autocommit=False)

    async def dispose(self):
        await self.engine.dispose()

    async def session_getter(self):
        async with self.session_maker() as session:
            yield session


db_helper = DbHelper(url=str(settings.db.url),
                     echo=settings.db.echo,
                     echo_pool=settings.db.echo_pool,
                     max_overflow=settings.db.max_overflow,
                     pool_size=settings.db.pool_size)