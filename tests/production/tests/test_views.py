import pytest
from django.urls import reverse
from rest_framework import status

from production.models import Lactation
from production.serializers import LactationSerializer, MilkSerializer
from reproduction.serializers import PregnancySerializer


@pytest.mark.django_db
class TestLactationViewSet:
    @pytest.fixture(autouse=True)
    def setup(
        self, setup_users, setup_lactation_data, setup_pregnancy_to_lactation_data
    ):
        self.client = setup_users["client"]

        self.tokens = {
            "farm_owner": setup_users["farm_owner_token"],
            "farm_manager": setup_users["farm_manager_token"],
            "asst_farm_manager": setup_users["asst_farm_manager_token"],
            "team_leader": setup_users["team_leader_token"],
            "farm_worker": setup_users["farm_worker_token"],
        }

        self.lactation_data = setup_lactation_data
        self.setup_pregnancy_to_lactation_data = setup_pregnancy_to_lactation_data

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
    def test_add_lactation(self, user_type, expected_status):
        response = self.client.post(
            reverse("production:lactation-records-list"),
            data=self.lactation_data,
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
    def test_retrieve_lactation(self, user_type, expected_status):
        response = self.client.get(
            reverse("production:lactation-records-list"),
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}",
        )
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "user_type",
        [
            "farm_owner",
            "farm_manager",
            "asst_farm_manager",
            "farm_worker",
        ],
    )
    def test_update_lactation(self, user_type):
        serializer = LactationSerializer(data=self.lactation_data)
        assert serializer.is_valid()
        lactation = serializer.save()
        response1 = self.client.patch(
            reverse("production:lactation-records-detail", kwargs={"pk": lactation.id}),
            data=self.lactation_data,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}",
        )

        response2 = self.client.patch(
            reverse("production:lactation-records-detail", kwargs={"pk": lactation.id}),
            data=self.lactation_data,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}",
        )
        assert response1.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert response2.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

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
    def test_delete_lactation(self, user_type, expected_status):
        serializer = LactationSerializer(data=self.lactation_data)
        assert serializer.is_valid()
        lactation = serializer.save()
        response = self.client.delete(
            reverse("production:lactation-records-detail", kwargs={"pk": lactation.id}),
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}",
        )
        assert response.status_code == expected_status

    def test_delete_lactation_with_pregnancy(self):
        serializer = PregnancySerializer(data=self.setup_pregnancy_to_lactation_data)
        assert serializer.is_valid()
        pregnancy = serializer.save()

        lactation = Lactation.objects.get(pregnancy=pregnancy)
        response = self.client.delete(
            reverse("production:lactation-records-detail", kwargs={"pk": lactation.id}),
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.tokens['farm_manager']}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestMilkViewSet:
    @pytest.fixture(autouse=True)
    def setup(self, setup_users, setup_milk_data):
        self.client = setup_users["client"]

        self.tokens = {
            "farm_owner": setup_users["farm_owner_token"],
            "farm_manager": setup_users["farm_manager_token"],
            "asst_farm_manager": setup_users["asst_farm_manager_token"],
            "team_leader": setup_users["team_leader_token"],
            "farm_worker": setup_users["farm_worker_token"],
        }
        self.setup_milk_data = setup_milk_data

    @pytest.mark.parametrize(
        "user_type, expected_status",
        [
            ("farm_owner", status.HTTP_201_CREATED),
            ("farm_manager", status.HTTP_201_CREATED),
            ("asst_farm_manager", status.HTTP_201_CREATED),
            ("farm_worker", status.HTTP_201_CREATED),
        ],
    )
    def test_add_milk(self, user_type, expected_status):
        response = self.client.post(
            path=reverse("production:milk-records-list"),
            data=self.setup_milk_data,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}",
        )

        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "user_type, expected_status",
        [
            ("farm_owner", status.HTTP_200_OK),
            ("farm_manager", status.HTTP_200_OK),
            ("asst_farm_manager", status.HTTP_403_FORBIDDEN),
            ("farm_worker", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_retrieve_milk(self, user_type, expected_status):
        response = self.client.get(
            reverse("production:milk-records-list"),
            HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}",
        )
        assert response.status_code == expected_status

    @pytest.mark.parametrize(
        "user_type, expected_status",
        [
            ("farm_owner", status.HTTP_200_OK),
            ("farm_manager", status.HTTP_200_OK),
            ("asst_farm_manager", status.HTTP_403_FORBIDDEN),
            ("farm_worker", status.HTTP_403_FORBIDDEN),
        ],
    )
    def test_update_milk(self, user_type, expected_status):
        serializer = MilkSerializer(data=self.setup_milk_data)
        serializer.is_valid()
        milk = serializer.save()

        update_record = {"cow": milk.cow.id, "amount_in_kgs": 21}
        response = self.client.patch(
            reverse("production:milk-records-detail", kwargs={"pk": milk.id}),
            data=update_record,
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
    def test_delete_milk(self, user_type, expected_status):
        serializer = MilkSerializer(data=self.setup_milk_data)
        serializer.is_valid()
        milk = serializer.save()

        response = self.client.delete(
            reverse("production:milk-records-detail", kwargs={"pk": milk.id}),
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.tokens[user_type]}",
        )
        assert response.status_code == expected_status
