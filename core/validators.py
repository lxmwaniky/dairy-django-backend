from django.core.exceptions import ValidationError


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
