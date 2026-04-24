from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.login_history_model import LoginHistory
from models.user_model import User
from datetime import datetime

login_history_bp = Blueprint("login_history", __name__)


@login_history_bp.route("/", methods=["GET"])
@jwt_required()
def get_login_history():
    query = LoginHistory.query

    username = request.args.get("username")
    from_date = request.args.get("from")
    to_date = request.args.get("to")

    # Filter by username
    if username:
        user = User.query.filter_by(username=username).first()
        if not user:
            return {"error": "User not found"}, 404

        query = query.filter(LoginHistory.user_id == user.id)

    # Date filter
    if from_date:
        query = query.filter(
            LoginHistory.login_time >= datetime.fromisoformat(from_date)
        )

    if to_date:
        query = query.filter(
            LoginHistory.login_time <= datetime.fromisoformat(to_date)
        )

    logs = query.all()

    result = []
    for log in logs:
        result.append({
            "user_id": log.user_id,
            "login_time": log.login_time,
            "logout_time": log.logout_time
        })

    return jsonify(result)