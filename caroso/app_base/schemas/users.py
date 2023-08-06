from pydantic import BaseModel, Field, EmailStr

class UserLogin(BaseModel):
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

class UserCreate(BaseModel):
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


class User(UserCreate):
	key: str
	is_active: bool


class UpdateToken(BaseModel):
    access_token: str = None


class LoginToken(BaseModel):
	access_token: str = None
	refresh_token: str = None