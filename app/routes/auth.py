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
def signup(user_in: LoginRequest, db: Session = Depends(get_db)):
    # 1. Logic: Check if the username is already taken
    print(f"DEBUG: Password received is: {user_in.password}")
    existing_user = db.query(User).filter(User.username == user_in.username).first()
    if existing_user:
        # Term: '400 Bad Request' -> The server says "I can't do that because the data is wrong"
        raise HTTPException(status_code=400, detail="Username already exists")

    # 2. Logic: Scramble the password using our utility and save it
    new_user = User(
        username=user_in.username, 
        hashed_password=hash_password(user_in.password) # From app.utils
    )
    
    db.add(new_user)
    db.commit() # This physically writes the row into momentum.db
    db.refresh(new_user) # This grabs the new ID the database assigned
    
    return {"message": "User created successfully!", "user_id": new_user.id}