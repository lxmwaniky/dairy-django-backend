from django.db import models


# Define choices for the 'Sex' field in your models
class SexChoices(models.TextChoices):
    MALE = "Male"
    FEMALE = "Female"
