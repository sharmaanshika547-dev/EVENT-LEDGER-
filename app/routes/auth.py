from flask import Blueprint, request
import jwt
import datetime 

from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        auth_header = request.headers.get("Authorization")
        print("HEADER:", auth_header)   # 👈 debug

        if not auth_header:
            return {"error": "token missing"}, 401

        try:
            parts = auth_header.split(" ")
            print("PARTS:", parts)      # 👈 debug

            if len(parts) != 2 or parts[0] != "Bearer":
                return {"error": "invalid auth header format"}, 401

            token = parts[1].strip()
            print("TOKEN:", token)      # 👈 debug

            data = jwt.decode(token, "secret_key", algorithms=["HS256"])
            print("DECODED:", data)     # 👈 debug

            request.user_id = data["user_id"]

        except Exception as e:
            print("JWT ERROR:", repr(e))   # 👈 IMPORTANT
            return {"error": "invalid token"}, 401

        return f(*args, **kwargs)

    return decorated

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# temporary in-memory storage
users = {}

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    # 1. no data
    if not data:
        return {"error": "no data provided"}, 400

    # 2. missing fields
    if "email" not in data:
        return {"error": "email required"}, 400

    if "password" not in data:
        return {"error": "password required"}, 400

    email = data["email"]
    password = data["password"]

    # 3. empty fields
    if not email or not password:
        return {"error": "fields cannot be empty"}, 400

    # 4. type check
    if not isinstance(email, str) or not isinstance(password, str):
        return {"error": "invalid data types"}, 400

    # 5. duplicate user
    if email in users:
        return {"error": "user already exists"}, 400

    # 6. hash password (temporary)
    hashed_password = str(hash(password))

    # 7. store user
    users[email] = {
        "password": hashed_password
    }

    return {"message": "user registered successfully"}, 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return {"error": "no data provided"}, 400

    if "email" not in data:
        return {"error": "email required"}, 400

    if "password" not in data:
        return {"error": "password required"}, 400

    email = data["email"]
    password = data["password"]

    if email not in users:
        return {"error": "user not found"}, 404

    if users[email]["password"] != str(hash(password)):
        return {"error": "invalid credentials"}, 401

    payload={
        "email":email,
        "user_id":email,
        "exp":datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }

    token = jwt.encode(payload,"secret_key",algorithm="HS256")
    if isinstance(token, bytes):
        token = token.decode("utf-8")

    return {"token": token}, 200

@auth_bp.route("/test")
def test():
    return {"msg": "auth working"}

