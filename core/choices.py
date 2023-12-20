from django.db import models


class CowBreedChoices(models.TextChoices):
    """
    Enumeration of choices for representing different cow breeds.

    Choices:
    - `FRIESIAN`: Represents the Friesian cow breed.
    - `SAHIWAL`: Represents the Sahiwal cow breed.
    - `JERSEY`: Represents the Jersey cow breed.
    - `GUERNSEY`: Represents the Guernsey cow breed.
    - `CROSSBREED`: Represents a crossbreed of cows.
    - `AYRSHIRE`: Represents the Ayrshire cow breed.

    Usage:
        This enumeration provides predefined choices for the cow breed field in the CowBreed model.
        Use these choices when defining or querying CowBreed instances to represent specific cow breeds.

    Example:
        ```
        class CowBreed(models.Model):
            name = models.CharField(max_length=50, choices=CowBreedChoices.choices)
        ```

    """
    FRIESIAN = 'Friesian'
    SAHIWAL = 'Sahiwal'
    JERSEY = 'Jersey'
    GUERNSEY = 'Guernsey'
    CROSSBREED = 'Crossbreed'
    AYRSHIRE = 'Ayrshire'
