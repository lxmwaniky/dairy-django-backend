from django.db import models

from core.models import Cow
from production.managers import LactationManager
from production.validators import LactationValidator
from reproduction.models import Pregnancy


class Lactation(models.Model):
    """
    Represents a lactation record associated with a specific cow in the dairy farm.

    Attributes:
    - `cow` (Cow): The cow associated with the lactation record.
    - `start_date` (date): The start date of the lactation period.
    - `lactation_number` (int): The number representing the lactation cycle for the cow.
    - `pregnancy` (Pregnancy or None): The associated pregnancy record, if applicable.
    - `actual_end_date` (date or None): The actual end date of the lactation period.

    Meta:
    - `get_latest_by`: Specifies the field used for determining the latest record.

    Methods:
    - `days_in_lactation`: Calculates and returns the number of days in the lactation period.
    - `lactation_stage`: Determines and returns the lactation stage based on the days in lactation.
    - `expected_end_date`: Calculates and returns the expected end date of the lactation period.

    Custom Managers:
    - `objects` (LactationManager): Custom manager for handling lactation-related operations.

    Overrides:
    - `__str__`: Returns a string representation of the lactation record.
    - `clean`: Performs validation checks before saving the lactation record.
    - `save`: Overrides the save method to ensure validation before saving.

    Raises:
    - `ValidationError`: If lactation record validation fails.
    """

    cow = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name="lactations")
    start_date = models.DateField()
    lactation_number = models.PositiveSmallIntegerField(default=1)
    pregnancy = models.OneToOneField(Pregnancy, on_delete=models.CASCADE, null=True)
    actual_end_date = models.DateField(null=True)

    class Meta:
        get_latest_by = "-start_date"

    objects = LactationManager()

    @property
    def days_in_lactation(self):
        """
        Calculates and returns the number of days in the lactation period.

        Returns:
        - `int`: The number of days in the lactation period.
        """
        return Lactation.objects.days_in_lactation(self)

    @property
    def lactation_stage(self):
        """
        Determines and returns the lactation stage based on the days in lactation.

        Returns:
        - `str`: The lactation stage.
        """
        return Lactation.objects.lactation_stage(self)

    @property
    def expected_end_date(self):
        """
        Calculates and returns the expected end date of the lactation period.

        Returns:
        - `date` or `str`: The end date of the lactation period or Ongoing.
        """
        return Lactation.objects.lactation_end_date_formatted(self)

    def __str__(self):
        """
        Returns a string representation of the lactation record.
        """
        return f"Lactation record {self.lactation_number} for {self.cow}"

    def clean(self):
        """
        Performs validation checks before saving the lactation record.

        Raises:
        - `ValidationError`: If lactation record validation fails.
        """

        LactationValidator.validate_age(self.start_date, self.cow)
        LactationValidator.validate_fields(
            self.start_date, self.pregnancy, self.lactation_number, self.cow, self
        )
        # LactationValidator.validate_cow_category(self.cow.category)
        # LactationValidator.validate_cow_origin(self.cow)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to ensure validation before saving.
        """
        self.clean()
        super().save(*args, **kwargs)
