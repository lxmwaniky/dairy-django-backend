from django_filters import rest_framework as filters

from production.models import Lactation, Milk


class LactationFilterSet(filters.FilterSet):
    """
    Filter set for querying Lactation instances based on specific criteria.

    Filters:
    - `start_date`: A filter for the start date of the lactation.
    - `year`: An exact match filter for the year of the lactation start date.
    - `month`: An exact match filter for the month of the lactation start date.
    - `lactation_number`: An exact match filter for the lactation number.

    Meta:
    - `model`: The Lactation model for which the filter set is defined.
    - `fields`: The fields available for filtering, including 'start_date', 'year', 'month', and 'lactation_number'.

    Usage:
        Use this filter set to apply filters when querying the list of Lactation instances.
        For example, to retrieve all lactations starting in a specific year.

    Example:
        ```
        /api/lactations/?year=2022
        ```
    """

    start_date = filters.DateFilter(field_name="start_date")
    year = filters.NumberFilter(field_name="start_date__year", lookup_expr="exact")
    month = filters.NumberFilter(field_name="start_date__month", lookup_expr="exact")
    lactation_number = filters.NumberFilter(
        field_name="lactation_number", lookup_expr="exact"
    )

    class Meta:
        model = Lactation
        fields = ["start_date", "year", "month", "lactation_number"]


class MilkFilterSet(filters.FilterSet):
    """
    Filter set for querying Milk instances based on specific criteria.

    Filters:
    - `cow`: A filter for the cow associated with the milk record (case-insensitive contains search).
    - `milking_date`: A filter for the date and time of milking.
    - `day_of_milking`: An exact match filter for the day of the milking date.
    - `week_of_milking`: An exact match filter for the week of the milking date.
    - `month_of_milking`: An exact match filter for the month of the milking date.
    - `year_of_milking`: An exact match filter for the year of the milking date.

    Meta:
    - `model`: The Milk model for which the filter set is defined.
    - `fields`: The fields available for filtering, including 'cow', 'milking_date', 'day_of_milking', 'week_of_milking', 'month_of_milking', and 'year_of_milking'.

    Usage:
        Use this filter set to apply filters when querying the list of Milk instances.
        For example, to retrieve all milk records for a specific cow.

    Example:
        ```
        /api/milk/?cow=123
        ```
    """

    cow = filters.CharFilter(field_name="cow", lookup_expr="icontains")
    milking_date = filters.DateTimeFilter(field_name="milking_date")
    day_of_milking = filters.NumberFilter(
        field_name="milking_date__day", lookup_expr="exact"
    )
    week_of_milking = filters.NumberFilter(
        field_name="milking_date__week", lookup_expr="exact"
    )
    month_of_milking = filters.NumberFilter(
        field_name="milking_date__month", lookup_expr="exact"
    )
    year_of_milking = filters.NumberFilter(
        field_name="milking_date__year", lookup_expr="exact"
    )

    class Meta:
        model = Milk
        fields = [
            "cow",
            "milking_date",
            "day_of_milking",
            "week_of_milking",
            "month_of_milking",
            "year_of_milking",
        ]
