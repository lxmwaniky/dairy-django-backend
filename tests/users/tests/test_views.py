import pytest
from django.urls import reverse
from rest_framework import status

from users.choices import SexChoices


@pytest.mark.django_db
def test_user_flow(client):
    """
    Test the complete user flow including registration, login, access, logout, and unauthorized access attempts.

    Test Steps:
    - Register a new user and ensure a successful creation.
    - Attempt to access user details without authentication and verify the expected unauthorized response.
    - Log in with valid credentials and obtain the authentication token.
    - Access user details with authentication and verify a successful response.
    - Log out and ensure a successful logout with no content returned.
    - Attempt to access user details after logout and verify the expected unauthorized response.

    """

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
    Test suite for the role assignment API views.

    This suite covers the functionality of assigning and dismissing roles via API endpoints, ensuring proper permissions
    are enforced. It utilizes pytest fixtures for setup and parameterized tests to efficiently cover multiple scenarios.

    Fixtures:
    - `setup_users`: Provides essential setup including client instances and user tokens.

    Test Cases:
    - `test_assign_roles`: Parameterized test covering various scenarios of role assignment.
    - `test_dismiss_roles`: Parameterized test covering various scenarios of role dismissal.

    API Endpoints:
    - Endpoints for assigning roles:
      - `/users-assign-farm-owner/`
      - `/users-assign-farm-manager/`
      - `/users-assign-assistant-farm-manager/`
      - `/users-assign-team-leader/`
      - `/users-assign-farm-worker/`

    - Endpoints for dismissing roles:
      - `/users-dismiss-farm-manager/`
      - `/users-dismiss-assistant-farm-manager/`
      - `/users-dismiss-team-leader/`
      - `/users-dismiss-farm-worker/`

    Test Cases Summary:
    - `test_assign_roles`: Covers scenarios of assigning roles, validating expected responses and permissions.
    - `test_dismiss_roles`: Covers scenarios of dismissing roles, validating expected responses and permissions.

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

    @pytest.mark.parametrize("assign_endpoint, user_id, token, expected_status", [
        ("users-assign-farm-owner", "farm_manager_user_id", "farm_owner_token", status.HTTP_200_OK),
        ("users-assign-farm-manager", "asst_farm_manager_user_id", "farm_owner_token", status.HTTP_200_OK),
        ("users-assign-assistant-farm-manager", "team_leader_user_id", "farm_owner_token", status.HTTP_200_OK),
        ("users-assign-team-leader", "farm_worker_user_id", "farm_manager_token", status.HTTP_200_OK),
        ("users-assign-farm-worker", "farm_worker_user_id", "farm_manager_token", status.HTTP_200_OK),
        ("users-assign-farm-manager", "farm_worker_user_id", "farm_manager_token", status.HTTP_403_FORBIDDEN),
        ("users-assign-assistant-farm-manager", "farm_worker_user_id", "farm_manager_token",
         status.HTTP_403_FORBIDDEN),
        ("users-assign-team-leader", "farm_worker_user_id", "farm_worker_token", status.HTTP_403_FORBIDDEN),
        ("users-assign-farm-worker", "farm_worker_user_id", "asst_farm_manager_token", status.HTTP_403_FORBIDDEN
         ),
    ])
    def test_assign_roles(self, assign_endpoint, user_id, token, expected_status):
        """
        Parameterized test for role assignment scenarios.

        Args:
        - `assign_endpoint`: Endpoint for assigning roles.
        - `user_id`: Attribute representing the user to assign roles to.
        - `token`: Attribute representing the authentication token for the user performing the assignment.
        - `expected_status`: Expected HTTP status code for the response.

        Test Steps:
        - Perform a POST request to the specified assignment endpoint.
        - Validate the HTTP status code against the expected status.

        """
        user_ids = [getattr(self, user_id)]
        response = self.client.post(
            reverse(f"users:{assign_endpoint}"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {getattr(self, token)}",
        )
        assert response.status_code == expected_status

    @pytest.mark.parametrize("dismiss_endpoint, user_id, token, expected_status", [
        ("users-dismiss-farm-manager", "farm_manager_user_id", "farm_owner_token", status.HTTP_200_OK),
        ("users-dismiss-assistant-farm-manager", "asst_farm_manager_user_id", "farm_owner_token", status.HTTP_200_OK),
        ("users-dismiss-team-leader", "team_leader_user_id", "farm_manager_token", status.HTTP_200_OK),
        ("users-dismiss-farm-worker", "farm_worker_user_id", "farm_manager_token", status.HTTP_200_OK),
        ("users-dismiss-farm-manager", "farm_manager_user_id", "farm_manager_token", status.HTTP_403_FORBIDDEN),
        ("users-dismiss-assistant-farm-manager", "asst_farm_manager_user_id", "farm_manager_token",
         status.HTTP_403_FORBIDDEN),
        ("users-dismiss-team-leader", "team_leader_user_id", "farm_worker_token", status.HTTP_403_FORBIDDEN),
        ("users-dismiss-farm-worker", "farm_worker_user_id", "asst_farm_manager_token", status.HTTP_403_FORBIDDEN
         ),
    ])
    def test_dismiss_roles(self, dismiss_endpoint, user_id, token, expected_status):
        """
        Parameterized test for role dismissal scenarios.

        Args:
        - `dismiss_endpoint`: Endpoint for dismissing roles.
        - `user_id`: Attribute representing the user to dismiss roles from.
        - `token`: Attribute representing the authentication token for the user performing the dismissal.
        - `expected_status`: Expected HTTP status code for the response.

        Test Steps:
        - Perform a POST request to the specified dismissal endpoint.
        - Validate the HTTP status code against the expected status.

        """
        user_ids = [getattr(self, user_id)]
        response = self.client.post(
            reverse(f"users:{dismiss_endpoint}"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {getattr(self, token)}",
        )
        assert response.status_code == expected_status
