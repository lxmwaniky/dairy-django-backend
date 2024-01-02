from rest_framework import serializers
from reproduction.models import Pregnancy, Heat


class PregnancySerializer(serializers.ModelSerializer):
    """
    Serializer for the Pregnancy model.

    Fields:
    - `id`: A read-only field representing the unique identifier of the pregnancy.
    - `cow`: A nested serializer field representing the cow associated with the pregnancy.
    - `start_date`: A date field representing the start date of the pregnancy.
    - `date_of_calving`: A date field representing the date of calving.
    - `pregnancy_status`: A choice field representing the status of the pregnancy.
    - `pregnancy_notes`: A text field representing notes related to the pregnancy.
    - `calving_notes`: A text field representing notes related to calving.
    - `pregnancy_scan_date`: A date field representing the date of pregnancy scanning.
    - `pregnancy_failed_date`: A date field representing the date when the pregnancy failed.
    - `pregnancy_outcome`: A choice field representing the outcome of the pregnancy.

    Meta:
    - `model`: The Pregnancy model for which the serializer is defined.
    - `fields`: The fields to include in the serialized representation.

    Usage:
        Use this serializer to convert Pregnancy model instances to JSON representations
        and vice versa. It includes read-only fields for additional information such as
        pregnancy duration and due date.

    Example:
        ```
        class Pregnancy(models.Model):
            cow = models.ForeignKey(Cow, on_delete=models.CASCADE)
            start_date = models.DateField()
            date_of_calving = models.DateField()
            pregnancy_status = models.CharField(max_length=50, choices=PregnancyStatusChoices.choices)
            pregnancy_notes = models.TextField()
            calving_notes = models.TextField()
            pregnancy_scan_date = models.DateField()
            pregnancy_failed_date = models.DateField()
            pregnancy_outcome = models.CharField(max_length=50, choices=PregnancyOutcomeChoices.choices)

        class PregnancySerializer(serializers.ModelSerializer):
            due_date = serializers.ReadOnlyField()
            pregnancy_duration = serializers.ReadOnlyField()

            class Meta:
                model = Pregnancy
                fields = ("id", "cow", "start_date", "date_of_calving", "pregnancy_status", "pregnancy_notes",
                          "calving_notes", "pregnancy_scan_date", "pregnancy_failed_date", "pregnancy_outcome",
                          "pregnancy_duration", "due_date")
        ```
    """

    class Meta:
        model = Pregnancy
        fields = ("id", "cow", "start_date", "date_of_calving", "pregnancy_status", "pregnancy_notes",
                  "calving_notes", "pregnancy_scan_date", "pregnancy_failed_date", "pregnancy_outcome",
                  "pregnancy_duration", "due_date")


class HeatSerializer(serializers.ModelSerializer):
    """
    Serializer for the Heat model.

    Fields:
    - `id`: A read-only field representing the unique identifier of the heat observation.
    - `cow`: A nested serializer field representing the cow associated with the heat observation.
    - `observation_time`: A datetime field representing the time of the heat observation.

    Meta:
    - `model`: The Heat model for which the serializer is defined.
    - `fields`: The fields to include in the serialized representation.

    Usage:
        Use this serializer to convert Heat model instances to JSON representations and vice versa.

    Example:
        ```
        class Heat(models.Model):
            cow = models.ForeignKey(Cow, on_delete=models.CASCADE)
            observation_time = models.DateTimeField()

        class HeatSerializer(serializers.ModelSerializer):
            class Meta:
                model = Heat
                fields = ("id", "cow", "observation_time")
        ```
    """

    class Meta:
        model = Heat
        fields = ("id", "cow", "observation_time")
