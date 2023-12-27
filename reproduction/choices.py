from django.db import models


class PregnancyStatusChoices(models.TextChoices):
    """
    Choices for the pregnancy status of a cow.

    Choices:
    - `CONFIRMED`: Pregnancy is confirmed.
    - `UNCONFIRMED`: Pregnancy is unconfirmed.
    - `FAILED`: Pregnancy has failed.

    Usage:
        These choices represent the pregnancy status in the Pregnancy model.
        Use these choices when defining or querying Pregnancy instances to represent the status of a cow's pregnancy.

    Example:
        ```
        class Pregnancy(models.Model):
            pregnancy_status = models.CharField(
                max_length=11,
                choices=PregnancyStatusChoices.choices,
                default=PregnancyStatusChoices.UNCONFIRMED,
            )
        ```
    """
    CONFIRMED = "Confirmed"
    UNCONFIRMED = "Unconfirmed"
    FAILED = "Failed"


class PregnancyOutcomeChoices(models.TextChoices):
    """
    Choices for the outcome of a cow's pregnancy.

    Choices:
    - `LIVE`: Live birth.
    - `STILLBORN`: Stillborn birth.
    - `MISCARRIAGE`: Miscarriage.

    Usage:
        These choices represent the outcome of a cow's pregnancy in the Pregnancy model.
        Use these choices when defining or querying Pregnancy instances to represent the outcome of a cow's pregnancy.

    Example:
        ```
        class Pregnancy(models.Model):
            pregnancy_outcome = models.CharField(
                max_length=11, choices=PregnancyOutcomeChoices.choices, null=True
            )
        ```
    """
    LIVE = "Live"
    STILLBORN = "Stillborn"
    MISCARRIAGE = "Miscarriage"
