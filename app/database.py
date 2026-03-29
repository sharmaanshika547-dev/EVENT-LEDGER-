from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Logic: Define where the database file sits
SQLALCHEMY_DATABASE_URL = "sqlite:///./momentum.db"

# 2. Logic: Create the Engine (The actual connection)
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# 3. Logic: The Session (The 'bridge' we use to talk to the DB)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Logic: The Base class (All our models will inherit from this)
Base = declarative_base()

# 5. The "Dependency" (The key to keeping your app fast)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()