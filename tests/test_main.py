import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.auth import fake_users_db

client = TestClient(app)

# Test user registration and login
def test_user_registration_and_login():
    # Clear the fake user database before the test
    fake_users_db.clear()
    
    # Register a new user
    response = client.post(
        "/users/register",
        json={"username": "testuser", "password": "testpassword"}  # Use 'data' instead of 'json' for form data
    )
    print("Response:", response.json())
    assert response.status_code == 201  # Ensure that the registration was successful
    
    # Obtain an access token for the registered user
    response = client.post(
        "/users/token",
        data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200  # Ensure that login was successful
    assert "access_token" in response.json()  # Check if the response contains an access token


# Test creating a post without moderation
def test_create_post_without_moderation():
    response = client.post(
        "/users/token",
        data={"username": "testuser", "password": "testpassword"}
    )
    token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(
        "/posts/",
        json={
            "id": 1,
            "title": "Clean Title",
            "content": "This is a clean post",
            "author": "testuser"
        },
        headers=headers
    )
    assert response.status_code == 201
    assert response.json()["content"] == "This is a clean post"
    
    
    # Test creating a comment without moderation
def test_create_comment_without_moderation():
    response = client.post(
        "/users/token",
        data={"username": "testuser", "password": "testpassword"}
    )
    token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(
        "/comments/",
        json={
            "id": 1,
            "post_id": 1,
            "author": "testuser",
            "content": "This is a clean comment"
        },
        headers=headers
    )
    assert response.status_code == 201
    assert response.json()["content"] == "This is a clean comment"
    
    
# Test creating a post with offensive content
def test_create_post_with_moderation():
    response = client.post(
        "/users/token",
        data={"username": "testuser", "password": "testpassword"}
    )
    token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(
        "/posts/",
        json={
            "id": 2,
            "title": "Offensive Title",
            "content": "fuck",  # Offensive word
            "author": "testuser"
        },
        headers=headers
    )
    
    print("Response status code:", response.status_code)
    print("Gemini API Response:", response.json())
    if response.status_code == 400:
        assert response.json()["detail"] == "Post contains offensive content and cannot be created."
    else:
        assert response.status_code == 201



# Test creating a comment with offensive content
def test_create_comment_with_moderation():
    response = client.post(
        "/users/token",
        data={"username": "testuser", "password": "testpassword"}
    )
    token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(
        "/comments/",
        json={
            "id": 2,
            "post_id": 1,
            "author": "testuser",
            "content": "fuck"
        },
        headers=headers
    )
    print("Response status code:", response.status_code)
    print("Gemini API Response:", response.json())
    if response.status_code == 400:
        assert response.json()["detail"] == "Comment contains offensive content and cannot be created."
    else:
        assert response.status_code == 201

# Test getting all posts
def test_get_all_posts():
    response = client.post(
        "/users/token",
        data={"username": "testuser", "password": "testpassword"}
    )
    token = response.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/posts/", headers=headers)
    assert response.status_code == 200
    

# Test analytics for comments
def test_comments_daily_breakdown():
    # Get an access token
    response = client.post(
        "/users/token",
        data={"username": "testuser", "password": "testpassword"}
    )
    token = response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get(
        "/analytics/comments_daily_breakdown?date_from=2024-10-20&date_to=2024-10-21",
        headers=headers
    )
    assert response.status_code == 200  # Ensure that the response is successful


def test_update_auto_reply_config():
    # Register a new user
    client.post(
        "/users/register",
        json={"username": "testuser", "password": "testpassword"}
    )

    # Obtain an access token for the registered user
    response = client.post(
        "/users/token",
        data={"username": "testuser", "password": "testpassword"}
    )
    token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # Update auto-reply settings
    update_response = client.put(
        "/users/update_auto_reply_config",
        json={"enabled": True, "delay_seconds": 10},
        headers=headers
    )

    assert update_response.status_code == 200
    assert update_response.json() == {"message": "Auto-reply configuration updated successfully"}

    # Check if the settings were updated in the fake database
    user = fake_users_db["testuser"]
    assert user["auto_reply_enabled"] is True
    assert user["reply_delay_seconds"] == 10
