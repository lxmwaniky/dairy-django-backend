import pytest
from django.urls import reverse
from rest_framework import status

from users.models import *


@pytest.mark.django_db
def test_user_flow(client):
    # Register a new user
    register_data = {
        "username": "test@example.com",
        "password": "testpassword",
        "first_name": "Peter",
        "last_name": "Evance",
        "phone_number": "+254712345699",
        "sex": SexChoices.MALE,
    }

    response = client.post("/auth/users/", register_data)
    assert response.status_code == status.HTTP_201_CREATED

    # Access user details (without authentication)
    response = client.get("/auth/users/me", follow=True)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Log in
    login_data = {
        "username": "test@example.com",
        "password": "testpassword",
    }
    response = client.post(reverse("users:login"), login_data)
    assert response.status_code == status.HTTP_200_OK
    token = response.data["auth_token"]

    # Access user details (with authentication)
    response = client.get(
        "/auth/users/me", HTTP_AUTHORIZATION=f"Token {token}", follow=True
    )
    assert response.status_code == status.HTTP_200_OK

    # Log out
    response = client.post(
        reverse("users:logout"),
        HTTP_AUTHORIZATION=f"Token {token}",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Attempt to access user details after logout
    response = client.get(
        "/auth/users/me", HTTP_AUTHORIZATION=f"Token {token}", follow=True
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
