from django.db import models

from users.choices import SexChoices
from core.choices import CowBreedChoices
from core.validators import CowBreedValidato, CowValidatorr
from datetime import date
import uuid


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

class Cow(models.Model):
    """
    Cow Model

    Represents an individual cow in a Django application.

    Attributes:
    - breed (CharField): The breed of the cow, selected from predefined choices in BreedChoices.
    - tag_number (CharField): Uniquely identifies each cow with a system-generated tag number.
    - parity (PositiveIntegerField): Indicates the parity or number of calvings the cow has undergone.
    - age (PositiveIntegerField): Represents the age of the cow in years.
    - date_of_birth (DateField): Stores the date of birth of the cow.
    - name (CharField): Holds the name assigned to the cow.
    - gender (CharField): Specifies the gender of the cow (e.g., male, female).
    - availability_status (BooleanField): Indicates whether the cow is currently available.
    - current_pregnancy_status (CharField): Tracks the current pregnancy status of the cow.
    - category (CharField): Categorizes the cow (e.g., calf, heifer, milking cow).
    - current_production_status (CharField): Captures the current production status of the cow (e.g., milking, weaning).
    - date_introduced_in_farm (DateField): Records the date the cow was introduced to the farm.
    - is_bought (BooleanField): Indicates whether the cow was purchased.
    - date_of_death (DateField, Nullable): Records the date of death if applicable.
    - sire (CharField): Specifies the sire (father) of the cow.
    - dam (CharField): Specifies the dam (mother) of the cow.
    """

class Cow(models.Model):

    breed = models.CharField(
        max_length=20,
        choices=BreedChoices.choices,
        blank=False,
    )

    tag_number = models.CharField(max_length=255, primary_key=True, editable=False)

    parity = models.PositiveIntegerField()
    age = models.PositiveIntegerField()

    # Field to store the date of birth of the cow.
    date_of_birth = models.DateField()

    # Field for the name of the cow.
    name = models.CharField(max_length=255)

    # Field to specify the gender of the cow.
    gender = models.CharField(
        max_length=10,
        choices=SexChoices.choices,
        blank=False,
    )

    # Field to indicate the availability status of the cow.
    availability_status = models.BooleanField(default=True)

    # Field to track the current pregnancy status of the cow.
    current_pregnancy_status = models.CharField(max_length=50, blank=True)

    # Field to categorize the cow (e.g., calf, heifer, milking cow).
    category = models.CharField(max_length=50)

    # Field to capture the current production status of the cow.
    current_production_status = models.CharField(max_length=50)

    # Field to record the date the cow was introduced to the farm.
    date_introduced_in_farm = models.DateField()

    # Field to indicate whether the cow was bought.
    is_bought = models.BooleanField(default=False)

    # Field to capture the date of death if applicable.
    date_of_death = models.DateField(null=True, blank=True)

    # Field to specify the sire of the cow.
    sire = models.CharField(max_length=255, blank=True)

    # Field to specify the dam of the cow.
    dam = models.CharField(max_length=255, blank=True)

    # Field for the age in farm
    age_in_farm = property(calculate_age_in_farm)

    def calculate_age_in_farm(self):
        today = date.today()
        introduced_date = self.date_introduced_in_farm
        age_in_farm = today.year - introduced_date.year - ((today.month, today.day) < (introduced_date.month, introduced_date.day))
        return age_in_farm

    def clean(self):
        # Use CowValidator for validation checks
        CowValidator.validate_category_production_status(self)
        CowValidator.validate_positive_age(self.age)
        CowValidator.validate_introduction_date(self.date_introduced_in_farm)

    def save(self, *args, **kwargs):
        # Generate a unique tag number using a combination of date and UUID
        if not self.tag_number:
            today_str = date.today().strftime("%Y%m%d")
            uuid_str = str(uuid.uuid4().hex)[:6]  # Use the first 6 characters of UUID
            self.tag_number = f"{today_str}-{uuid_str}"
        self.clean()
        super().save(*args, **kwargs)
