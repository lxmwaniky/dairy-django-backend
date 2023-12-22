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

    FRIESIAN = "Friesian"
    SAHIWAL = "Sahiwal"
    JERSEY = "Jersey"
    GUERNSEY = "Guernsey"
    CROSSBREED = "Crossbreed"
    AYRSHIRE = "Ayrshire"


class CowAvailabilityChoices(models.TextChoices):
    """
    Choices for the availability status of a cow.

    Choices:
    - `ALIVE`: Cow is alive and active.
    - `SOLD`: Cow has been sold.
    - `DEAD`: Cow has died.

    Usage:
        These choices represent the availability status of a cow in the Cow model.
        Use these choices when defining or querying Cow instances to represent the current status of a cow.

    Example:
        ```
        class Cow(models.Model):
            availability_status = models.CharField(max_length=50, choices=CowAvailabilityChoices.choices)
        ```
    """

    ALIVE = "Alive"
    SOLD = "Sold"
    DEAD = "Dead"


class CowPregnancyChoices(models.TextChoices):
    """
    Choices for the pregnancy status of a cow.

    Choices:
    - `OPEN`: Cow is not pregnant.
    - `PREGNANT`: Cow is pregnant.
    - `CALVED`: Cow has calved.
    - `UNAVAILABLE`: Cow cannot have pregnancy status.

    Usage:
        These choices represent the pregnancy status of a cow in the Cow model.
        Use these choices when defining or querying Cow instances to represent the current pregnancy status of a cow.

    Example:
        ```
        class Cow(models.Model):
            current_pregnancy_status = models.CharField(max_length=15, choices=CowPregnancyChoices.choices)
        ```
    """

    OPEN = "Open"
    PREGNANT = "Pregnant"
    CALVED = "Calved"
    UNAVAILABLE = "Unavailable"


class CowCategoryChoices(models.TextChoices):
    """
    Choices for the category of a cow.

    Choices:
    - `CALF`: Represents a calf.
    - `WEANER`: Represents a weaner.
    - `HEIFER`: Represents a heifer.
    - `BULL`: Represents a bull.
    - `MILKING_COW`: Represents a milking cow.

    Usage:
        These choices represent the category of a cow in the Cow model.
        Use these choices when defining or querying Cow instances to represent the category of a cow.

    Example:
        ```
        class Cow(models.Model):
            category = models.CharField(max_length=15, choices=CowCategoryChoices.choices)
        ```
    """

    CALF = "Calf"
    WEANER = "Weaner"
    HEIFER = "Heifer"
    BULL = "Bull"
    MILKING_COW = "Milking Cow"


class CowProductionStatusChoices(models.TextChoices):
    """
    Choices for the production status of a cow.

    Choices:
    - `OPEN`: Cow is open (not pregnant or lactating).
    - `PREGNANT_NOT_LACTATING`: Cow is pregnant but not lactating.
    - `PREGNANT_AND_LACTATING`: Cow is pregnant and lactating.
    - `DRY`: Cow is dry (not lactating).
    - `CULLED`: Cow has been culled.
    - `QUARANTINED`: Cow is quarantined.
    - `BULL`: Represents a bull.
    - `YOUNG_BULL`: Represents a young bull.
    - `YOUNG_HEIFER`: Represents a young heifer.
    - `MATURE_BULL`: Represents a mature bull.
    - `CALF`: Represents a calf.
    - `WEANER`: Represents a weaner.

    Usage:
        These choices represent the production status of a cow in the Cow model.
        Use these choices when defining or querying Cow instances to represent the current production status of a cow.

    Example:
        ```
        class Cow(models.Model):
            current_production_status = models.CharField(max_length=15, choices=CowProductionStatusChoices.choices)
        ```
    """

    OPEN = "Open"
    PREGNANT_NOT_LACTATING = "Pregnant not Lactating"
    PREGNANT_AND_LACTATING = "Pregnant and Lactating"
    DRY = "Dry"
    CULLED = "Culled"
    QUARANTINED = "Quarantined"
    BULL = "Bull"
    YOUNG_BULL = "Young Bull"
    YOUNG_HEIFER = "Young Heifer"
    MATURE_BULL = "Mature Bull"
    CALF = "Calf"
    WEANER = "Weaner"
