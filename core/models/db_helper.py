from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session, AsyncSession
from ..config import settings
from asyncio import current_task


class DatabaseHelper:

    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):   # Для передачи сессии в views
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=lambda: None,
        )
        return session
    
    async def session_dependency(self):                     # 1 способ передачи сессии
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def scoped_session_dependency(self):              # 2 способ передачи сессии
        session = self.get_scoped_session()
        yield session
        await session.close()




db_helper = DatabaseHelper(
    url=settings.db_url, 
    echo=settings.db_echo
)