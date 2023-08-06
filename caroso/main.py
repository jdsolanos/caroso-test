# from fastapi import FastAPI, Body, Depends, Header, HTTPException
# from fastapi.responses import JSONResponse
# from app_base.models.model import PostSchema, User, UserLoginSchema,UserSchema, Settings

# from fastapi_jwt_auth import AuthJWT
# from fastapi_jwt_auth.exceptions import AuthJWTException
# #from app_base.auth.jwt_bearer import JWTBearer
# #from app_base.auth.jwt_handler import signJWT, validate_token

# from typing import Dict, List
# from datetime import datetime
# from deta import Deta
# from dotenv import load_dotenv
# import traceback
# import json
# from pprint import pprint

# deta = Deta()
# posts = deta.Base("posts-crud")
# users = deta.Base("users-crud")

# load_dotenv()

# app = FastAPI()

# @AuthJWT.load_config
# def get_config():
#     return Settings()

# @app.post("/user/signup", tags=["users"])
# def user_signup(user: User = Body(default=None)):
#     user_dict = user.dict()
#     user_dict["key"] = user_dict["email"]
#     user_dict["created_at"] = str(datetime.now())
#     user_dict["updated_at"] = str(datetime.now())
#     try:
#         users.insert(user_dict) 
#         return "usuario creado exitosamente"
#     except:
#         return "ya existe una cuenta con este correo"

# def check_user(data:UserLoginSchema):
#     user = users.get(data.email)
#     if not user:
#         return False        
#     true_credentials = user["email"]==data.email and user["password"]==data.password
#     if true_credentials:
#         return True
#     return False

# @app.post("/user/login", tags=["users"])
# def user_login(user: UserLoginSchema = Body(default=None), Authorize: AuthJWT = Depends()):
#     if not check_user(user):
#         raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectas")
#     access_token = Authorize.create_access_token(subject=user.email)
#     refresh_token = Authorize.create_refresh_token(subject=user.email)
#     return {"access_token": access_token, "refresh_token": refresh_token}

# @app.post('/refresh')
# def refresh(Authorize: AuthJWT = Depends()):
#     """
#     Refresh token endpoint. This will generate a new access token from
#     the refresh token, but will mark that access token as non-fresh,
#     as we do not actually verify a password in this endpoint.
#     """
#     Authorize.jwt_refresh_token_required()

#     current_user = Authorize.get_jwt_subject()
#     print(current_user)
#     new_access_token = Authorize.create_access_token(subject=current_user,fresh=False)
#     return {"access_token": new_access_token}
# # @app.post("/posts", dependencies=[Depends(JWTBearer())], tags=["posts"])
# # def create_post(post: PostSchema):
# #     print("im here")
# #     response = posts.put(post.dict()) 
# #     # response = "ouch"
# #     # try:
# #     #     response = users.fetch()._items
# #     # except Exception as e:
# #     #     traceback.print_exc()
# #     #     print("miau, asi es", e)
# #     return response

# @app.get("/posts", tags=["posts"])
# def get_all_posts():
#     response = posts.fetch()._items
#     print("jeje")
#     return response

# @app.get("/posts/{uid}", tags=["posts"])
# def get_post(uid: str):
#     post = posts.get(uid)
#     if post:
#         return post
#     response = JSONResponse({"message":"user_not_found"},status_code=404)
#     return response

# @app.put("/posts/{uid}", tags=["posts"])
# def update_post(uid: str, post: PostSchema):
#     post_dict = post.dict()
#     post_dict["key"] = uid
#     response = posts.put(post_dict)
#     return response

# @app.delete("/posts/{uid}", tags=["posts"])
# def delete_post(uid: str):
#     posts.delete(uid)
#     return {}

from fastapi import FastAPI
from deta import Deta

import app_base.routers.users as _users
import app_base.routers.posts as _posts
#deta = Deta()
#posts = deta.Base("posts-crud")
#users = deta.Base("users-crud")

app = FastAPI()


app.include_router(_users.router, tags=["User"])
app.include_router(_posts.router, tags=["Post"])

