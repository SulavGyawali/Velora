from app.models.user_model import User
from app.core.database import get_db
from fastapi import Depends
from requests import Session

def get_user_by_phone(phone: str, db: Session):
    return db.query(User).filter(User.phone == phone).first()

def create_user(username: str, phone: str, password: str, db: Session):
    new_user = User(username=username, phone=phone, password=password, is_verified=False, is_active=True)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_user_verification(phone: str, is_verified: bool, db: Session):
    user = get_user_by_phone(phone, db)
    if user:
        user.is_verified = is_verified
        db.commit()
        db.refresh(user)
    return user

def check_user_verification(phone: str, db: Session):
    user = get_user_by_phone(phone, db)
    return user.is_verified if user else False
