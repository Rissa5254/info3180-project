import os
from flask import Flask, send_from_directory
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .config import Config


app = Flask(
    __name__,
    static_folder="../dist",
    static_url_path=""
)

app.config.from_object(Config)

CORS(app, supports_credentials=True)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))


from app import views


@app.route("/")
def serve_vue():
    return send_from_directory(app.static_folder, "index.html")


@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, "index.html")
