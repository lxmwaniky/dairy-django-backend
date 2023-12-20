from django.core.exceptions import ValidationError
from datetime import date


class CowBreedValidator:
    @staticmethod
    def validate_breed_name(name):
        """
        Validates that the breed name is unique and belongs to the available choices.

        Args:
        - `name`: The breed name to validate.

        Raises:
        - `ValidationError`: If a breed with the same name already exists or if the breed name is not in the choices.
        """
        from core.models import CowBreed
        from core.choices import CowBreedChoices

        if name not in CowBreedChoices.values:
            raise ValidationError(f"Invalid cow breed: '{name}'.", code='invalid_cow_breed')

        if CowBreed.objects.filter(name=name).exists():
            raise ValidationError(f"A breed with the name '{name}' already exists.", code='duplicate_cow_breed')

class CowValidator:
    @staticmethod
    def validate_category_production_status(cow):
        """
        Validates that if the cow category is 'calf', the production status is limited to 'Newborn' or 'Weaning'.
        """
        if cow.category.lower() == 'calf' and cow.current_production_status.lower() not in ['newborn', 'weaning']:
            raise ValidationError("Calf category should have production status limited to 'Newborn' or 'Weaning'.")

    @staticmethod
    def validate_positive_age(age):
        """
        Validates that the age is a positive integer.
        """
        if age <= 0:
            raise ValidationError("Age must be a positive integer.")

    @staticmethod
    def validate_introduction_date(introduction_date):
        """
        Validates that the introduction date is not in the future.
        """
        if introduction_date > date.today():
            raise ValidationError("Introduction date cannot be in the future.")

