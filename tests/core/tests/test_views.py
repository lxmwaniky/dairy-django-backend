import pytest
from django.urls import reverse
from rest_framework import status

from core.choices import CowBreedChoices
from core.models import CowBreed


@pytest.mark.django_db
class TestCowBreedViewSet:
    @pytest.fixture(autouse=True)
    def setup(self, setup_users):
        self.client = setup_users["client"]
        self.tokens = {
            "farm_owner": setup_users["farm_owner_token"],
            "farm_manager": setup_users["farm_manager_token"],
            "asst_farm_manager": setup_users["asst_farm_manager_token"],
            "team_leader": setup_users["team_leader_token"],
            "farm_worker": setup_users["farm_worker_token"],
        }

    @pytest.mark.parametrize(
        "user_type, expected_status",
        [
            ("farm_owner", status.HTTP_201_CREATED),
            ("farm_manager", status.HTTP_201_CREATED),
            ("asst_farm_manager", status.HTTP_403_FORBIDDEN),
            ("team_leader", status.HTTP_403_FORBIDDEN),
            ("farm_worker", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_create_cow_breed(self, user_type, expected_status):
        """
        Test creating a cow breed with different user types.
        """
        cow_breed_data = {"name": CowBreedChoices.GUERNSEY}
        response = self.client.post(
            reverse("core:cow-breeds-list"),
            cow_breed_data,
            HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}",
        )
        assert response.status_code == expected_status

        if expected_status == status.HTTP_201_CREATED:
            assert CowBreed.objects.filter(name=cow_breed_data["name"]).exists()

    @pytest.mark.parametrize(
        "user_type, expected_status",
        [
            ("farm_owner", status.HTTP_200_OK),
            ("farm_manager", status.HTTP_200_OK),
            ("asst_farm_manager", status.HTTP_200_OK),
            ("farm_worker", status.HTTP_200_OK),
        ],
    )
    def test_retrieve_cow_breeds(self, user_type, expected_status):
        """
        Test retrieving cow breeds with different user types.
        """
        response = self.client.get(
            reverse("core:cow-breeds-list"),
            HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}",
        )
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "user_type, expected_status",
        [
            ("farm_owner", status.HTTP_200_OK),
            ("farm_manager", status.HTTP_200_OK),
            ("asst_farm_manager", status.HTTP_403_FORBIDDEN),
            ("team_leader", status.HTTP_403_FORBIDDEN),
            ("farm_worker", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_update_cow_breed(self, user_type, expected_status):
        """
        Test updating a cow breed with different user types.
        """
        cow_breed = CowBreed.objects.create(name=CowBreedChoices.FRIESIAN)
        url = reverse("core:cow-breeds-detail", kwargs={"pk": cow_breed.id})
        cow_breed_update_data = {"name": CowBreedChoices.AYRSHIRE}
        response = self.client.put(
            url,
            cow_breed_update_data,
            HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}",
        )
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "user_type, expected_status",
        [
            ("farm_owner", status.HTTP_204_NO_CONTENT),
            ("farm_manager", status.HTTP_204_NO_CONTENT),
            ("asst_farm_manager", status.HTTP_403_FORBIDDEN),
            ("team_leader", status.HTTP_403_FORBIDDEN),
            ("farm_worker", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_delete_cow_breed(self, user_type, expected_status):
        """
        Test deleting a cow breed with different user types.
        """
        cow_breed = CowBreed.objects.create(name=CowBreedChoices.FRIESIAN)
        url = reverse("core:cow-breeds-detail", kwargs={"pk": cow_breed.id})
        response = self.client.delete(
            url, HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}"
        )
        assert response.status_code == expected_status

        if expected_status == status.HTTP_204_NO_CONTENT:
            assert not CowBreed.objects.filter(id=cow_breed.id).exists()

    @pytest.mark.parametrize(
        "filter_name, expected_count, status_code",
        [
            (CowBreedChoices.JERSEY, 1, status.HTTP_200_OK),
            ("ey", 2, status.HTTP_200_OK),
            ("nonexistent", 1, status.HTTP_404_NOT_FOUND),
        ],
    )
    def test_filter_cow_breeds_by_name(self, filter_name, expected_count, status_code):
        """
        Test filtering cow breeds by name.
        """
        CowBreed.objects.create(name=CowBreedChoices.JERSEY)
        CowBreed.objects.create(name=CowBreedChoices.GUERNSEY)
        url = reverse("core:cow-breeds-list") + f"?name={filter_name}"

        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Token {self.tokens['farm_owner']}"
        )

        assert response.status_code == status_code
        assert len(response.data) == expected_count

    def test_order_cow_breeds_by_multiple_fields(self):
        """
        Test ordering cow breeds by multiple fields.
        """
        CowBreed.objects.create(name=CowBreedChoices.JERSEY)
        CowBreed.objects.create(name=CowBreedChoices.GUERNSEY)
        CowBreed.objects.create(name=CowBreedChoices.CROSSBREED)
        url = reverse("core:cow-breeds-list") + "?ordering=-name"
        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Token {self.tokens['farm_manager']}"
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3
        assert response.data[0]["name"] == CowBreedChoices.JERSEY
        assert response.data[1]["name"] == CowBreedChoices.GUERNSEY
        assert response.data[2]["name"] == CowBreedChoices.CROSSBREED

    def test_no_results_for_invalid_name(self):
        """
        Test that no results are returned for an invalid cow breed name.
        """
        url = reverse("core:cow-breeds-list") + "?name=nonexistent"
        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Token {self.tokens['farm_worker']}"
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data == {
            "detail": "No cow breed(s) found matching the provided filters."
        }
