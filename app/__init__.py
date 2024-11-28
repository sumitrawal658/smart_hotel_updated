from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.abspath('instance/smart_hotel.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['REDIS_HOST'] = 'localhost'
    app.config['REDIS_PORT'] = 6379

    db.init_app(app)
    migrate.init_app(app, db)

    # Register the blueprint after initializing the app
    from .routes import bp
    app.register_blueprint(bp)

    return app
