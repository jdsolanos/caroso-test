from pydantic import BaseModel

class _PostBase(BaseModel):
	title: str
	detail: str


class PostCreate(_PostBase):
	#email: str
	pass


class Post(_PostBase):
	id: int
	username: str
	date_created: str
	date_last_updated: str


class PostsList(BaseModel):
	id: int
	title: str
	username: str
	date_last_updated: str

class Content(BaseModel):
	detail: str

class PostResult(BaseModel):
	title: str
