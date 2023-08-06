from pydantic import BaseModel, Field, EmailStr
import os

class Settings(BaseModel):
    authjwt_secret_key: str = os.getenv("SECRET")


class PostSchema(BaseModel):
    id : int = Field(default=None)
    title : str = Field(default=None)
    content : str = Field(default=None)
    class Config:
        schema_extra = {
            "post_demo": {
                "title": "some title about animal",
                "content": "some content about animal"
            }
        }


class User(BaseModel):
    fullname : str = Field(default=None)
    email : EmailStr = Field(default=None)
    password: str = Field(default=None)
    class Config:
        the_schema = {
            "user_demo": {
                "name": "qwertyu",
                "email": "qwertyu@yuio.com",
                "password": "123456"
            }
        }

class UserSchema(BaseModel):
    key : str = Field(default=None)
    fullname : str = Field(default=None)
    email : EmailStr = Field(default=None)
    password: str = Field(default=None)
    created_at : str = Field(default=None)
    updated_at : str = Field(default=None)
    class Config:
        the_schema = {
            "user_demo": {
                "name": "qwertyu",
                "email": "qwertyu@yuio.com",
                "password": "123456"
                ""
            }
        }

class UserLoginSchema(BaseModel):
    email : EmailStr = Field(default=None)
    password: str = Field(default=None)
    class Config:
        the_schema = {
            "user_demo": {
                "email": "qwertyu@yuio.com",
                "password": "123456"
            }
        }
    