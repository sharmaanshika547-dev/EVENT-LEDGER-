from flask import Flask 
from app.routes.events import events_bp


def create_app():
	app=Flask(__name__)

	app.register_blueprint(events_bp)
	return app 
