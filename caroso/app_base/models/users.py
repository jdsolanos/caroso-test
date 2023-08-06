from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    key : str = Field(default=None)
    fullname : str = Field(default=None)
    email : EmailStr = Field(default=None)
    hashed_password: str = Field(default=None)
    is_active = Field(default=True)
    class Config:
        the_schema = {
            "user_demo": {
                "name": "qwertyu",
                "email": "qwertyu@yuio.com",
                "password": "123456"
                ""
            }
        }
        