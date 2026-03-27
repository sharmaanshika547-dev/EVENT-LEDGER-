from flask import Flask
from app.routes.events import events_bp
from app.routes.auth import auth_bp
from app.extensions import db

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///events.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

    db.init_app(app)

    app.register_blueprint(events_bp)
    app.register_blueprint(auth_bp)

    return app
