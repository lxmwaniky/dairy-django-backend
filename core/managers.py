from django.db import models

from core.choices import CowAvailabilityChoices, CowPregnancyChoices
from core.utils import todays_date
from users.choices import SexChoices


class CowManager(models.Manager):
    """
    Custom manager for the Cow model providing various utility methods for querying and managing cow instances.

    Methods:
    - `get_tag_number(cow)`: Generates and returns the tag number for a cow.
    - `calculate_age(cow)`: Calculates and returns the age of a cow in days.
    - `calculate_age_in_farm(cow)`: Calculates and returns the age of a cow in days since introduction to the farm.
    - `get_available_cows()`: Returns a queryset of available (alive) cows.
    - `get_pregnant_cows()`: Returns a queryset of pregnant cows.
    - `get_male_cows()`: Returns a queryset of available (alive) male cows.
    - `get_female_cows()`: Returns a queryset of available (alive) female cows.
    - `get_sold_cows()`: Returns a queryset of sold cows.
    - `get_dead_cows()`: Returns a queryset of dead cows.
    - `get_calf_records(cow)`: Returns a list of calf records associated with the cow.

    Usage:
        Use this manager to perform various operations related to cows, such as retrieving specific subsets
        of cows, calculating ages, and generating tag numbers.

    Example:
        ```
        class Cow(models.Model):
            objects = CowManager()
        ```
    """

    @staticmethod
    def get_tag_number(cow):
        """
        Generates and returns the tag number for a cow.

        Args:
        - `cow`: The cow object.

        Returns:
        - The tag number of the cow in the format "XX-YYYY-ID".
        """
        year_of_birth = cow.date_of_birth.strftime("%Y")
        first_letters_of_breed = cow.breed.name[:2].upper()
        counter = cow.id
        return f"{first_letters_of_breed}-{year_of_birth}-{counter}"

    @staticmethod
    def calculate_age(cow):
        """
        Calculates and returns the age of a cow in days.

        Args:
        - `cow`: The cow object.

        Returns:
        - The age of the cow in days.
        """
        age_in_days = (todays_date - cow.date_of_birth).days
        return age_in_days

    @staticmethod
    def calculate_age_in_farm(cow):
        """
        Calculates and returns the age of a cow in days since introduction to the farm.

        Args:
        - `cow`: The cow object.

        Returns:
        - The age of the cow in days since introduction to the farm.
        """
        age_in_days = (todays_date - cow.date_introduced_in_farm).days
        return age_in_days

    @staticmethod
    def get_available_cows(self):
        """
        Returns a queryset of available (alive) cows.

        Returns:
        - A queryset of available (alive) cows.
        """
        return self.filter(availability_status=CowAvailabilityChoices.ALIVE)

    @staticmethod
    def get_pregnant_cows(self):
        """
        Returns a queryset of pregnant cows.

        Returns:
        - A queryset of pregnant cows.
        """
        return self.filter(pregnancy_status=CowPregnancyChoices.PREGNANT)

    @staticmethod
    def get_male_cows(self):
        """
        Returns a queryset of available (alive) male cows.

        Returns:
        - A queryset of available (alive) male cows.
        """
        return self.filter(
            availability_status=CowAvailabilityChoices.ALIVE, gender=SexChoices.MALE
        )

    @staticmethod
    def get_female_cows(self):
        """
        Returns a queryset of available (alive) female cows.

        Returns:
        - A queryset of available (alive) female cows.
        """
        return self.filter(
            availability_status=CowAvailabilityChoices.ALIVE, gender=SexChoices.FEMALE
        )

    @staticmethod
    def get_sold_cows(self):
        """
        Returns a queryset of sold cows.

        Returns:
        - A queryset of sold cows.
        """
        return self.filter(availability_status=CowAvailabilityChoices.SOLD)

    @staticmethod
    def get_dead_cows(self):
        """
        Returns a queryset of dead cows.

        Returns:
        - A queryset of dead cows.
        """
        return self.filter(availability_status=CowAvailabilityChoices.DEAD)

    def get_calf_records(self, cow):
        """
        Returns a list of calf records associated with the cow.

        Args:
        - `cow`: The cow object.

        Returns:
        - A list of calf records associated with the cow.
        """
        from core.models import Cow

        if cow.gender == SexChoices.FEMALE:
            calf_records = list(Cow.objects.filter(dam=cow))
        else:
            calf_records = list(Cow.objects.filter(dam=cow))
        return calf_records
