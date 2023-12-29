from django_filters import rest_framework as filters

from production.models import Lactation


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

