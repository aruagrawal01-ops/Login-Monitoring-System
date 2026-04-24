from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from models.user_model import User
from datetime import datetime

user_bp = Blueprint("users", __name__)


@user_bp.route("/", methods=["GET"])
@jwt_required()
def get_users():
    query = User.query

    # 🔍 FILTERS
    name = request.args.get("name")
    starts_with = request.args.get("starts_with")
    start_letter = request.args.get("start_letter")
    end_letter = request.args.get("end_letter")
    created_from = request.args.get("created_from")
    created_to = request.args.get("created_to")

    # Name contains
    if name:
        query = query.filter(User.username.ilike(f"%{name}%"))

    # Starts with
    if starts_with:
        query = query.filter(User.username.ilike(f"{starts_with}%"))

    # Range (A → C)
    if start_letter and end_letter:
        query = query.filter(
            User.username >= start_letter,
            User.username < chr(ord(end_letter) + 1)
        )

    # Date filters
    if created_from:
        query = query.filter(
            User.created_at >= datetime.fromisoformat(created_from)
        )

    if created_to:
        query = query.filter(
            User.created_at <= datetime.fromisoformat(created_to)
        )

    # 📄 PAGINATION
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)

    paginated = query.paginate(page=page, per_page=limit, error_out=False)

    users = []
    for user in paginated.items:
        users.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "mobile": user.mobile_number,
            "created_at": user.created_at
        })

    return jsonify({
        "total": paginated.total,
        "page": paginated.page,
        "pages": paginated.pages,
        "data": users
    })