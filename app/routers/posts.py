from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.models import Post
from app.auth import get_current_user
from app.moderation import moderate_content_with_gemini

router = APIRouter()

# Fake database for posts
fake_posts_db = []

# Create a new post with content moderation
@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED, operation_id="create_new_post")
def create_post(post: Post, current_user: str = Depends(get_current_user)):
    post.id = len(fake_posts_db) + 1
    if moderate_content_with_gemini(post.content):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post contains offensive content and cannot be created."
        )
    fake_posts_db.append(post)
    return post

# Get all posts (protected route)
@router.get("/", response_model=List[Post])
def get_posts(current_user: str = Depends(get_current_user)):
    return fake_posts_db


# Get a post by ID (protected route)
@router.get("/{post_id}", response_model=Post)
def get_post(post_id: int, current_user: str = Depends(get_current_user)):
    for post in fake_posts_db:
        if post.id == post_id:
            return post
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Post not found"
    )

# Delete a post by ID (protected route)
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, current_user: str = Depends(get_current_user)):
    global fake_posts_db
    fake_posts_db = [post for post in fake_posts_db if post.id != post_id]
    

