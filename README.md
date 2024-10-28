# Posts Comments API

## Description
This API allows users to manage posts and comments with AI moderation and automated responses. It is developed using FastAPI and Pydantic.

## Requirements
- Python 3.12
- Poetry
- requests

## Setup
1. **Initialize the project:**
   - Navigate to the directory where you want to create the project.
   mkdir posts_comments_api
   cd posts_comments_api

2. Install dependencies:
```poetry install```

3. Add the requests library:

```poetry add requests```

4. Run the application:
```poetry run uvicorn app.main:app --reload```

5. Access the API documentation:
    Swagger UI: http://localhost:8000/docs
    OpenAPI JSON: http://localhost:8000/openapi.json

### Add an example of setting an API key to the environment variables:

    Add the following environment variables to set up your Gemini API key

        - **API_KEY** Your Gemini API key for content moderation.

## Install additional dependencies: 
Ensure you have installed python-multipart and a compatible version of bcrypt:
```poetry add python-multipart bcrypt==4.0.1```

### Features Implemented
    1. User Registration &  JWT-based Login:
        - Users can register and log in using JWT tokens.

        - Endpoints:
            - /users/register - Register a new user.
            - /users/token - Log in and receive an access token.

        - Tokens are generated with JWT and require Authorization: Bearer <token> in the request headers for accessing protected routes.


    2. Post Management:

        - Users can create, read, and delete posts.
        - Endpoints:
            /posts/ - Get all posts or create a new post (requires JWT).
            /posts/{post_id} - Get or delete a post by ID (requires JWT).

    3. Comment Management:

        - Users can create, read, and delete comments.
        - Endpoints:
            /comments/ - Get all comments or create a new comment (requires JWT).
            /comments/{comment_id} - Get or delete a comment by ID (requires JWT).
    
    4. Content Moderation:

        - Posts and comments are checked for offensive words during creation. If offensive content is detected, the request is blocked.
        - **Gemini API integration**: The API uses Gemini's content moderation service to detect offensive words and phrases in posts and comments. If the content is flagged as offensive, it will not be created.


    5. Automated Reply to Comments:

        - Users can configure automated replies to comments on their posts with a delay.
        - Endpoint:
            - PUT /users/update_auto_reply_config - Update auto-reply settings (requires JWT).
            - Request body: {"enabled": bool, "delay_seconds": int}
    6. Analytics for Comments:

        - Get a breakdown of comments created over a specified date range.
        - Endpoint:
            - GET /analytics/comments_daily_breakdown - Provides daily breakdown of created and blocked comments.
            - Query parameters: date_from, date_to (in YYYY-MM-DD format).


## Dependencies Used:

        - fastapi for API development.
        - pydantic for data validation.
        - python-jose for JWT authentication.
        - passlib for password hashing.


### Endpoints
    1. User Endpoints

        - Register a new user:
            - POST /users/register: Register a new user.
            - Request body: {"username": "string", "password": "string"}

        - Obtain an access token:
            - POST /users/token: Obtain an access token.
            - Form data: username, password

        - Update auto-reply configuration:
            - PUT /users/update_auto_reply_config
            - Request body: {"enabled": bool, "delay_seconds": int}

    2. Post Endpoints

        - Create a new post:
            - POST /posts/
            - Requires JWT authentication.
            - Request body: {"title": "string", "content": "string", "author": "string"}

        - Get all posts:
            - GET /posts/
            - Requires JWT authentication

    3. Comment Endpoints

        - Create a new comment:
            - POST /comments/
            - Requires JWT authentication.
            - Request body: {"post_id": int, "content": "string", "author": "string"}

        - Get all comments:
            - GET /comments/: Get all comments.
            - Requires JWT authentication.

    4. Analytics Endpoints

        - Get daily comment breakdown:
            - GET /analytics/comments_daily_breakdown
            - Query parameters: date_from, date_to (in YYYY-MM-DD format).

### Running Tests
To run the test suite, use:
```pytest```

### Additional Information
    This API uses a fake in-memory database for demonstration purposes. In a production setup, it should be replaced with a real database (e.g., SQL, NoSQL).
    
    Content moderation checks for predefined offensive words. For real-world use, integrating an AI-based API for moderation is recommended.
    
    Automated replies to comments are configured per user and triggered with a delay set by the user.