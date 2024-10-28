import asyncio
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.models import Comment
from app.auth import get_current_user, is_auto_reply_enabled, get_reply_delay, fake_users_db
from app.moderation import moderate_content_with_gemini
from app.schemas import AutoReply

router = APIRouter()

# Fake database for comments
fake_comments_db = [
    Comment(id=1, post_id=1, author="user1", content="This is a comment", created_at=datetime(2024, 10, 20)),
    Comment(id=2, post_id=1, author="user2", content="Offensive comment", created_at=datetime(2024, 10, 21), is_blocked=True),
]

# Create a new comment with moderation and auto-reply
@router.post("/", response_model=Comment, status_code=status.HTTP_201_CREATED, operation_id="create_new_comment")
async def create_comment(comment: Comment, current_user: str = Depends(get_current_user)):
    # Check content moderation
    if moderate_content_with_gemini(comment.content):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Comment contains offensive content and cannot be created."
        )

    # Add the comment to the database
    fake_comments_db.append(comment)

    # Check if auto-reply is enabled for the user
    user = fake_users_db.get(current_user.username)
    if is_auto_reply_enabled(user):
        # Launch an asynchronous task for auto-reply
        asyncio.create_task(auto_reply(comment, user))

    return comment

# Function for auto-reply with delay
async def auto_reply(comment: Comment, user):
    delay = get_reply_delay(user)  # Get delay from user settings
    print(f"Auto-reply delay set to {delay} seconds")  # Debugging output
    await asyncio.sleep(delay)  # Simulate the delay
    reply_content = f"Auto-reply to comment '{comment.content}'"  # Generate a relevant reply

    # Create a new reply comment using AutoReply schema
    auto_reply_comment = AutoReply(
        post_id=comment.post_id,
        comment_id=comment.id,
        reply_content=reply_content,
        author="auto-replier",
        created_at=datetime.utcnow()
    )
    
    # Convert AutoReply to Comment before adding to fake_comments_db
    new_comment_id = len(fake_comments_db) + 1
    auto_reply_as_comment = Comment(
        id=new_comment_id,
        post_id=auto_reply_comment.post_id,
        author=auto_reply_comment.author,
        content=auto_reply_comment.reply_content,
        created_at=auto_reply_comment.created_at,
        is_blocked=False
    )
    fake_comments_db.append(auto_reply_as_comment)

# Get all comments (protected route)
@router.get("/", response_model=List[Comment])
def get_comments(current_user: str = Depends(get_current_user)):
    return fake_comments_db

# Get a comment by ID (protected route)
@router.get("/{comment_id}", response_model=Comment)
def get_comment(comment_id: int, current_user: str = Depends(get_current_user)):
    for comment in fake_comments_db:
        if comment.id == comment_id:
            return comment
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Comment not found"
    )

# Delete a comment by ID (protected route)
@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, current_user: str = Depends(get_current_user)):
    global fake_comments_db
    fake_comments_db = [comment for comment in fake_comments_db if comment.id != comment_id]
    