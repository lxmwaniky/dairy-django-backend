from django.core.exceptions import ValidationError

from core.choices import CowAvailabilityChoices


class WeightRecordValidator:
    """
    Provides validation methods for weight records associated with cows.

    Methods:
    - `validate_weight(weight_in_kgs)`: Validates the weight of a cow in kilograms.
    - `validate_cow_availability_status(cow)`: Validates the availability status of a cow for recording weight.
    - `validate_frequency_of_weight_records(date_taken, cow)`: Validates the frequency of weight records for a cow.

    """
    @staticmethod
    def validate_weight(weight_in_kgs):
        """
        Validates the weight of a cow in kilograms.

        Args:
        - `weight_in_kgs` (float): The weight of a cow in kilograms.

        Raises:
        - `ValidationError` with codes:
            - "invalid_weight": If the weight is less than 10 kgs or exceeds the maximum allowed weight of 1500 kgs.
        """
        if weight_in_kgs < 10:
            raise ValidationError("A cow cannot weigh less than 10 kgs!", code="invalid_weight")
        if weight_in_kgs > 1500:
            raise ValidationError("A cow's weight cannot exceed 1500 kgs!", code="invalid_weight")

    @staticmethod
    def validate_cow_availability_status(cow):
        """
        Validates the availability status of a cow for recording weight.

        Args:
        - `cow` (Cow): The cow associated with the weight record.

        Raises:
        - `ValidationError` with code "invalid_availability_status": If the cow is not marked as alive.
        """
        if cow.availability_status != CowAvailabilityChoices.ALIVE:
            raise ValidationError(
                f"Weight records are only allowed for cows present in the farm. This cow is marked as: {cow.availability_status}",
                code="invalid_availability_status",
            )

    @staticmethod
    def validate_frequency_of_weight_records(date_taken, cow):
        """
        Validates the frequency of weight records for a cow.

        Args:
        - `date_taken` (Date): The date when the weight record was taken.
        - `cow` (Cow): The cow associated with the weight record.

        Raises:
        - `ValidationError` with code "duplicate_weight_record": If there is more than one weight record for the same cow on the same date.
        """
        from health.models import WeightRecord

        if WeightRecord.objects.filter(cow=cow, date_taken=date_taken).count() > 1:
            raise ValidationError("This cow already has a weight record on this date!", code="duplicate_weight_record")
