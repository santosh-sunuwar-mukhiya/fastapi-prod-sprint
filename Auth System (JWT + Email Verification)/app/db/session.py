from sqlmodel import SQLModel
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.core.config import db_settings, app_settings

# Create async engine with echo based on environment
engine = create_async_engine(
    url=db_settings.DATABASE_URL,
    echo=app_settings.RELOAD  # Only log SQL in development/reload mode
)

# Configure async session factory
# commit_on_expire=False prevents automatic session expiration on commit
AsyncSessionFactory = sessionmaker(
    bind=engine,  # type: ignore
    class_=AsyncSession,
    expire_on_commit=False,
)  # type: ignore


async def create_db_tables():
    """Create all database tables based on SQLModel metadata."""
    async with engine.begin() as connection:
        # Import models to register them with SQLModel.metadata
        from app.db.models import User  # noqa: F401
        await connection.run_sync(SQLModel.metadata.create_all)


async def get_session():
    """
    Dependency for FastAPI to provide database sessions.
    Ensures proper session cleanup even if an error occurs.
    """
    async with AsyncSessionFactory() as session:  # type: ignore
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()