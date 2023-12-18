from django.db import models


# Define choices for the 'Sex' field in your models
class SexChoices(models.TextChoices):
    MALE = "Male"
    FEMALE = "Female"

# choices for the 'Breed' field in your models
class BreedChoices(models.TextChoices):
    FRIESIAN = 'Friesian', 'Friesian'
    SAHIWAL = 'Sahiwal', 'Sahiwal'
    JERSEY = 'Jersey', 'Jersey'
    GUERNSEY = 'Guernsey', 'Guernsey'
    CROSSBREED = 'Crossbreed', 'Crossbreed'
    AYRSHIRE = 'Ayrshire', 'Ayrshire'    
