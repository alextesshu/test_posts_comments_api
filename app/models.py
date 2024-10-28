from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Post model
class Post(BaseModel):
    id: int
    title: str
    content: str
    author: str
    created_at: datetime = datetime.now()
    comments: List[int] = []  # List of comment IDs

# Comment model
class Comment(BaseModel):
    id: int
    post_id: int
    author: str
    content: str
    created_at: datetime = datetime.now()
    is_blocked: bool = False  # Flag for blocked comments
