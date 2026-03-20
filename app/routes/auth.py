from flask import Blueprint, request

auth_bp = Blueprint("auth", __name__)

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

    # temporary token
    token = "logged_in_user"

    return {"token": token}, 200