from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

from users.choices import *
from users.validators import *


class CustomUser(AbstractUser):
    """
    Custom user model representing a user in the farm management system.

    Fields:
    - `username`: A unique character field representing the username of the user.
                  It is limited to a maximum length of 45 characters.
    - `email`: A unique email field representing the email address of the user.
    - `first_name`: A character field representing the first name of the user.
                     It is limited to a maximum length of 20 characters.
    - `last_name`: A character field representing the last name of the user.
                    It is limited to a maximum length of 20 characters.
    - `phone_number`: A phone number field representing the phone number of the user.
                      It is limited to a maximum length of 13 characters and must be unique.
    - `sex`: A character field representing the gender of the user.
             The available choices are defined in the `SexChoices` enum.
             It is limited to a maximum length of 6 characters.
    - `is_farm_owner`: A boolean field representing whether the user is a farm owner.
    - `is_farm_manager`: A boolean field representing whether the user is a farm manager.
    - `is_assistant_farm_manager`: A boolean field representing whether the user is an assistant farm manager.
    - `is_team_leader`: A boolean field representing whether the user is a team leader.
    - `is_farm_worker`: A boolean field representing whether the user is a farm worker.

    Methods:
    - `assign_farm_owner()`: Assigns the user as a farm owner and updates related fields accordingly.
    - `assign_farm_manager()`: Assigns the user as a farm manager and updates related fields accordingly.
    - `assign_assistant_farm_manager()`: Assigns the user as an assistant farm manager and updates related fields accordingly.
    - `assign_team_leader()`: Assigns the user as a team leader and updates related fields accordingly.
    - `assign_farm_worker()`: Assigns the user as a farm worker and updates related fields accordingly.
    - `dismiss_farm_owner()`: Dismisses the user from the farm owner role.
    - `dismiss_farm_manager()`: Dismisses the user from the farm manager role.
    - `dismiss_assistant_farm_manager()`: Dismisses the user from the assistant farm manager role.
    - `dismiss_team_leader()`: Dismisses the user from the team leader role.
    - `dismiss_farm_worker()`: Dismisses the user from the farm worker role.
    - `get_full_name()`: Returns the full name of the user.
    - `get_role()`: Returns the role of the user based on their assigned roles.
    """

    username = models.CharField(max_length=45, unique=True)
    email = models.EmailField(null=True, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_number = PhoneNumberField(max_length=13, unique=True, null=True)
    sex = models.CharField(choices=SexChoices.choices, max_length=6)
    is_farm_owner = models.BooleanField(default=False)
    is_farm_manager = models.BooleanField(default=False)
    is_assistant_farm_manager = models.BooleanField(default=False)
    is_team_leader = models.BooleanField(default=False)
    is_farm_worker = models.BooleanField(default=False)

    REQUIRED_FIELDS = [
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "sex",
        "is_farm_owner",
        "is_farm_manager",
        "is_assistant_farm_manager",
        "is_farm_worker",
        "is_team_leader",
    ]

    def assign_farm_owner(self):
        self.is_farm_owner = True
        self.is_farm_manager = False
        self.is_assistant_farm_manager = False
        self.is_team_leader = False
        self.is_farm_worker = False
        self.save()

    def assign_farm_manager(self):
        self.is_farm_owner = False
        self.is_farm_manager = True
        self.is_assistant_farm_manager = False
        self.is_team_leader = False
        self.is_farm_worker = False
        self.save()

    def assign_assistant_farm_manager(self):
        self.is_farm_owner = False
        self.is_farm_manager = False
        self.is_assistant_farm_manager = True
        self.is_team_leader = False
        self.is_farm_worker = False
        self.save()

    def assign_team_leader(self):
        self.is_farm_owner = False
        self.is_farm_manager = False
        self.is_assistant_farm_manager = False
        self.is_team_leader = True
        self.is_farm_worker = True
        self.save()

    def assign_farm_worker(self):
        self.is_farm_owner = False
        self.is_farm_manager = False
        self.is_asst_farm_manager = False
        self.is_team_leader = False
        self.is_farm_worker = True
        self.save()

    def dismiss_farm_owner(self):
        self.is_farm_owner = False
        self.save()

    def dismiss_farm_manager(self):
        self.is_farm_manager = False
        self.save()

    def dismiss_assistant_farm_manager(self):
        self.is_assistant_farm_manager = False
        self.save()

    def dismiss_team_leader(self):
        self.is_team_leader = False
        self.save()

    def dismiss_farm_worker(self):
        if self.is_team_leader:
            self.is_team_leader = False
        self.is_farm_worker = False
        self.save()

    def get_full_name(self):
        """Return the full name of the user."""
        return f"{self.first_name} {self.last_name}"

    def get_role(self):
        if self.is_farm_owner:
            return "Farm Owner"
        elif self.is_farm_manager:
            return "Farm Manager"
        elif self.is_assistant_farm_manager:
            return "Assistant Farm Manager"
        elif self.is_team_leader:
            return "Team Leader"
        elif self.is_farm_worker:
            return "Farm Worker"

    def clean(self):
        CustomUserValidator.validate_sex(self.sex)
        CustomUserValidator.validate_username(self.username)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class CowBreed(models.Model):
    """
    CowBreed Model

    Represents the breed of a cow in a Django application.

    Attributes:
    - breed_name (CharField): The name of the cow breed.
        Choices are limited to the values defined in BreedChoices.


    Usage:
    1. Create a new CowBreed instance by specifying the breed_name.
    2. Access and modify the breed_name attribute as needed.
    
    Example:
    ```python
    # Creating a new CowBreed instance with the default breed_name (FRIESIAN)
    cow = CowBreed(breed_name=BreedChoices.JERSEY)

    # Accessing and modifying the breed_name attribute
    cow.breed_name = BreedChoices.JERSEY

    # Saving the instance to the database
    cow_breed.save()
    ```

    Note:
    - Ensure that the choices in BreedChoices match the actual cow breeds supported in the application.

    Choices for breed_name:
    - FRIESIAN: Friesian cow breed.
    - JERSEY: Jersey cow breed.
    - HOLSTEIN: Holstein cow breed.
    - OTHER: Other or unspecified cow breed.

    """

    breed_name = models.CharField(
        max_length=20,
        choices=BreedChoices.choices,
        blank=False,  # Ensure the field is not blank
    )

    def save(self, *args, **kwargs):
        # Validate the breed_name before saving
        CustomCowBreedValidator.validate_breed_name(self.breed_name)
        super().save(*args, **kwargs)
