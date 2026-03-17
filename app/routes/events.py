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
