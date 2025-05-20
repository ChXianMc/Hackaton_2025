import os
import logging
from datetime import timedelta

from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_login import LoginManager


# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET") or "dev-secret-key-fixed"  # Use a fallback for development
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)  # needed for url_for to generate with https

# configure the database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///healthcare.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Mejoras de seguridad
app.config["SESSION_COOKIE_SECURE"] = True  # Cookies solo por HTTPS
app.config["SESSION_COOKIE_HTTPONLY"] = True  # Evita acceso a cookies desde JavaScript
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)  # Sesión expira después de 30 min
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"  # Previene CSRF
app.config["WTF_CSRF_ENABLED"] = True  # Activa protección CSRF en formularios

# Set up Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

# initialize the app with the extension, flask-sqlalchemy >= 3.0.x
db.init_app(app)

with app.app_context():
    # Make sure to import the models here or their tables won't be created
    import models  # noqa: F401
    
    # Create all database tables
    db.create_all()
    
    # Import routes after database is initialized
    from routes import *  # noqa: F401, F403
    
    # Create test users
    from routes import create_test_users
    create_test_users()

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))
