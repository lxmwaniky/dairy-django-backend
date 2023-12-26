from datetime import timedelta

import pytest
from django.urls import reverse
from rest_framework import status

from core.utils import todays_date
from reproduction.choices import PregnancyStatusChoices
from reproduction.models import Pregnancy
from reproduction.serializers import PregnancySerializer


@pytest.mark.django_db
class TestPregnancyViewSet:
    @pytest.fixture(autouse=True)
    def setup(self, setup_users, setup_pregnancy_data):
        self.client = setup_users["client"]
        self.tokens = {
            "farm_owner": setup_users["farm_owner_token"],
            "farm_manager": setup_users["farm_manager_token"],
            "asst_farm_manager": setup_users["asst_farm_manager_token"],
            "team_leader": setup_users["team_leader_token"],
            "farm_worker": setup_users["farm_worker_token"],
        }

        self.pregnancy_data = setup_pregnancy_data

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
    def test_add_pregnancy(self, user_type, expected_status):
        response = self.client.post(
            reverse("reproduction:pregnancy-records-list"),
            data=self.pregnancy_data,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}",
        )

        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "user_type, expected_status",
        [
            ("farm_owner", status.HTTP_200_OK),
            ("farm_manager", status.HTTP_200_OK),
            ("asst_farm_manager", status.HTTP_200_OK),
            ("farm_worker", status.HTTP_200_OK),
        ],
    )
    def test_retrieve_pregnancy(self, user_type, expected_status):
        response = self.client.get(
            reverse("reproduction:pregnancy-records-list"),
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}",
        )
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize(
        "user_type, expected_status",
        [
            ("farm_owner", status.HTTP_200_OK),
            ("farm_manager", status.HTTP_200_OK),
            ("asst_farm_manager", status.HTTP_403_FORBIDDEN),
            ("farm_worker", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_update_pregnancy(self, user_type, expected_status):
        serializer = PregnancySerializer(data=self.pregnancy_data)
        assert serializer.is_valid()
        pregnancy = serializer.save()
        update_data = {
            "pregnancy_status": PregnancyStatusChoices.FAILED,
            "pregnancy_notes": "Updated pregnancy status as failed",
            "pregnancy_failed_date": todays_date - timedelta(days=100),
        }
        response = self.client.patch(
            reverse("reproduction:pregnancy-records-detail", kwargs={"pk": pregnancy.id}),
            data=update_data,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}",
        )
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "user_type, expected_status",
        [
            ("farm_owner", status.HTTP_204_NO_CONTENT),
            ("farm_manager", status.HTTP_204_NO_CONTENT),
            ("asst_farm_manager", status.HTTP_403_FORBIDDEN),
            ("farm_worker", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_delete_pregnancy(self, user_type, expected_status):
        serializer = PregnancySerializer(data=self.pregnancy_data)
        assert serializer.is_valid()
        pregnancy = serializer.save()
        response = self.client.delete(
            reverse("reproduction:pregnancy-records-detail", kwargs={"pk": pregnancy.id}),
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}",
        )
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "filter_field, filter_value, expected_count, status_code",
        [
            ("cow", "General", 1, status.HTTP_200_OK),
            ("year", "2022", 1, status.HTTP_404_NOT_FOUND),
            ("month", "4", 1, status.HTTP_200_OK),
            ("pregnancy_outcome", "", 1, status.HTTP_200_OK),
            ("pregnancy_status", "pregnant", 1, status.HTTP_404_NOT_FOUND),
        ],
    )
    def test_filter_pregnancy_by_field(
            self, filter_field, filter_value, expected_count, status_code
    ):
        serializer = PregnancySerializer(data=self.pregnancy_data)
        assert serializer.is_valid()
        serializer.save()

        url = reverse("reproduction:pregnancy-records-list") + f"?{filter_field}={filter_value}"

        response = self.client.get(
            url,
            HTTP_AUTHORIZATION=f"Token {self.tokens['farm_manager']}"
        )

        assert response.status_code == status_code
        assert len(response.data) == expected_count
