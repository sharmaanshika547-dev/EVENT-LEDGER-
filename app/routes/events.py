print("EVENTS FILE LOADED")
import jwt 
from flask import Blueprint ,request
    
events_bp = Blueprint("events",__name__)


events ={}
event_id=1


@events_bp.route("/events", methods=["POST"])
def create_events():
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return {"error": "token missing"}, 401
    try:
        token = auth_header.split(" ")[1]
        decoded = jwt.decode(token, "secret_key", algorithms=["HS256"])
        print("USER:", decoded)  # debug
    except Exception as e:
        print("JWT ERROR:", e)
        return {"error": "invalid token"}, 401

    data = request.get_json()

    if not data:
        return {"error": "no data"}, 400

    return {"msg": "working"}, 200
   

@events_bp.route("/events", methods=["GET"])
def get_events():
	return {"events": events}

@events_bp.route("/events/<int:id>", methods=["DELETE"])
def delete_event(id):

    if id in events:
        del events[id]
        return {"message": f"Event {id} deleted"}, 204
    else:
        return {"error": "Event not found"}, 404

@events_bp.route("/events/<int:id>", methods=["PUT"])
def update_event(id):
    if id not in events:
        return {"error":"event not found"},404

    data = request.get_json()

    if not data:
        return {"error":"no data provided"},400

    if "title" not in data:
        return {"error":"title required"},400

    if not data["title"]:
        return {"error":"title cant be empty"},400

    if not isinstance(data["title"], str):
        return {"error":"title must be a string"},400

    events[id] = data["title"]

    return {
        "id": id,
        "event": events[id]
    }, 200
    
@events_bp.route("/events/<int:id>", methods=["GET"])
def get_event(id):
    if id in events:
        return {
            "id": id,
            "event": events[id]
        }, 200
    else:
        return {"error": "Event not found"}, 404
