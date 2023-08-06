from datetime import datetime

import app_base.models.posts as _models
import app_base.schemas.posts as _schemas
from deta import Deta
def create_post(db: Deta, post: _schemas.PostCreate, username: str):
	db_post = {
		'title': post.title,
		'content': post.detail,
		'username': username	
	}
	return db.insert(db_post)


def get_posts(db: Deta, start: int, limit: int):
	if start == 0:
		return db.fetch(limit=limit)["_items"]
	return db.fetch(limit=limit, last=start)["_items"]
	
def get_my_posts(db: Deta, limit: int, start: int, username: str):
	return db.fetch(query={"username":username},limit=limit,  last= start)


def get_post(db: Deta, post_id: int):
	return db.get(post_id)

def get_detail(db: Deta, post_id: int):
	db_post = db.get(post_id) 
	return db_post["content"]


def delete_post(db: Deta, post_id: int):
	db.delete(post_id)


def update_post(db: Deta, post_id: int, post: _schemas.PostCreate):
	post_update = {
	"title": post.title,
	"content": post.detail
	}
	return db.update(post_update, post_id)