from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///arena.db'

    db.init_app(app)
    login_manager.init_app(app)

    from .auth_routes import auth_bp
    from .game_routes import game_bp
    from .game_routes_extra import extra_bp 

    app.register_blueprint(auth_bp, url_prefix="/")
    app.register_blueprint(game_bp, url_prefix="/")
    app.register_blueprint(extra_bp, url_prefix="/") 

    return app
