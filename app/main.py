from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import users, comments, posts, analytics

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include user router
app.include_router(users.router, prefix="/users", tags=["users"])

# Include post router
app.include_router(posts.router, prefix="/posts", tags=["posts"])

# Include comment router
app.include_router(comments.router, prefix="/comments", tags=["comments"])

# Include analytics router
app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Post Management API!"}
