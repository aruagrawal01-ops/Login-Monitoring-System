import os
from dotenv import load_dotenv

load_dotenv()

from flask import Flask
from db import init_db, db
from flask_jwt_extended import JWTManager

# Import routes (we will create these next)
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.login_history_routes import login_history_bp

from models.user_model import User
from models.login_history_model import LoginHistory
from models.otp_model import OTP

def create_app():
    app = Flask(__name__)
    init_db(app)

    app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")
    JWTManager(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(login_history_bp, url_prefix="/login-history")

    return app

app = create_app()

with app.app_context():
    db.create_all()
    print("Tables created successfully!")

if __name__ == "__main__":
    app.run(debug=True)