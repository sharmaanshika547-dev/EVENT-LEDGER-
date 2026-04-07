from sqlalchemy import select 
from sqlalchemy.ext.asyncio import AsyncSession 
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

# New Imports for Login Logic
from app.database import get_db
from app.models.user import User
from app.utils import verify_password
from pydantic import BaseModel
from app.utils import hash_password

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()

# Settings
SECRET_KEY = "your_secret_key_here" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 # Token dies after 1 hour for security

# --- 1. THE SCHEMA (The Input Contract) ---
class LoginRequest(BaseModel):
    username: str
    password: str

# --- 2. THE TOKEN GENERATOR (The "Office") ---
def create_access_token(data: dict):
    """Logic: Creates a scrambled JWT string that expires."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --- 3. THE LOGIN ROUTE ---
@router.post("/login")
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    # Logic: Look for the user in the DB
    user = db.query(User).filter(User.username == login_data.username).first()
    
    # Logic: If user doesn't exist OR password doesn't match the hash
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Logic: Give them their "ID Card" (Token)
    token = create_access_token(data={"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}

# --- 4. THE BOUNCER (Your original code) ---
async def get_current_user(auth: HTTPAuthorizationCredentials = Depends(security)):
    token = auth.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token invalid")
        return user_id
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
# --- ADD THIS SIGNUP ROUTE ---

@router.post("/signup")
async def signup(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # 1. Check if user exists (Async style)
    query = select(User).where(User.email == user_data.email)
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash(user_data.password)

    # 2. Create new user
    new_user = User(email=user_data.email, password=hashed_password)
    db.add(new_user)
    
    # 3. Await the commit and refresh
    await db.commit()
    await db.refresh(new_user)
    return new_user