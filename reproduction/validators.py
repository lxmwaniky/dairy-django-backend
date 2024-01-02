from datetime import timedelta

from django.core.exceptions import ValidationError
from django.utils import timezone

from core.choices import (
    CowPregnancyChoices,
    CowAvailabilityChoices,
    CowProductionStatusChoices,
)
from core.utils import todays_date
from reproduction.choices import PregnancyStatusChoices, PregnancyOutcomeChoices
from users.choices import SexChoices


class PregnancyValidator:
    """
    Provides validation methods for the Pregnancy model.

    Methods:
    - `validate_age(age, start_date, cow)`: Validates the age of the cow, start date, and pregnancy threshold.
    - `validate_cow_current_pregnancy_status(cow)`: Validates the current pregnancy status of the cow.
    - `validate_cow_availability_status(cow)`: Validates the availability status of the cow.
    - `validate_pregnancy_status(pregnancy_status, start_date, pregnancy_failed_date, pregnancy_duration)`:
        Validates the pregnancy status.
    - `validate_dates(start_date, pregnancy_status, date_of_calving, pregnancy_scan_date, pregnancy_failed_date)`:
        Validates various date-related constraints.
    - `validate_scan_date_and_start_date(pregnancy_scan_date, start_date)`: Validates the scan date in relation to
        the start date.
    - `validate_failed_date_and_start_date(pregnancy_failed_date, start_date, pregnancy_status)`:
        Validates the failed date in relation to the start date and pregnancy status.
    - `validate_outcome(pregnancy_outcome, pregnancy_status, date_of_calving)`: Validates the pregnancy outcome.

    Each method raises a `ValidationError` with a specific error code and message if the validation fails.
    """

    @staticmethod
    def validate_age(age, start_date, cow):
        """
        Validates the age of the cow, start date, and pregnancy threshold.

        Args:
        - `age` (int): The age of the cow in days.
        - `start_date` (date): The start date of the pregnancy.
        - `cow` (Cow): The cow associated with the pregnancy.

        Raises:
        - `ValidationError`: If age is below the threshold, start date is missing or invalid.
        """
        if age < 365:
            raise ValidationError(
                "This cow must have a pregnancy threshold age of 1 year. "
                f"This cow is {round(age / 30.417, 2)} months old.",
                code="age_below_threshold",
            )
        if not start_date:
            raise ValidationError(
                "Provide pregnancy start date.", code="missing_start_date"
            )

        if (start_date - cow.date_of_birth).days < 0:
            raise ValidationError("Invalid start date.", code="invalid_start_date")

        if (start_date - cow.date_of_birth).days < 365:
            raise ValidationError(
                f"Invalid start date. Cow cannot be pregnant at "
                f"{round((start_date - cow.date_of_birth).days / 30.417, 2)} months of age.",
                code="pregnancy_age_threshold_not_met",
            )

    @staticmethod
    def validate_cow_current_pregnancy_status(cow):
        """
        Validates the current pregnancy status of the cow.

        Args:
        - `cow` (Cow): The cow associated with the pregnancy.

        Raises:
        - `ValidationError`: If the cow is already pregnant, calved recently, or not ready.
        """
        if cow.current_pregnancy_status == CowPregnancyChoices.PREGNANT:
            raise ValidationError(
                "This cow is already pregnant!", code="cow_already_pregnant"
            )
        if cow.current_pregnancy_status == CowPregnancyChoices.CALVED:
            raise ValidationError(
                "This cow just gave birth recently!", code="cow_calved_recently"
            )
        if cow.current_pregnancy_status == CowPregnancyChoices.UNAVAILABLE:
            raise ValidationError("This cow is not ready!", code="cow_not_ready")

    @staticmethod
    def validate_cow_availability_status(cow):
        """
        Validates the availability status of the cow.

        Args:
        - `cow` (Cow): The cow associated with the pregnancy.

        Raises:
        - `ValidationError`: If the cow is dead or sold.
        """
        if cow.availability_status == CowAvailabilityChoices.DEAD:
            raise ValidationError(
                "Cannot add pregnancy record for a dead cow.", code="dead_cow"
            )

        if cow.availability_status == CowAvailabilityChoices.SOLD:
            raise ValidationError(
                "Cannot add pregnancy record for a sold cow.", code="sold_cow"
            )

    @staticmethod
    def validate_pregnancy_status(
        pregnancy_status, start_sate, pregnancy_failed_date, pregnancy_duration
    ):
        """
        Validates the pregnancy status.

        Args:
        - `pregnancy_status` (str): The pregnancy status.
        - `start_sate` (date): The start date of the pregnancy.
        - `pregnancy_failed_date` (date): The date of pregnancy failure.
        - `pregnancy_duration` (int): The duration of the pregnancy.

        Raises:
        - `ValidationError`: If the pregnancy status or associated data is invalid.
        """
        if pregnancy_status not in PregnancyStatusChoices.values:
            raise ValidationError(
                f"Invalid pregnancy status: '{pregnancy_status}'.",
                code="invalid_pregnancy_status_choice",
            )

        if (
            pregnancy_status == PregnancyStatusChoices.FAILED
            and not pregnancy_failed_date
        ):
            raise ValidationError(
                "Pregnancy is marked as failed, provide the date of failure",
                code="missing_date_of_failure",
            )

        if (todays_date - start_sate) < timedelta(
            days=30
        ) and pregnancy_status != PregnancyStatusChoices.UNCONFIRMED:
            raise ValidationError(
                f"Confirm the pregnancy status on {start_sate + timedelta(days=30)}",
                code="too_early_to_confirm_status",
            )
        if pregnancy_duration != "Ended":
            if pregnancy_duration >= 30 and pregnancy_status not in [
                PregnancyStatusChoices.CONFIRMED,
                PregnancyStatusChoices.FAILED,
            ]:
                raise ValidationError(
                    f"Pregnancy status must be confirmed or failed. "
                    f"The pregnancy duration is {pregnancy_duration} days."
                )

    @staticmethod
    def validate_dates(start_date, date_of_calving):
        """
        Validates various date-related constraints.

        Args:
        - `start_date` (date): The start date of the pregnancy.
        - `pregnancy_status` (str): The pregnancy status.
        - `date_of_calving` (date): The date of calving.
        - `pregnancy_scan_date` (date): The date of pregnancy scanning.
        - `pregnancy_failed_date` (date): The date of pregnancy failure.

        Raises:
        - `ValidationError`: If any date-related constraints are violated.
        """
        if start_date > todays_date:
            raise ValidationError(
                "Start date cannot be in the future.", code="invalid_start_date"
            )

        if date_of_calving and start_date:
            if date_of_calving < start_date:
                raise ValidationError(
                    "Date of calving must be after the start date.",
                    code="invalid_date_of_calving",
                )

            if date_of_calving > todays_date:
                raise ValidationError(
                    "Calving date cannot be in the future.",
                    code="invalid_date_of_calving",
                )
            min_days_between_calving_and_start = 270
            max_days_between_calving_and_start = 295
            days_difference = (date_of_calving - start_date).days
            if not (
                min_days_between_calving_and_start
                <= days_difference
                <= max_days_between_calving_and_start
            ):
                raise ValidationError(
                    f"Difference between calving date and start date should be between 270 and 295 days. "
                    f"Current difference {days_difference} day(s)",
                    code="invalid_calving_start_date_difference",
                )

    @staticmethod
    def validate_scan_date_and_start_date(pregnancy_scan_date, start_date):
        """
        Validates the scan date in relation to the start date.

        Args:
        - `pregnancy_scan_date` (date): The date of pregnancy scanning.
        - `start_date` (date): The start date of the pregnancy.

        Raises:
        - `ValidationError`: If the scan date is before the start date or in the future.
        """
        if pregnancy_scan_date and start_date:
            if pregnancy_scan_date < start_date:
                raise ValidationError(
                    "Pregnancy scan date must be after the start date.",
                    code="scan_date_before_start_date",
                )

            if pregnancy_scan_date.date() > todays_date:
                raise ValidationError(
                    "Pregnancy scan date cannot be in the future.",
                    code="scan_date_in_future",
                )

            min_days_after_start_date_for_scan = 21
            max_days_after_start_date_for_scan = 60
            days_after_start_date_for_scan = (pregnancy_scan_date - start_date).days
            if not (
                min_days_after_start_date_for_scan
                <= days_after_start_date_for_scan
                <= max_days_after_start_date_for_scan
            ):
                raise ValidationError(
                    f"Scan date should be between 21 and 60 days from the start date."
                    f"Currently {days_after_start_date_for_scan} elapsed.",
                    code="invalid_scan_date_difference",
                )

    @staticmethod
    def validate_failed_date_and_start_date(
        pregnancy_failed_date, start_date, pregnancy_status
    ):
        """
        Validates the failed date in relation to the start date and pregnancy status.

        Args:
        - `pregnancy_failed_date` (date): The date of pregnancy failure.
        - `start_date` (date): The start date of the pregnancy.
        - `pregnancy_status` (str): The pregnancy status.

        Raises:
        - `ValidationError`: If the failed date is invalid or inconsistent with the status.
        """
        if pregnancy_failed_date and start_date:
            if pregnancy_failed_date > todays_date:
                raise ValidationError(
                    "Pregnancy failed date cannot be in the future.",
                    code="failed_date_in_future",
                )

            if pregnancy_failed_date < start_date:
                raise ValidationError(
                    "Pregnancy failed date cannot be before the start date.",
                    code="failed_date_before_start_date",
                )

            if (
                pregnancy_failed_date
                and pregnancy_status != PregnancyStatusChoices.FAILED
            ):
                raise ValidationError(
                    "Pregnancy status must be 'Failed' if pregnancy failed date is provided.",
                    code="invalid_failed_date_status",
                )

            min_days_after_start_date_for_failure = 21
            max_days_after_start_date_for_failure = 295
            days_after_start_date_for_failure = (
                pregnancy_failed_date - start_date
            ).days
            if not (
                min_days_after_start_date_for_failure
                <= days_after_start_date_for_failure
                <= max_days_after_start_date_for_failure
            ):
                raise ValidationError(
                    "Pregnancy failed date must be between 21 and 295 days from the start date.",
                    code="invalid_failed_date_difference",
                )

    @staticmethod
    def validate_outcome(pregnancy_outcome, pregnancy_status, date_of_calving):
        """
        Validates the pregnancy outcome.

        Args:
        - `pregnancy_outcome` (str): The pregnancy outcome.
        - `pregnancy_status` (str): The pregnancy status.
        - `date_of_calving` (date): The date of calving.

        Raises:
        - `ValidationError`: If the outcome or its association with other data is invalid.
        """
        if pregnancy_outcome:
            if pregnancy_outcome not in PregnancyOutcomeChoices.values:
                raise ValidationError(
                    f"Invalid pregnancy outcome: '{pregnancy_outcome}'.",
                    code="invalid_outcome_choice",
                )

            if (
                pregnancy_outcome
                in [PregnancyOutcomeChoices.LIVE, PregnancyOutcomeChoices.STILLBORN]
                and pregnancy_status != PregnancyStatusChoices.CONFIRMED
            ):
                raise ValidationError(
                    f"Pregnancy status must be 'Confirmed' if the pregnancy outcome is '{pregnancy_outcome}'.",
                    code="invalid_outcome_status",
                )

            if (
                pregnancy_outcome == PregnancyOutcomeChoices.LIVE
                and not date_of_calving
            ):
                raise ValidationError(
                    f"Date of calving must be provided if the pregnancy outcome is '{pregnancy_outcome}'.",
                    code="missing_date_of_calving",
                )

            if (
                pregnancy_outcome == PregnancyOutcomeChoices.MISCARRIAGE
                and pregnancy_status != PregnancyStatusChoices.FAILED
            ):
                raise ValidationError(
                    f"Pregnancy status must be 'Failed' if the pregnancy outcome is 'Miscarriage'. "
                    f"Currently its {pregnancy_status}",
                    code="invalid_outcome_status",
                )

        if date_of_calving and pregnancy_outcome not in [
            PregnancyOutcomeChoices.LIVE,
            PregnancyOutcomeChoices.STILLBORN,
        ]:
            raise ValidationError(
                "Provide the pregnancy outcome", code="missing_outcome"
            )


