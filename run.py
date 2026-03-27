from flask import Flask 
from app import create_app,db
from app.models.event import Event

app = create_app()
with app.app_context():
	db.create_all()
	print("DB created")

	event = Event(title="fest",user_id=1)
	db.session.add(event)
	db.session.commit()
	
if __name__ == "__main__":
	app.run(debug=True)
