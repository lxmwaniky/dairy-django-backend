from datetime import timedelta

from django.db import models

from core.utils import todays_date
from reproduction.choices import PregnancyStatusChoices, PregnancyOutcomeChoices


class PregnancyManager(models.Manager):
    """
    Custom manager for the Pregnancy model providing utility methods for managing and querying pregnancy instances.

    Methods:
    - `pregnancy_duration(pregnancy)`: Calculates and returns the duration of a pregnancy in days.
    - `due_date(pregnancy)`: Calculates and returns the expected due date of a pregnancy.
    - `get_confirmed_pregnancies()`: Returns a queryset of confirmed pregnancies.
    - `get_unconfirmed_pregnancies()`: Returns a queryset of unconfirmed pregnancies.
    - `get_failed_pregnancies()`: Returns a queryset of failed pregnancies.
    - `get_successful_pregnancies()`: Returns a queryset of successful (live) pregnancies.
    - `get_miscarried_pregnancies()`: Returns a queryset of miscarried pregnancies.
    - `get_stillborn_pregnancies()`: Returns a queryset of stillborn pregnancies.

    Usage:
        Use this manager to perform various operations related to pregnancies, such as calculating durations,
        determining due dates, and querying different pregnancy statuses.

    Example:
        ```
        class Pregnancy(models.Model):
            objects = PregnancyManager()
        ```
    """

    @staticmethod
    def pregnancy_duration(pregnancy):
        """
        Calculates and returns the duration of a pregnancy in days.

        Args:
        - `pregnancy`: The pregnancy object.

        Returns:
        - The duration of the pregnancy in days or "Ended" if the pregnancy has concluded.
        """
        if pregnancy.start_date and not (pregnancy.date_of_calving and pregnancy.pregnancy_outcome):
            return (todays_date - pregnancy.start_date).days
        if pregnancy.date_of_calving and pregnancy.pregnancy_outcome:
            return "Ended"

    @staticmethod
    def due_date(pregnancy):
        """
        Calculates and returns the expected due date of a pregnancy.

        Args:
        - `pregnancy`: The pregnancy object.

        Returns:
        - The expected due date of the pregnancy or "Ended" if the pregnancy has concluded.
        """
        if pregnancy.start_date and not pregnancy.pregnancy_outcome:
            return pregnancy.start_date + timedelta(days=285)
        return "Ended"

    def get_confirmed_pregnancies(self):
        """
        Returns a queryset of confirmed pregnancies.

        Returns:
        - A queryset of confirmed pregnancies.
        """
        return self.filter(pregnancy_status=PregnancyStatusChoices.CONFIRMED)

    def get_unconfirmed_pregnancies(self):
        """
        Returns a queryset of unconfirmed pregnancies.

        Returns:
        - A queryset of unconfirmed pregnancies.
        """
        return self.filter(pregnancy_status=PregnancyStatusChoices.UNCONFIRMED)

    def get_failed_pregnancies(self):
        """
        Returns a queryset of failed pregnancies.

        Returns:
        - A queryset of failed pregnancies.
        """
        return self.filter(pregnancy_status=PregnancyStatusChoices.FAILED)

    def get_successful_pregnancies(self):
        """
        Returns a queryset of successful (live) pregnancies.

        Returns:
        - A queryset of successful (live) pregnancies.
        """
        return self.filter(pregnancy_outcome=PregnancyOutcomeChoices.LIVE)

    def get_miscarried_pregnancies(self):
        """
        Returns a queryset of miscarried pregnancies.

        Returns:
        - A queryset of miscarried pregnancies.
        """
        return self.filter(pregnancy_outcome=PregnancyOutcomeChoices.MISCARRIAGE)

    def get_stillborn_pregnancies(self):
        """
        Returns a queryset of stillborn pregnancies.

        Returns:
        - A queryset of stillborn pregnancies.
        """
        return self.filter(pregnancy_outcome=PregnancyOutcomeChoices.STILLBORN)
