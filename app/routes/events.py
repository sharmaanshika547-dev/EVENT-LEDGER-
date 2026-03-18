from flask import Blueprint 

events_bp = Blueprint("events",__name__)


events ={}
event_id=1

@events_bp.route("/events",methods=["POST"])

def create_events():
	global event_id
	data = request.get_json()
	events[event_id]=data
	response={
		"id":event_id,
		"event":data
	}
	event_id+=1

	return response,201

@events_bp.route("/events", methods=["GET"])
def get_events():
	return {"events": events}

@events_bp.route("/events/<int:id>", methods=["DELETE"])
def delete_event(id):
    if id in events:
        del events[id]
        return {"message": "Event deleted"}, 200
    else:
        return {"error": "Event not found"}, 404

@events_bp.route("/events/<int:id>", methods=["PUT"])
def update_event(id):
    if id in events:
        data = request.get_json()
        events[id] = data
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