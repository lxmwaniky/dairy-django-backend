from rest_framework import serializers

from production.models import Lactation, Milk
from production.validators import LactationValidator


class LactationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Lactation model.

    Fields:
    - `cow`: A nested serializer field representing the cow associated with the lactation record.
    - `start_date`: A date field representing the start date of the lactation.
    - `lactation_number`: An integer field representing the number of the lactation.
    - `pregnancy`: A nested serializer field representing the associated pregnancy (if any).
    - `actual_end_date`: A date field representing the actual end date of the lactation.
    - `days_in_lactation`: A read-only field representing the duration of the lactation in days.
    - `lactation_stage`: A read-only field representing the stage of the lactation.
    - `expected_end_date`: A read-only field representing the expected end date of the lactation.

    Meta:
    - `model`: The Lactation model for which the serializer is defined.
    - `fields`: The fields to include in the serialized representation.

    Usage:
        Use this serializer to convert Lactation model instances to JSON representations
        and vice versa. It includes read-only fields for additional information such as
        lactation duration and expected end date.

    Example:
        ```
        class Lactation(models.Model):
            cow = models.ForeignKey(Cow, on_delete=models.CASCADE)
            start_date = models.DateField()
            lactation_number = models.IntegerField()
            pregnancy = models.OneToOneField(Pregnancy, on_delete=models.CASCADE, null=True, blank=True)
            actual_end_date = models.DateField()

        class LactationSerializer(serializers.ModelSerializer):
            days_in_lactation = serializers.ReadOnlyField()
            lactation_stage = serializers.ReadOnlyField()
            expected_end_date = serializers.ReadOnlyField()

            class Meta:
                model = Lactation
                fields = ("cow", "start_date", "lactation_number", "pregnancy", "actual_end_date",
                          "days_in_lactation", "lactation_stage", "expected_end_date")
        ```
    """

    days_in_lactation = serializers.ReadOnlyField()
    lactation_stage = serializers.ReadOnlyField()
    expected_end_date = serializers.ReadOnlyField()

    class Meta:
        model = Lactation
        fields = (
            "cow",
            "start_date",
            "lactation_number",
            "pregnancy",
            "actual_end_date",
            "days_in_lactation",
            "lactation_stage",
            "expected_end_date",
        )

    def create(self, validated_data):
        # Get the cow instance from the validated data
        cow_instance = validated_data["cow"]

        LactationValidator.validate_cow_origin(cow_instance)
        LactationValidator.validate_cow_category(cow_instance.category)

        lactation_instance = Lactation.objects.create(**validated_data)
        return lactation_instance


class MilkSerializer(serializers.ModelSerializer):
    """
    Serializer for the Milk model.

    Fields:
    - `milking_date`: A date field representing the date of milking.
    - `cow`: A nested serializer field representing the cow associated with the milk record.
    - `amount_in_kgs`: A decimal field representing the amount of milk produced in kilograms.
    - `lactation`: A nested serializer field representing the associated lactation record.

    Meta:
    - `model`: The Milk model for which the serializer is defined.
    - `fields`: The fields to include in the serialized representation.

    Usage:
        Use this serializer to convert Milk model instances to JSON representations
        and vice versa.

    Example:
        ```
        class Milk(models.Model):
            milking_date = models.DateField()
            cow = models.ForeignKey(Cow, on_delete=models.CASCADE)
            amount_in_kgs = models.DecimalField(max_digits=5, decimal_places=2)
            lactation = models.ForeignKey(Lactation, on_delete=models.CASCADE)

        class MilkSerializer(serializers.ModelSerializer):
            class Meta:
                model = Milk
                fields = ("milking_date", "cow", "amount_in_kgs", "lactation")
        ```
    """

    class Meta:
        model = Milk
        fields = ("milking_date", "cow", "amount_in_kgs", "lactation")
