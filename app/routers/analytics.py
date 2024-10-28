from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Dict
from datetime import datetime
from app.models import Comment
from app.auth import get_current_user

router = APIRouter()

# Fake database for comments (import from comments.py)
fake_comments_db = [
    Comment(id=1, post_id=1, author="user1", content="This is a comment", created_at=datetime(2024, 10, 20)),
    Comment(id=2, post_id=1, author="user2", content="Offensive comment", created_at=datetime(2024, 10, 21), is_blocked=True),
]

@router.get("/comments_daily_breakdown", response_model=List[Dict[str, str]])
def get_comments_daily_breakdown(date_from: str, date_to: str, current_user: str = Depends(get_current_user)):
    try:
        start_date = datetime.strptime(date_from, "%Y-%m-%d")
        end_date = datetime.strptime(date_to, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Use YYYY-MM-DD."
        )
        
    # Initialize the response dictionary
    breakdown_dict = {}

    # Filter and aggregate comments based on date range
    for comment in fake_comments_db:
        if start_date <= comment.created_at <= end_date:
            date_key = comment.created_at.strftime("%Y-%m-%d")
            if date_key not in breakdown_dict:
                breakdown_dict[date_key] = {"created": 0, "blocked": 0}
            breakdown_dict[date_key]["created"] += 1
            if comment.is_blocked:
                breakdown_dict[date_key]["blocked"] += 1

    # Convert to a list of dictionaries for easier client-side processing
    daily_breakdown = [
        {
            "date": date,
            "created": str(counts["created"]),  # Convert to string
            "blocked": str(counts["blocked"])   # Convert to string
        }
        for date, counts in breakdown_dict.items()
    ]

    return daily_breakdown