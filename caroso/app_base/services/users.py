import app_base.models.users as _models
import app_base.schemas.users as _schemas
from typing import Dict, List

def get_user_by_username(db, username: str):
    return db.get(username)


def create_user(db, user: _schemas.UserCreate):
    db_user = _models.User()
    db_user.key = user.email
    db_user.email = user.email
    db_user.fullname = user.fullname
    db_user.hashed_password = user.password
    user_dict = db_user.dict()
    return db.insert(user_dict)


def get_users(db, skip: int, limit: int):
	return db.query(_models.User).offset(skip).limit(limit).all()


def get_user(db, user_id: int):
	return db.query(_models.User).filter(_models.User.id == user_id).first()