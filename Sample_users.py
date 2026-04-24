from app import create_app
from db import db
from models.user_model import User
from utils.security_utils import hash_password
from datetime import datetime, timedelta
import random

app = create_app()

names = [
    "arush","rahul","rohit","amit","vikas","sneha","priya","neha","anita","kiran",
    "john","mike","david","alex","sam","emma","olivia","ava","mia","lily",
    "noah","liam","logan","james","lucas","sophia","isabella","charlotte","amelia","harper",
    "ethan","daniel","jack","ryan","leo","grace","ella","zoe","hannah","nora",
    "aarav","vivaan","aditya","krishna","arjun","isha","diya","meera","anaya","kavya"
]

with app.app_context():
    for i in range(50):
        username = names[i] + str(i)
        user = User(
            username=username,
            email=f"{username}@mail.com",
            password=hash_password("123456"),
            mobile_number=f"99999{i:05}",
            created_at=datetime.utcnow() - timedelta(days=random.randint(0, 365))
        )
        db.session.add(user)

    db.session.commit()

print("50 users inserted successfully!")