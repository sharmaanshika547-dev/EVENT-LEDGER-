from flask import Blueprint ,request

events_bp = Blueprint("events",__name__)


events ={}
event_id=1
@events_bp.route("/events", methods=["POST"])
def create_events():
    global event_id

    data = request.get_json()

    # 1. no data
    if not data:
        return {"error": "no data provided"}, 400

    # 2. missing title
    if "title" not in data:
        return {"error": "title is required"}, 400

    # 3. empty title
    if not data["title"]:
        return {"error": "title cannot be empty"}, 400

    # 4. type check
    if not isinstance(data["title"], str):
        return {"error": "title must be a string"}, 400

    # create event
    events[event_id] = data["title"]

    response = {
        "id": event_id,
        "title": data["title"]
    }

    event_id += 1

    return response, 201
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
    data=request.get_json()
    if not data:
        return {"error":"no data provided"},400
    if "title" not in data:
        return {"error":"title required"},400
    if not data["title"]:
        return {"error":"title cant be empty"},400
    if not isinstance(data["title",str]):
        return {"error":"title must be a string"},400

        events[id] = data["title"]
        return {
            "id": id,
            "event": events[id]
        }, 200
    else:
        return {"error": "Event not found"}, 404
    
@events_bp.route("/events/<int:id>", methods=["GET"])
def get_event(id):
    if id in events:
        return {
            "id": id,
            "event": events[id]
        }, 200
    else:
        return {"error": "Event not found"}, 404
