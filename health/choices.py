from django.db import models


class CullingReasonChoices(models.TextChoices):
    """
        Choices for reasons behind culling a cow.
    
        Choices:
        - `INJURIES`: Culling due to injuries.
        - `CHRONIC_HEALTH`: Culling due to chronic health issues.
        - `COST_OF_CARE`: Culling due to the high cost of care.
        - `UNPROFITABLE`: Culling because the cow is unprofitable.
        - `LOW_MARKET_DEMAND`: Culling due to low market demand.
        - `AGE`: Culling based on the age of the cow.
        - `CONSISTENT_LOW_PRODUCTION`: Culling due to consistently low milk production.
        - `LOW_QUALITY`: Culling due to low-quality milk production.
        - `INEFFICIENT_FEED_CONVERSION`: Culling due to inefficient feed conversion.
        - `INHERITED_DISEASES`: Culling due to inherited diseases.
        - `INBREEDING`: Culling due to inbreeding concerns.
        - `UNWANTED_TRAITS`: Culling due to unwanted traits.
        - `CLIMATE_CHANGE`: Culling due to the impact of climate change.
        - `NATURAL_DISASTER`: Culling due to natural disasters.
        - `OVERPOPULATION`: Culling due to overpopulation concerns.
        - `GOVERNMENT_REGULATIONS`: Culling to comply with government regulations.
        - `ANIMAL_WELFARE_STANDARDS`: Culling to meet animal welfare standards.
        - `ENVIRONMENT_PROTECTION_LAWS`: Culling to comply with environmental protection laws.
    
        Usage:
            These choices represent various reasons for culling a cow and are used as options in the CullingRecord model.
    
        Example:
            ```
            class CullingRecord(models.Model):
                cow = models.OneToOneField(Cow, on_delete=models.CASCADE, related_name="culling_record")
                reason = models.CharField(max_length=35, choices=CullingReasonChoices.choices)
                notes = models.TextField(null=True, max_length=100)
                date_carried = models.DateField(auto_now_add=True)
            ```
        """

    # MEDICAL_REASONS
    INJURIES = "Injuries"
    CHRONIC_HEALTH = "Chronic Health Issues"

    # FINANCIAL_REASONS
    COST_OF_CARE = "Cost Of Care"
    UNPROFITABLE = "Unprofitable"
    LOW_MARKET_DEMAND = "Low Market Demand"

    # PRODUCTION_REASONS
    AGE = "Age"
    CONSISTENT_LOW_PRODUCTION = "Consistent Low Production"
    CONSISTENT_POOR_QUALITY = "Low Quality"
    INEFFICIENT_FEED_CONVERSION = "Inefficient Feed Conversion"

    # GENETIC_REASONS
    INHERITED_DISEASES = "Inherited Diseases"
    INBREEDING = "Inbreeding"
    UNWANTED_TRAITS = "Unwanted Traits"

    # ENVIRONMENTAL_REASONS
    CLIMATE_CHANGE = "Climate Change"
    NATURAL_DISASTER = "Natural Disaster"
    OVERPOPULATION = "Overpopulation"

    # LEGAL_REASONS
    GOVERNMENT_REGULATIONS = "Government Regulations"
    ANIMAL_WELFARE_STANDARDS = "Animal Welfare Standards"
    ENVIRONMENT_PROTECTION_LAWS = "Environmental Protection Laws"
