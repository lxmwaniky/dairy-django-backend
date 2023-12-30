from django.db import models

from core.utils import todays_date
from production.choices import LactationStageChoices


class LactationManager(models.Manager):
    """
    Custom manager for the Lactation model providing utility methods for managing and querying lactation instances.

    Methods:
    - `days_in_lactation(lactation)`: Calculates and returns the number of days in the lactation period.
    - `lactation_stage(lactation)`: Determines the stage of lactation based on the number of days.
    - `lactation_end_date_formatted(lactation)`: Returns the formatted end date of the lactation.

    Usage:
        Use this manager to perform various operations related to lactations, such as calculating durations,
        determining lactation stages, and formatting end dates.

    Example:
        ```
        class Lactation(models.Model):
            objects = LactationManager()
        ```
    """

    @staticmethod
    def days_in_lactation(lactation):
        """
        Calculate the number of days in the lactation period.
        If the lactation has ended, return the difference between the end date and start date.
        If the lactation is ongoing, return the difference between the current date and start date.
        """
        if lactation.actual_end_date:
            return (lactation.actual_end_date - lactation.start_date).days
        else:
            return (todays_date - lactation.start_date).days

    def lactation_stage(self, lactation):
        """
        Determine the stage of lactation based on the number of days.
        """
        days_in_lactation = self.days_in_lactation(lactation)

        if lactation.actual_end_date:
            return LactationStageChoices.ENDED
        elif days_in_lactation <= 100:
            return LactationStageChoices.EARLY
        elif days_in_lactation <= 200:
            return LactationStageChoices.MID
        elif days_in_lactation <= 275:
            return LactationStageChoices.LATE
        else:
            return LactationStageChoices.DRY

    @staticmethod
    def lactation_end_date_formatted(lactation):
        if lactation.end_date:
            return lactation.actual_end_date.strftime("%Y-%m-%d")
        else:
            return "Ongoing"