class HeatValidator:
    """
    Provides validation methods for the Heat model.

    Methods:
    - `validate_pregnancy(cow)`: Validates that the cow is not already pregnant.
    - `validate_production_status(cow)`: Validates that the cow is in an open production status.
    - `validate_already_in_heat(cow)`: Validates that the cow is not already in heat within the past day.
    - `validate_dead(cow)`: Validates that the cow is not dead.
    - `validate_gender(cow)`: Validates that the heat can only be observed in female cows.
    - `validate_within_60_days_after_calving(cow, observation_time)`: Validates that the cow is not in heat within
        60 days after calving.
    - `validate_within_21_days_of_previous_heat(cow, observation_time)`: Validates that the cow is not in heat within
        21 days of the previous heat observation.
    - `validate_min_age(cow)`: Validates that the cow is at least 12 months old to be in heat.

    Each method raises a `ValidationError` with a specific error code and message if the validation fails.
    """

    @staticmethod
    def validate_pregnancy(cow):
        """
        Validates that the cow is not already pregnant.

        Args:
        - `cow` (Cow): The cow associated with the heat observation.

        Raises:
        - `ValidationError`: If the cow is already pregnant.
        """
        if cow.current_pregnancy_status == CowPregnancyChoices.PREGNANT:
            raise ValidationError("Cow is already pregnant.", code="cow_already_pregnant")

    @staticmethod
    def validate_production_status(cow):
        """
        Validates that the cow is in an open production status.

        Args:
        - `cow` (Cow): The cow associated with the heat observation.

        Raises:
        - `ValidationError`: If the cow is not in an open production status.
        """
        if cow.current_production_status != CowProductionStatusChoices.OPEN:
            raise ValidationError(
                f"Cow must be open and ready to be served. This cow is marked as {cow.current_production_status}",
                code="invalid_production_status",
            )

    @staticmethod
    def validate_already_in_heat(cow):
        """
        Validates that the cow is not already in heat within the past day.

        Args:
        - `cow` (Cow): The cow associated with the heat observation.

        Raises:
        - `ValidationError`: If the cow is already in heat within the past day.
        """
        if cow.heat_records.filter(
            observation_time__range=(
                timezone.now() - timedelta(days=1),
                timezone.now(),
            )
        ).exists():
            raise ValidationError("Cow is already in heat within the past day.", code="already_in_heat")

    @staticmethod
    def validate_dead(cow):
        """
        Validates that the cow is not dead.

        Args:
        - `cow` (Cow): The cow associated with the heat observation.

        Raises:
        - `ValidationError`: If the cow is dead.
        """
        if cow.availability_status == CowAvailabilityChoices.DEAD:
            raise ValidationError("Cow is dead and cannot be in heat.", code="dead_cow")

    @staticmethod
    def validate_gender(cow):
        """
        Validates that the heat can only be observed in female cows.

        Args:
        - `cow` (Cow): The cow associated with the heat observation.

        Raises:
        - `ValidationError`: If the cow's gender is not female.
        """
        if cow.gender == SexChoices.MALE:
            raise ValidationError("Heat can only be observed in female cows.", code="invalid_gender")

    @staticmethod
    def validate_within_60_days_after_calving(cow, observation_time):
        """
        Validates that the cow is not in heat within 60 days after calving.

        Args:
        - `cow` (Cow): The cow associated with the heat observation.
        - `observation_time` (datetime): The time of heat observation.

        Raises:
        - `ValidationError`: If the cow is in heat within 60 days after calving.
        """
        has_pregnancy_records = cow.pregnancies.exists()

        if has_pregnancy_records:
            latest_pregnancy = cow.pregnancies.latest("-date_of_calving")
            if (
                cow.current_pregnancy_status == CowPregnancyChoices.CALVED
                and (observation_time.date() - latest_pregnancy.date_of_calving) < timedelta(days=60)
            ):
                raise ValidationError("Cow cannot be in heat within 60 days after calving.",
                                      code="in_heat_after_calving")

    @staticmethod
    def validate_within_21_days_of_previous_heat(cow, observation_time):
        """
        Validates that the cow is not in heat within 21 days of the previous heat observation.

        Args:
        - `cow` (Cow): The cow associated with the heat observation.
        - `observation_time` (datetime): The time of heat observation.

        Raises:
        - `ValidationError`: If the cow is in heat within 21 days of the previous heat observation.
        """
        if cow.heat_records.filter(
            observation_time__range=(
                observation_time - timedelta(days=21),
                observation_time,
            )
        ).exists():
            raise ValidationError("Cow cannot be in heat within 21 days of previous heat observation.",
                                  code="in_heat_within_21_days")

    @staticmethod
    def validate_min_age(cow):
        """
        Validates that the cow is at least 12 months old to be in heat.

        Args:
        - `cow` (Cow): The cow associated with the heat observation.

        Raises:
        - `ValidationError`: If the cow is not at least 12 months old.
        """
        if cow.age < 365:
            raise ValidationError("Cow must be at least 12 months old to be in heat.", code="invalid_age_for_heat")
