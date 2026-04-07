from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

# 1. Update the prefix to include +asyncpg to use async driver
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://user:password@localhost/event_ledger_db"

# 2. Use create_async_engine instead of create_engine
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# 3. Use async_sessionmaker for the session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    autoflush=False, 
    class_=AsyncSession, #explicityly tells it to produce asyncsession object 
    autocommit=False, 
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass

# 4. Refactor get_db to be an async generator
async def get_db(): #dependency how fastapi gets acess to db 
    async with AsyncSessionLocal() as session: #context manger handles cleanup 
        try:
            yield session #suspends her,gives session to the route then resumes to close 
        finally:
            await session.close()