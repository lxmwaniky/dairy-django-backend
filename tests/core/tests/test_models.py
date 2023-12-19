import pytest
from django.core.exceptions import ValidationError

from core.choices import CowBreedChoices
from core.models import CowBreed


@pytest.mark.django_db
class TestCowBreedModel:
    def test_save_breed_with_valid_name(self):
        breed = CowBreed.objects.create(name=CowBreedChoices.JERSEY)
        assert breed.name == CowBreedChoices.JERSEY

    def test_create_breed_with_invalid_name(self):
        with pytest.raises(ValidationError) as err:
            CowBreed.objects.create(name="unknown_breed")
        assert err.value.code == 'invalid_cow_breed'

    def test_create_breed_with_duplicate_name(self):
        # Create a breed with a valid name first
        CowBreed.objects.create(name=CowBreedChoices.FRIESIAN)

        # Attempt to create another breed with the same name, should raise ValidationError
        with pytest.raises(ValidationError) as err:
            CowBreed.objects.create(name=CowBreedChoices.FRIESIAN)
        assert err.value.code == 'duplicate_cow_breed'
