from django.db import models


class PregnancyStatusChoices(models.TextChoices):
    CONFIRMED = "Confirmed"
    UNCONFIRMED = "Unconfirmed"
    FAILED = "Failed"


class PregnancyOutcomeChoices(models.TextChoices):
    LIVE = "Live"
    STILLBORN = "Stillborn"
    MISCARRIAGE = "Miscarriage"
