from flask import Flask
from .models import db
from dotenv import load_dotenv

load_dotenv()


def create_app():

    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app