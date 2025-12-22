import ssl

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from configurations import _DatabaseSettings

_DATABASE_SETTINGS = _DatabaseSettings()

DATABASE_URL: str = f"postgresql+asyncpg://{_DATABASE_SETTINGS.user}:{_DATABASE_SETTINGS.password}@postgres:5432/" \
                    f"{_DATABASE_SETTINGS.database}"

_ssl_context = ssl.create_default_context(cafile="/channel_actions/certs/postgres/rootCA.crt")
_ssl_context.check_hostname = True
_ssl_context.verify_mode = ssl.CERT_REQUIRED

engine = create_async_engine(DATABASE_URL, echo=False, connect_args={"ssl": _ssl_context})

async_session: AsyncSession = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
