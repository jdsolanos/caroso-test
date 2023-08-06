from typing import List
from fastapi import APIRouter, Depends, HTTPException

import app_base.database.connection as _database
import app_base.services.users as _users
import app_base.schemas.users as _schemas
import app_base.auth.authenticate as _auth

auth_handler = _auth.AuthHandler()

conn_db = _database.db_conn

users_db = conn_db.Base("users-crud")

router = APIRouter()


@router.post("/signup", status_code=201, response_model=_schemas.User)
def create_user(user: _schemas.UserCreate):
	db_user = _users.get_user_by_username(db=users_db, username=user.email)
	if db_user:
		raise HTTPException(status_code=400, detail="The E-Mail is already used")

	user.password = auth_handler.get_password_hash(user.password)
	
	#cambiar respuesta por algo que no nos deje una vulnerabilidad de seguridad xd
	return _users.create_user(db=users_db, user=user)

@router.post("/login", response_model=_schemas.LoginToken)
def login_user(user: _schemas.UserLogin):
	db_user = _users.get_user_by_username(db=users_db, username=user.email)
	if db_user is None:
		raise HTTPException(status_code=401, detail="The E-Mail does not exist")
	is_verified = auth_handler.verify_password(user.password, db_user["hashed_password"])
	if not is_verified:
		raise HTTPException(status_code=401, detail="Password does not matched")
	return auth_handler.encode_login_token(user.email)


@router.get("/update_token", response_model=_schemas.UpdateToken)
def update_token(username=Depends(auth_handler.auth_refresh_wrapper)):
	if username is None:
		raise HTTPException(status_code=401, detail="not authorization")
	return auth_handler.encode_update_token(username)