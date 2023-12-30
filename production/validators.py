from datetime import timedelta

from django.core.exceptions import ValidationError

from core.choices import CowCategoryChoices, CowAvailabilityChoices
from core.utils import todays_date
from production.choices import LactationStageChoices
from users.choices import SexChoices


class LactationValidator:
    """
    Provides validation methods for lactation records associated with cows.

    Methods:
    - `validate_age(start_date, cow)`: Validates the start date of lactation based on the cow's age.
    - `validate_cow_origin(cow)`: Validates that manual entry is allowed only for bought cows.
    - `validate_cow_category(category)`: Validates the cow category for lactation records, allowing only bought cows with calves.
    - `validate_fields(start_date, pregnancy, lactation_number, cow, lactation)`: Validates various fields of the lactation record, including start date, end date, pregnancy status, lactation number, and cow's age.

    """
    @staticmethod
    def validate_age(start_date, cow):
        """
        Validates the start date of lactation based on the cow's age.

        Args:
        - `start_date` (date): The start date of the lactation.
        - `cow` (Cow): The cow associated with the lactation record.

        Raises:
        - `ValidationError`: If the start date is before the cow reaches 635 days of age.
        """
        if start_date < cow.date_of_birth + timedelta(days=635):
            raise ValidationError(
                code="invalid_start_date",
                message=f"Invalid start date. Lactation must have started or be around {cow.date_of_birth + timedelta(days=635)}, not {start_date}.",
            )

    @staticmethod
    def validate_cow_origin(cow):
        """
        Validates that manual entry is allowed only for bought cows.

        Args:
        - `cow` (Cow): The cow associated with the lactation record.

        Raises:
        - `ValidationError`: If manual entry is attempted on a cow that is not bought.
        """
        if not cow.is_bought:
            raise ValidationError(
                code="manual_entry_only_on_bought_cows",
                message="Manual entry is allowed only for bought cows.",
            )

    @staticmethod
    def validate_cow_category(category):
        """
        Validates the cow category for lactation records, allowing only bought cows with calves.

        Args:
        - `category` (str): The cow category associated with the lactation record.

        Raises:
        - `ValidationError`: If the cow category is invalid or not a milking cow with calves.
        """
        if category not in CowCategoryChoices.values:
            raise ValidationError(
                code="invalid_cow_category",
                message=f"Invalid cow category: ({category}).",
            )
        if category != CowCategoryChoices.MILKING_COW:
            raise ValidationError(
                code="only_bought_cows_with_calves_allowed",
                message=f"Only bought cows that have calved are allowed. This cow is categorized as ({category})."
                        f" Manual entry is forbidden.",
            )

    @staticmethod
    def validate_fields(start_date, pregnancy, lactation_number, cow, lactation):
        """
        Validates various fields of the lactation record.

        Args:
        - `start_date` (date): The start date of the lactation.
        - `pregnancy` (Pregnancy): The associated pregnancy record (can be None).
        - `lactation_number` (int): The lactation number.
        - `cow` (Cow): The cow associated with the lactation record.
        - `lactation` (Lactation): The lactation record being validated.

        Raises:
        - `ValidationError`: If any of the validation conditions are not met.
        """
        if start_date > todays_date:
            raise ValidationError(
                code="start_date_in_future", message="Start date cannot be in the future."
            )

        if lactation.actual_end_date and lactation.actual_end_date > todays_date:
            raise ValidationError(
                code="end_date_in_future", message="End date cannot be in the future."
            )

        if cow.is_bought and pregnancy is not None:
            raise ValidationError(
                code="pregnancy_should_be_null",
                message=f"Pregnancy must be NULL for this lactation record No.({lactation_number}). {cow.tag_number} "
                        f"never gave birth in this farm; it was brought on {cow.date_introduced_in_farm}.",
            )

        if ((cow.age - 635) / 305) < 1 and lactation_number != 1:
            raise ValidationError(
                code="invalid_lactation_number", message="Invalid lactation number."
            )


class MilkValidator:
    """
    Provides validation methods for milk records associated with cows.

    Methods:
    - `validate_amount_in_kgs(amount_in_kgs)`: Validates the amount of milk in kilograms.
    - `validate_cow_eligibility(cow)`: Validates the eligibility of a cow to record milk based on its status and lactation stage.

    """
    @staticmethod
    def validate_amount_in_kgs(amount_in_kgs):
        """
        Validates the amount of milk in kilograms.

        Args:
        - `amount_in_kgs` (float): The amount of milk in kilograms.

        Raises:
        - `ValidationError` with code "invalid_amount": If the amount is negative or exceeds the maximum expected amount of 35 kgs.
        """
        if amount_in_kgs < 0:
            raise ValidationError("Invalid amount!", code="invalid_amount")
        if amount_in_kgs > 35:
            raise ValidationError(
                f"Amount {amount_in_kgs} Kgs exceeds the maximum expected amount of 35 kgs!",
                code="exceeds_maximum_amount",
            )

    @staticmethod
    def validate_cow_eligibility(cow):
        """
        Validates the eligibility of a cow to record milk based on its status and lactation stage.

        Args:
        - `cow` (Cow): The cow associated with the milk record.

        Raises:
        - `ValidationError` with codes:
            - "invalid_availability_status": If the cow is dead or sold.
            - "male_cow": If the cow is a bull.
            - "no_active_lactation": If the cow has no active lactation.
            - "dried_off_cow": If the cow has been dried off.
            - "previous_lactation_ended": If the previous lactation has ended.
        """
        from production.models import Lactation

        if cow.availability_status == CowAvailabilityChoices.DEAD:
            raise ValidationError("Cannot add milk record for a dead cow.", code="invalid_availability_status")

        if cow.availability_status == CowAvailabilityChoices.SOLD:
            raise ValidationError("Cannot add milk record for a sold cow.", code="invalid_availability_status")

        if cow.gender != SexChoices.FEMALE:
            raise ValidationError("This cow is a Bull and cannot produce milk!", code="male_cow")

        try:
            lactation = Lactation.objects.filter(cow=cow).latest()
        except Lactation.DoesNotExist:
            raise ValidationError("Cannot add milk entry, cow has no active lactation", code="no_active_lactation")

        if lactation.lactation_stage == LactationStageChoices.DRY:
            raise ValidationError("Cannot add milk entry, Cow has been dried off", code="dried_off_cow")

        if lactation.lactation_stage == LactationStageChoices.ENDED:
            raise ValidationError("Cannot add milk entry, Previous Lactation Ended!", code="previous_lactation_ended")
