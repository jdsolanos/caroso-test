from pydantic import BaseModel, Field, EmailStr

class Post(BaseModel):
    key : int = Field(default=None)
    title : str = Field(default=None)
    content : str = Field(default=None)
    username : EmailStr = Field(default=None)
    class Config:
        schema_extra = {
            "post_demo": {
                "title": "some title about animal",
                "content": "some content about animal"
            }
        }