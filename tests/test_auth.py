from fastapi import status


# Test user registration endpoint
def test_register_user(client):
    user_data = {
        "username": "newuser",
        "role": "employee",
        "password": "newpass",
    }
    response = client.post("/api/v1/register", json=user_data)

    assert response.status_code == status.HTTP_200_OK
    assert "username" in response.json()


# Test login with valid credentials
def test_login_user(client, test_user):
    response = client.post(
        "/api/v1/login",
        json={"username": "testuser_employee", "password": "testpass"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()


# Test login with invalid credentials
def test_login_user_invalid_credentials(client, test_user):
    response = client.post(
        "/api/v1/login",
        json={"username": "invaliduser", "password": "wrongpass"},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid credentials"
