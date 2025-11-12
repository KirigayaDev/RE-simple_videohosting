from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from configurations import DatabaseSettings

_DATABASE_SETTINGS = DatabaseSettings()


DATABASE_URL: str = f"postgresql+asyncpg://{_DATABASE_SETTINGS.user}:{_DATABASE_SETTINGS.password}@postgres:5432/" \
               f"{_DATABASE_SETTINGS.database}"
engine = create_async_engine(DATABASE_URL, echo=False)

async_session: AsyncSession = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
