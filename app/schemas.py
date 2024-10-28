from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class AutoReply(BaseModel):
    post_id: int
    comment_id: int
    reply_content: str
    author: str
    created_at: datetime = Field(default_factory=datetime.now)
    
    
class AutoReplyConfig(BaseModel):
    enabled: bool = True
    delay_seconds: int = 5
    
    
# Example of a user model that includes auto-reply settings
class User(BaseModel):
    username: str
    auto_reply_enabled: bool = False
    reply_delay_seconds: Optional[int] = 5
    