import pytest
from django.urls import reverse
from rest_framework import status

from users.models import *


@pytest.mark.django_db
def test_user_flow(client):
    # Register a new user
    register_data = {
        "username": "test@example.com",
        "email": "abc@gmail.com",
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


@pytest.mark.django_db
class TestRoleAssignments:
    """
    Test class for the role assignment API views.

    Ensure that assigning and dismissing roles functions correctly with proper permissions.

    API Endpoints:

    - `POST /users/assign_farm_owner/`
      - Assign the farm owner role to selected users.
      - `Permission`: Only authenticated users with farm owner permission can access this view.

    - `POST /users/assign_farm_manager/`
      - Assign the farm manager role to selected users.
      - `Permission`: Only authenticated users with farm owner permission can access this view.

    - `POST /users/assign_assistant_farm_manager/`
      - Assign the assistant farm manager role to selected users.
      - `Permission`: Only authenticated users with farm owner permission can access this view.

    - `POST /users/assign_team_leader/`
      - Assign the team leader role to selected users.
      - `Permission`: Only authenticated users with farm manager permission can access this view.

    - `POST /users/assign_farm_worker/`
      - Assign the farm worker role to selected users.
      - `Permission`: Only authenticated users with farm manager permission can access this view.

    - `POST /users/dismiss_farm_owner/`
      - Dismiss the farm owner role from selected users.
      - `Permission`: Only authenticated users with farm owner permission can access this view.

    - `POST /users/dismiss_farm_manager/`
      - Dismiss the farm manager role from selected users.
      - `Permission`: Only authenticated users with farm owner permission can access this view.

    - `POST /users/dismiss_assistant_farm_manager/`
      - Dismiss the assistant farm manager role from selected users.
      - `Permission`: Only authenticated users with farm owner permission can access this view.

    - `POST /users/dismiss_team_leader/`
      - Dismiss the team leader role from selected users.
      - `Permission`: Only authenticated users with farm manager permission can access this view.

    - `POST /users/dismiss_farm_worker/`
      - Dismiss the farm worker role from selected users.
      - `Permission`: Only authenticated users with farm manager permission can access this view.

    Test Cases:

    - `test_assign_to_self`
      - Assigning the role to oneself should be restricted.
      - `Expected Response`: 400 Bad Request, "Cannot assign roles to yourself."

    - `test_assign_farm_owner`
      - Assign farm owner role to another user.
      - `Expected Response`: 200 OK

    - `test_assign_farm_manager`
      - Assign farm manager role to another user.
      - `Expected Response`: 200 OK

    - `test_assign_asst_farm_manager`
      - Assign assistant farm manager role to another user.
      - `Expected Response`: 200 OK

    - `test_assign_team_leader`
      - Assign team leader role to another user.
      - `Expected Response`: 200 OK

    - `test_assign_farm_worker`
      - Assign farm worker role to another user.
      - `Expected Response`: 200 OK

    - `test_assign_farm_manager_permission_denied`
      - Attempt to assign farm manager role with insufficient permissions.
      - `Expected Response`: 403 Forbidden

    - `test_assign_assistant_farm_manager_permission_denied`
      - Attempt to assign assistant farm manager role with insufficient permissions.
      - `Expected Response`: 403 Forbidden

    - `test_assign_team_leader_permission_denied`
      - Attempt to assign team leader role with insufficient permissions.
      - `Expected Response`: 403 Forbidden

    - `test_assign_farm_worker_permission_denied`
      - Attempt to assign farm worker role with insufficient permissions.
      - `Expected Response`: 403 Forbidden

    - `test_dismiss_farm_manager`
      - Dismiss farm manager role from another user.
      - `Expected Response`: 200 OK

    - `test_dismiss_asst_farm_manager`
      - Dismiss assistant farm manager role from another user.
      - `Expected Response`: 200 OK

    - `test_dismiss_team_leader`
      - Dismiss team leader role from another user.
      - `Expected Response`: 200 OK

    - `test_dismiss_farm_worker`
      - Dismiss farm worker role from another user.
      - `Expected Response`: 200 OK

    - `test_dismiss_user_not_found`
      - Attempt to dismiss role from a non-existent user.
      - `Expected Response`: 200 OK, "User with ID '99' was not found."

    - `test_dismiss_user_invalid_id`
      - Attempt to dismiss role with an invalid user ID.
      - `Expected Response`: 200 OK, "The ID 'Y' is invalid."
    """

    @pytest.fixture(autouse=True)
    def setup(self, setup_users):
        self.client = setup_users["client"]

        self.farm_owner_token = setup_users["farm_owner_token"]
        self.farm_owner_user_id = setup_users["farm_owner_user_id"]

        self.farm_manager_token = setup_users["farm_manager_token"]
        self.farm_manager_user_id = setup_users["farm_manager_user_id"]

        self.asst_farm_manager_token = setup_users["asst_farm_manager_token"]
        self.asst_farm_manager_user_id = setup_users["asst_farm_manager_user_id"]

        self.team_leader_token = setup_users["team_leader_token"]
        self.team_leader_user_id = setup_users["team_leader_user_id"]

        self.farm_worker_token = setup_users["farm_worker_token"]
        self.farm_worker_user_id = setup_users["farm_worker_user_id"]

    def test_assign_to_self(self):
        user_ids = [self.farm_owner_user_id]
        response = self.client.post(
            reverse("users:users-assign-farm-manager"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data[0] == "Cannot assign roles to yourself."

    def test_assign_farm_owner(self):
        user_ids = [self.farm_manager_user_id]
        response = self.client.post(
            reverse("users:users-assign-farm-owner"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_assign_farm_manager(self):
        user_ids = [self.asst_farm_manager_user_id]
        response = self.client.post(
            reverse("users:users-assign-farm-manager"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_assign_asst_farm_manager(self):
        user_ids = [self.team_leader_user_id]
        response = self.client.post(
            reverse("users:users-assign-assistant-farm-manager"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_assign_team_leader(self):
        user_ids = [self.farm_owner_user_id]
        response = self.client.post(
            reverse("users:users-assign-team-leader"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_assign_farm_worker(self):
        user_ids = [self.team_leader_user_id]
        response = self.client.post(
            reverse("users:users-assign-farm-worker"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_assign_farm_manager_permission_denied(self):
        user_ids = [self.farm_worker_user_id]
        response = self.client.post(
            reverse("users:users-assign-farm-manager"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_assign_assistant_farm_manager_permission_denied(self):
        user_ids = [self.farm_worker_user_id]
        response = self.client.post(
            reverse("users:users-assign-assistant-farm-manager"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_assign_team_leader_permission_denied(self):
        user_ids = [self.farm_worker_user_id]
        response = self.client.post(
            reverse("users:users-assign-team-leader"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_assign_farm_worker_permission_denied(self):
        user_ids = [self.farm_worker_user_id]
        response = self.client.post(
            reverse("users:users-assign-farm-worker"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_dismiss_farm_manager(self):
        user_ids = [self.farm_worker_user_id]
        response = self.client.post(
            reverse("users:users-dismiss-farm-manager"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_dismiss_asst_farm_manager(self):
        user_ids = [self.asst_farm_manager_user_id]
        response = self.client.post(
            reverse("users:users-dismiss-assistant-farm-manager"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_dismiss_team_leader(self):
        user_ids = [self.team_leader_user_id]
        response = self.client.post(
            reverse("users:users-dismiss-team-leader"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_dismiss_farm_worker(self):
        user_ids = [self.farm_worker_user_id]
        response = self.client.post(
            reverse("users:users-dismiss-farm-worker"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_dismiss_user_not_found(self):
        user_ids = ["99"]
        response = self.client.post(
            reverse("users:users-dismiss-farm-manager"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["error"] == "User with ID '99' was not found."

    def test_dismiss_user_invalid_id(self):
        user_ids = ["Y"]
        response = self.client.post(
            reverse("users:users-dismiss-farm-manager"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["invalid"] == "The ID 'Y' is invalid."
