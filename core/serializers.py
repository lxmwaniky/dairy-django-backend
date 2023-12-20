from rest_framework import serializers

from core.models import CowBreed


class CowBreedSerializer(serializers.ModelSerializer):
    """
    Serializer for the CowBreed model.

    Fields:
    - `name`: A CharField representing the name of the cow breed.

    Meta:
    - `model`: The CowBreed model for which the serializer is defined.
    - `fields`: The fields to include in the serialized representation.

    Usage:
        Use this serializer to convert CowBreed model instances to JSON representations
        and vice versa. It includes the 'name' field of the cow breed.

    """

    class Meta:
        model = CowBreed
        fields = ("name",)
