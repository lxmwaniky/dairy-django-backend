from django.db import models

from core.choices import CowBreedChoices
from core.validators import CowBreedValidator


class CowBreed(models.Model):
    """
    CowBreed Model

    Represents the breed of a cow in a Django application.

    Attributes:
    - name (CharField): The name of the cow breed.
        Choices are limited to the values defined in CowBreedChoices.

    """

    name = models.CharField(
        max_length=20,
        choices=CowBreedChoices.choices,
    )

    def save(self, *args, **kwargs):
        CowBreedValidator.validate_breed_name(self.name)
        super().save(*args, **kwargs)
