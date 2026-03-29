from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    # Logic: Force the password to be cut at 72 characters no matter what.
    # This prevents the '72 bytes' crash.
    safe_password = password[:72] 
    return pwd_context.hash(safe_password)

def verify_password(plain_password, hashed_password):
    # Logic: Do the same cut here so they match!
    safe_password = plain_password[:72]
    return pwd_context.verify(safe_password, hashed_password)