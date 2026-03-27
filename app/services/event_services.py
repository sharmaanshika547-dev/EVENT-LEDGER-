from app.models.event import Event 
def get_events(user_id,db,title=None,date=None):
	query = Event.query.filter_by(user_id=user_id)

	if title:
		query= query.filter(Event.title==title)

	if date:
		query= query.filter(Event.date==date)

	return query.all 
