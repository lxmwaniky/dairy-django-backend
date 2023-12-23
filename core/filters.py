from django_filters import rest_framework as filters

from core.models import Cow, CowBreed

class CowBreedFilterSet(filters.FilterSet):
    """
    Filter set for querying CowBreed instances based on specific criteria.

    Filters:
    - `name`: A case-insensitive partial match filter for the name of the cow breed.

    Meta:
    - `model`: The CowBreed model for which the filter set is defined.
    - `fields`: The fields available for filtering, including 'name'.

    Usage:
        Use this filter set to apply filters when querying the list of CowBreed instances.
        For example, to retrieve all cow breeds with names containing a specific substring.

    Example:
        ```
        /api/cow-breeds/?name=guernsey
        ```

    """

    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = CowBreed
        fields = ["name"]


class CaseInsensitiveBooleanFilter(filters.BooleanFilter):
    """
    Custom boolean filter that accepts case-insensitive boolean values.

    Usage:
        Use this filter to handle case-insensitive boolean values when filtering a queryset.

    Example:
        ```
        class CowFilterSet(filters.FilterSet):
            is_bought = CaseInsensitiveBooleanFilter(field_name="is_bought")
        ```
    """

    def filter(self, qs, value):
        if value in ["true", "T", "t", "1"]:
            value = True
        elif value in ["false", "F", "f", "0"]:
            value = False
        return super().filter(qs, value)


class CowFilterSet(filters.FilterSet):
    """
    Filter set for querying Cow instances based on specific criteria.

    Filters:
    - `breed`: A case-insensitive partial match filter for the name of the cow's breed.
    - `is_bought`: A case-insensitive boolean filter for the purchase status of the cow.
    - `gender`: A case-insensitive partial match filter for the gender of the cow.
    - `year_of_birth`: An exact match filter for the year of birth of the cow.
    - `month_of_birth`: An exact match filter for the month of birth of the cow.
    - `availability_status`: A case-insensitive partial match filter for the availability status of the cow.
    - `current_pregnancy_status`: A case-insensitive partial match filter for the current pregnancy status of the cow.
    - `category`: A case-insensitive partial match filter for the category of the cow.
    - `current_production_status`: A case-insensitive partial match filter for the current production status of the cow.
    - `name`: A case-insensitive partial match filter for the name of the cow.

    Meta:
    - `model`: The Cow model for which the filter set is defined.
    - `fields`: The fields available for filtering, including 'breed', 'is_bought', 'gender', 'year_of_birth',
                'month_of_birth', 'availability_status', 'current_pregnancy_status', 'category',
                'current_production_status', and 'name'.

    Usage:
        Use this filter set to apply filters when querying the list of Cow instances.
        For example, to retrieve all cows with a specific breed name.

    Example:
        ```
        /api/cows/?breed=jersey
        ```
    """

    breed = filters.CharFilter(field_name="breed__name", lookup_expr="icontains")
    is_bought = CaseInsensitiveBooleanFilter(field_name="is_bought")
    gender = filters.CharFilter(field_name="gender", lookup_expr="icontains")
    year_of_birth = filters.NumberFilter(
        field_name="date_of_birth__year", lookup_expr="exact"
    )
    month_of_birth = filters.NumberFilter(
        field_name="date_of_birth__month", lookup_expr="exact"
    )
    availability_status = filters.CharFilter(
        field_name="availability_status", lookup_expr="icontains"
    )
    current_pregnancy_status = filters.CharFilter(
        field_name="current_pregnancy_status", lookup_expr="icontains"
    )
    category = filters.CharFilter(field_name="category", lookup_expr="icontains")
    current_production_status = filters.CharFilter(
        field_name="current_production_status", lookup_expr="icontains"
    )
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Cow
        fields = [
            "breed",
            "is_bought",
            "gender",
            "year_of_birth",
            "month_of_birth",
            "availability_status",
            "current_pregnancy_status",
            "category",
            "current_production_status",
            "name",
        ]
