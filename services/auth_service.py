from models.user_model import User
from models.login_history_model import LoginHistory
from db import db
import re

from utils.security_utils import hash_password, verify_password
from flask_jwt_extended import create_access_token

from models.otp_model import OTP
from datetime import datetime




# ---------------- REGISTER USER ---------------- #

def register_user(data):
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    mobile = data.get("mobile_number")

    # 🔹 1. All fields required
    if not username or not email or not password or not mobile:
        return {"error": "All fields are required"}, 400

    # 🔹 2. Phone number validation (exactly 10 digits)
    if not re.fullmatch(r"\d{10}", mobile):
        return {"error": "Mobile number must be exactly 10 digits"}, 400

    # 🔹 3. Check if user exists
    existing_user = User.query.filter(
        (User.username == username) |
        (User.email == email) |
        (User.mobile_number == mobile)
    ).first()

    if existing_user:
        return {"error": "User already exists"}, 400

    # 🔹 4. Hash password
    hashed_password = hash_password(password)

    # 🔹 5. Create user
    new_user = User(
        username=username,
        email=email,
        password=hashed_password,
        mobile_number=mobile
    )

    db.session.add(new_user)
    db.session.commit()

    return {"message": "User registered successfully"}, 201


# ---------------- LOGIN USER ---------------- #

def login_user(data):
    username = data.get("username")
    password = data.get("password")

    # Find user
    user = User.query.filter_by(username=username).first()

    if not user:
        return {"error": "User not found"}, 404

    # Check if account is locked
    if user.locked_until:
        from datetime import datetime
        if datetime.utcnow() < user.locked_until:
            return {"error": "Account temporarily locked"}, 403

    # Verify password
    if not verify_password(password, user.password):
        user.failed_attempts += 1

        # Lock account after 5 failed attempts
        if user.failed_attempts >= 5:
            from datetime import datetime, timedelta
            user.locked_until = datetime.utcnow() + timedelta(minutes=15)

        db.session.commit()
        return {"error": "Invalid credentials"}, 401

    # Reset failed attempts on successful login
    user.failed_attempts = 0
    user.locked_until = None
    db.session.commit()

    # ✅ Save login history
    login_entry = LoginHistory(user_id=user.id)
    db.session.add(login_entry)
    db.session.commit()

    # Generate JWT token
    access_token = create_access_token(identity=str(user.id))

    return {
        "message": "Login successful",
        "token": access_token
    }, 200

from models.otp_model import OTP
from datetime import datetime, timedelta
from utils.otp_utils import generate_otp

def send_otp(data):
    username = data.get("username")

    user = User.query.filter_by(username=username).first()
    if not user:
        return {"error": "User not found"}, 404

    # Get latest OTP
    otp_entry = OTP.query.filter_by(username=username)\
        .order_by(OTP.created_at.desc()).first()

    now = datetime.utcnow()

    # 🚫 Check resend cooldown (60 sec)
    if otp_entry and (now - otp_entry.last_sent_at).seconds < 60:
        return {
            "error": "Please wait before requesting OTP again"
        }, 429

    # 🚫 Max resend limit (3 in 10 minutes)
    if otp_entry:
        if otp_entry.resend_count >= 3 and (now - otp_entry.created_at).seconds < 600:
            return {
                "error": "Too many OTP requests. Try again later"
            }, 429

    # Generate OTP
    otp_code = generate_otp()

    new_entry = OTP(
        username=username,
        otp=otp_code,
        expires_at=now + timedelta(minutes=5),
        resend_count=(otp_entry.resend_count + 1) if otp_entry else 1,
        last_sent_at=now
    )

    db.session.add(new_entry)
    db.session.commit()

    return {
        "message": "OTP sent successfully",
        "otp": otp_code  # remove later in production
    }, 200


def reset_password(data):
    username = data.get("username")
    otp_input = data.get("otp")
    new_password = data.get("new_password")

    # 1️⃣ Check user exists
    user = User.query.filter_by(username=username).first()
    if not user:
        return {"error": "User not found"}, 404

    # 2️⃣ Get latest OTP
    otp_entry = OTP.query.filter_by(username=username, is_used=False)\
        .order_by(OTP.created_at.desc()).first()

    if not otp_entry:
        return {"error": "No OTP found"}, 404

    # 3️⃣ Check expiry
    if datetime.utcnow() > otp_entry.expires_at:
        return {"error": "OTP expired"}, 400

    # 4️⃣ Check attempts
    if otp_entry.attempts >= 5:
        otp_entry.is_used = True
        db.session.commit()
        return {"error": "Too many attempts. Request new OTP"}, 429

    # 5️⃣ Verify OTP
    if otp_entry.otp != otp_input:
        otp_entry.attempts += 1
        db.session.commit()

        return {
            "error": "Invalid OTP",
            "remaining_attempts": 5 - otp_entry.attempts
        }, 400

    # 6️⃣ OTP correct → reset password
    user.password = hash_password(new_password)

    # 7️⃣ Mark OTP as used
    otp_entry.is_used = True

    db.session.commit()

    return {"message": "Password reset successful"}, 200
