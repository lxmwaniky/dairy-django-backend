from rest_framework.exceptions import ValidationError


class CustomUserValidator:
    """
    Helper class for validating fields in the CustomUser model.

    Methods:
    - `validate_sex(sex)`: Validates that the sex field value is within the specified choices.
    - `validate_username(username)`: Validates that the username is unique and exists in the database.

    """

    @classmethod
    def validate_sex(cls, sex):
        """
        Validates that the sex field value is within the specified choices.

        Parameters:
        - `sex`: The value of the sex field.

        Raises:
        - `ValidationError`: If the sex value is not within the choices or is an empty string.

        """
        from users.choices import SexChoices

        if not sex:
            raise ValidationError("Sex field cannot be empty.")

        if sex not in SexChoices.values:
            raise ValidationError(
                f"Invalid value for sex: '{sex}'. It must be one of {SexChoices.values}."
            )

    @classmethod
    def validate_username(cls, username):
        """
        Validates that the username is unique and exists in the database.

        Parameters:
        - `username`: The username to validate.

        Raises:
        - `ValidationError`: If the username is not unique or does not exist in the database.

        """
        from users.models import CustomUser

        if (
            CustomUser.objects.filter(username=username)
            .exclude(username=username)
            .exists()
        ):
            
            raise ValidationError("Username already exists.")

class CustomCowBreedValidator:
    """
    Helper class for validating fields in the CowBreed model.

    Methods:
    - `validate_breed_name(breed_name)`: Validates that the breed_name field value is within the specified choices.

    """

    @classmethod
    def validate_breed_name(cls, breed_name):
        """
        Validates that the breed_name field value is within the specified choices.

        Parameters:
        - `breed_name`: The value of the breed_name field.

        Raises:
        - `ValidationError`: If the breed_name value is not within the choices or is an empty string.

        """ 
        from users.choices import BreedChoices
        if not breed_name:
            raise ValidationError("Breed name field cannot be empty.")

        valid_choices = ", ".join(map(str, BreedChoices.values))

        if breed_name not in BreedChoices.values:
            raise ValidationError(
                f"Invalid value for breed name: '{breed_name}'. It must be one of {valid_choices}."
        )
