from typing import List
from fastapi import APIRouter, Depends, HTTPException

import app_base.database.connection as _database
import app_base.services.posts as _posts
import app_base.services.users as _users
import app_base.schemas.posts as _schemas
import app_base.auth.authenticate as _auth
from deta import Deta

auth_handler = _auth.AuthHandler()

conn_db = _database.db_conn

posts_db: Deta = conn_db.Base("posts-crud")

router = APIRouter()

@router.get("/posts")
def read_posts(start: int = 0, limit: int = 10, username = Depends(auth_handler.auth_access_wrapper)):
	db_posts = _posts.get_posts(db=posts_db, start=start, limit=limit)
	return db_posts


@router.post("/posts", status_code=201, response_model=_schemas.PostResult)
def create_post(post: _schemas.PostCreate, username=Depends(auth_handler.auth_access_wrapper)):
#	db_user = _users.get_user_by_username(db=db, username=username)
#	if db_user is None:
#		raise HTTPException(status_code=401, detail="Unauthorized")
	return _posts.create_post(db=posts_db, post=post, username=username)


@router.get("/posts/my_post", response_model=List[_schemas.PostsList])
def get_my_post(limit: int = 10, username=Depends(auth_handler.auth_access_wrapper)):
	db_posts = _posts.get_my_posts(db=posts_db, limit=limit, username=username)
	return db_posts

@router.get("/posts/{post_id}", response_model=_schemas.Content)
def get_post(post_id: int, username=Depends(auth_handler.auth_access_wrapper)):
	db_post = _posts.get_detail(db=posts_db, post_id=post_id)
	if db_post is None:
		raise HTTPException(status_code=404, detail="This post does not exist")
	return db_post


@router.delete("/posts/{post_id}")
def delete_post(post_id: int, username=Depends(auth_handler.auth_access_wrapper)):
	db_post = _posts.get_post(db=posts_db, post_id=post_id)
	if db_post is None:
		raise HTTPException(status_code=404, detail="This post does not exist") 
	if db_post.username != username:
		raise HTTPException(status_code=401, detail="Unauthorized")
	_posts.delete_post(db=posts_db, post_id=post_id)
	return {"message" : f"successfully deleted post with id: {post_id}"}


@router.put("/posts/{post_id}", response_model=_schemas.Post)
def update_post(post_id: int, post: _schemas.PostCreate, username=Depends(auth_handler.auth_access_wrapper)):
	db_post = _posts.get_post(db=posts_db, post_id=post_id)
	if db_post is None:
		raise HTTPException(status_code=404, detail="This post does not exist") 
	if db_post.username != username:
		raise HTTPException(status_code=401, detail="Unauthorized")
	return _posts.update_post(db=posts_db, post_id=post_id, post=post)