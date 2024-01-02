from django.db import models
from django.utils import timezone

from core.models import Cow
from reproduction.choices import PregnancyStatusChoices, PregnancyOutcomeChoices
from reproduction.managers import PregnancyManager
from reproduction.validators import PregnancyValidator, HeatValidator


class Pregnancy(models.Model):
    """
    Represents a pregnancy record associated with a specific cow in the dairy farm.

    Attributes:
    - `cow` (Cow): The cow associated with the pregnancy.
    - `start_date` (date): The start date of the pregnancy.
    - `date_of_calving` (date or None): The date of calving, if applicable.
    - `pregnancy_status` (str): The current status of the pregnancy.
    - `pregnancy_notes` (str or None): Additional notes related to the pregnancy.
    - `calving_notes` (str or None): Additional notes related to calving.
    - `pregnancy_scan_date` (date or None): The date of pregnancy scanning, if applicable.
    - `pregnancy_failed_date` (date or None): The date of pregnancy failure, if applicable.
    - `pregnancy_outcome` (str or None): The outcome of the pregnancy.

    Methods:
    - `pregnancy_duration`: Returns the number of days since the inception of pregnancy.
    - `due_date`: Returns the due date of the pregnancy.

    Custom Managers:
    - `objects` (PregnancyManager): Custom manager for handling pregnancy-related operations.

    Overrides:
    - `clean`: Performs validation checks before saving the pregnancy record.
    - `save`: Overrides the save method to ensure validation before saving.

    Raises:
    - `ValidationError`: If pregnancy record validation fails.
    """

    cow = models.ForeignKey(Cow, on_delete=models.PROTECT, related_name="pregnancies")
    start_date = models.DateField()
    date_of_calving = models.DateField(null=True)
    pregnancy_status = models.CharField(
        max_length=11,
        choices=PregnancyStatusChoices.choices,
        default=PregnancyStatusChoices.UNCONFIRMED,
    )
    pregnancy_notes = models.TextField(null=True)
    calving_notes = models.TextField(null=True)
    pregnancy_scan_date = models.DateField(null=True)
    pregnancy_failed_date = models.DateField(null=True)
    pregnancy_outcome = models.CharField(
        max_length=11, choices=PregnancyOutcomeChoices.choices, null=True
    )

    objects = PregnancyManager()

    @property
    def pregnancy_duration(self):
        """
        Returns the number of days since the inception of pregnancy.
        """
        return PregnancyManager.pregnancy_duration(self)

    @property
    def due_date(self):
        """
        Returns the due date of the pregnancy.
        """
        return PregnancyManager.due_date(self)

    def clean(self):
        """
        Performs validation checks before saving the pregnancy record.

        Raises:
        - `ValidationError`: If pregnancy record validation fails.
        """
        PregnancyValidator.validate_age(self.cow.age, self.start_date, self.cow)
        PregnancyValidator.validate_cow_current_pregnancy_status(self.cow)
        PregnancyValidator.validate_cow_availability_status(self.cow)
        PregnancyValidator.validate_dates(
            self.start_date,
            self.date_of_calving,
        )
        PregnancyValidator.validate_pregnancy_status(
            self.pregnancy_status, self.start_date, self.pregnancy_failed_date, self.pregnancy_duration
        )
        PregnancyValidator.validate_outcome(
            self.pregnancy_outcome, self.pregnancy_status, self.date_of_calving
        )

    def save(self, *args, **kwargs):
        """
        Overrides the save method to ensure validation before saving.
        """
        self.clean()
        super().save(*args, **kwargs)


class Heat(models.Model):
    """
    Represents a record of heat observation in a cow.

    Attributes:
    - `observation_time` (datetime): The time of heat observation.
    - `cow` (Cow): The cow associated with the heat observation.

    Methods:
    - `__str__`: Returns a string representation of the heat record.

    Overrides:
    - `clean`: Performs validation checks before saving the heat record.
    - `save`: Overrides the save method to ensure validation before saving.

    Raises:
    - `ValidationError`: If heat record validation fails.
    """

    observation_time = models.DateTimeField(default=timezone.now, editable=False)
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE, related_name="heat_records")

    def __str__(self):
        """
        Returns a string representation of the heat record.
        """
        return f"Heat record for cow {self.cow.tag_number} on {self.observation_time}"

    def clean(self):
        """
        Performs validation checks before saving the heat record.

        Raises:
        - `ValidationError`: If heat record validation fails.
        """
        HeatValidator.validate_pregnancy(self.cow)
        HeatValidator.validate_production_status(self.cow)
        HeatValidator.validate_dead(self.cow)
        HeatValidator.validate_gender(self.cow)
        HeatValidator.validate_within_60_days_after_calving(
            self.cow, self.observation_time
        )
        HeatValidator.validate_within_21_days_of_previous_heat(
            self.cow, self.observation_time
        )
        HeatValidator.validate_min_age(self.cow)
        HeatValidator.validate_already_in_heat(self.cow)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to ensure validation before saving.
        """
        self.clean()
        super().save(*args, **kwargs)