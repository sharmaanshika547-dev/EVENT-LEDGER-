import jwt 
from flask import Blueprint ,request
from app.models.event import Event
from app.services.event_services import get_events
from app.extensions import db 
from app.routes.auth import token_required
events_bp = Blueprint("events",__name__)


events ={}
event_id=1


@events_bp.route("/events", methods=["POST"])
@token_required
def create_events():
    auth_header = request.headers.get("Authorization")
    print("HEADER:", auth_header) 
    if not auth_header:
        return {"error": "token missing"}, 401
    try:
        token = auth_header.split(" ")[1]
        decoded = jwt.decode(token, "secret_key", algorithms=["HS256"])
        current_user_id = decoded["user_id"]
        print("USER:", decoded)  # debug
    except Exception as e:
        print("JWT ERROR:", e)
        return {"error": "invalid token"}, 401

    data = request.get_json()

    if "title" not in data:
        return {"error": "title required"}, 400

    if not data["title"]:
        return {"error": "title cannot be empty"}, 400

    if not isinstance(data["title"], str):
        return {"error": "title must be string"}, 400

    

    event = Event(
        user_id = current_user_id,
        title=data["title"],
        date=data.get("data")
)
    db.session.add(event)
    db.session.commit()

    return {"msg": "working",
            "event":event.to_dict()
    },201
   

@events_bp.route("/events", methods=["GET"])
@token_required
def fetch_events():
    current_user_id = request.user_id

    events = Event.query.filter_by(user_id=current_user_id).all()

    return {
        "events": [e.to_dict() for e in events]
    }

@events_bp.route("/events/<int:id>", methods=["DELETE"])
@token_required
def delete_event(id):

    event = Event.query.get(id)

    if not event:
        return {"error": "event not found"}, 404

    if event.user_id != request.user_id:
        return {"error": "forbidden"}, 403

    db.session.delete(event)
    db.session.commit()

    print("EVENT USER:", event.user_id)
    print("REQUEST USER:", request.user_id)
    return {"message": "event deleted"}, 200

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
    current_user_id=request.user_id

    event = next((e for e in events if e["id"]==id),None)

    if not event:
        return {"error":"event not found"},404
    if event["user_id"]!=current_user_id:
        return{"errror":"forbidden"},403
    
    return {"events":event}

    
