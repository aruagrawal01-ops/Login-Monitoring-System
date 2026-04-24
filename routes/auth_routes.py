from flask import Blueprint, request, jsonify
from services.auth_service import register_user, login_user, send_otp, reset_password
from flask_jwt_extended import jwt_required

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    response, status = register_user(data)

    return jsonify(response), status


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    response, status = login_user(data)

    return jsonify(response), status

@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    response, status = send_otp(data)
    return jsonify(response), status


@auth_bp.route("/reset-password", methods=["POST"])
def reset_password_route():
    data = request.get_json()
    response, status = reset_password(data)
    return jsonify(response), status
