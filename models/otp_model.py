from db import db
from datetime import datetime

class OTP(db.Model):
    __tablename__ = "otp"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), nullable=False)
    otp = db.Column(db.String(6), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)

    attempts = db.Column(db.Integer, default=0)
    is_used = db.Column(db.Boolean, default=False)
    resend_count = db.Column(db.Integer, default=0)
    last_sent_at = db.Column(db.DateTime, default=datetime.utcnow)