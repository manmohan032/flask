from flask import Flask
from app.routes.users import users_bp
from app.routes.auth import auth_bp
from app.models.user import User

def create_app():
    app = Flask(__name__)

    # Initialize database (ensure table exists)
    User.create_table()

    # Register blueprints
    app.register_blueprint(users_bp)
    app.register_blueprint(auth_bp)

    # Health check
    @app.route('/')
    def home():
        return {"message": "User Management System"}, 200

    return app
