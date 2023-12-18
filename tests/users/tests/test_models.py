import pytest

from rest_framework.exceptions import ValidationError
from users.choices import *
from users.models import CustomUser,CowBreed
from users.serializers import *
from users.validators import CustomCowBreedValidator



class TestUserCreation:
    @pytest.mark.django_db
    def test_create_user(self):
        serializer = CustomUserCreateSerializer(
            data={
                "username": "testuser",
                "email": "abc@gmail.com",
                "first_name": "John",
                "last_name": "Doe",
                "phone_number": "+254712345673",
                "sex": SexChoices.MALE,
                "password": "testpassword",
            }
        )
        if serializer.is_valid():
            user = serializer.save()

            assert user.username == "testuser"
            assert user.first_name == "John"
            assert user.last_name == "Doe"
            assert user.phone_number == "+254712345673"
            assert user.sex == SexChoices.MALE
            assert user.check_password("testpassword")
            assert not user.is_staff
            assert not user.is_superuser
            assert user.is_active
        else:
            print(serializer.errors)

    @pytest.mark.django_db
    def test_create_superuser(self):
        superuser = CustomUser.objects.create_superuser(
            username="admin",
            email="abc@gmail.com",
            first_name="Admin",
            last_name="User",
            phone_number="+254712345678",
            sex=SexChoices.FEMALE,
            password="adminpassword",
        )
        assert superuser.username == "admin"
        assert superuser.first_name == "Admin"
        assert superuser.last_name == "User"
        assert superuser.phone_number == "+254712345678"
        assert superuser.sex == SexChoices.FEMALE
        assert superuser.check_password("adminpassword")
        assert superuser.is_staff
        assert superuser.is_superuser
        assert superuser.is_active

@pytest.mark.django_db
class TestCowBreedModel:
    def test_create_breed_with_valid_name(self):
        # Test creating a CowBreed instance with a valid breed name
        breed = CowBreed.objects.create(breed_name=BreedChoices.JERSEY)
        assert breed.breed_name == BreedChoices.JERSEY

    def test_create_breed_with_invalid_name(self):
        # Test creating a CowBreed instance with an invalid breed name
        with pytest.raises(ValidationError, match="Invalid value for breed name"):
            CowBreed.objects.create(breed_name="InvalidBreed")

    def test_create_breed_with_empty_name(self):
        # Test creating a CowBreed instance with an empty breed name
        with pytest.raises(ValidationError, match="Breed name field cannot be empty"):
            CowBreed.objects.create(breed_name="")

    def test_save_breed_with_valid_name(self):
        # Test saving a CowBreed instance with a valid breed name
        breed = CowBreed(breed_name=BreedChoices.JERSEY)
        breed.save()
        assert breed.breed_name == BreedChoices.JERSEY

    def test_save_breed_with_invalid_name(self):
        # Test saving a CowBreed instance with an invalid breed name
        breed = CowBreed(breed_name="InvalidBreed")
        with pytest.raises(ValidationError, match="Invalid value for breed name"):
            breed.save()

    def test_save_breed_with_empty_name(self):
        # Test saving a CowBreed instance with an empty breed name
        breed = CowBreed(breed_name="")
        with pytest.raises(ValidationError, match="Breed name field cannot be empty"):
            breed.save()
