import ssl

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from configurations import _DatabaseSettings

_DATABASE_SETTINGS = _DatabaseSettings()

DATABASE_URL: str = f"postgresql+asyncpg://{_DATABASE_SETTINGS.user}:{_DATABASE_SETTINGS.password}@postgres:5432/" \
                    f"{_DATABASE_SETTINGS.database}"

ssl_context = ssl.create_default_context(cafile="/auth_service/postgres_certs/rootCA.crt")
ssl_context.check_hostname = True
ssl_context.verify_mode = ssl.CERT_REQUIRED

engine = create_async_engine(DATABASE_URL, echo=False,
                             connect_args={
                                 "ssl": ssl_context
                             }
                             )

async_session: AsyncSession = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
