from django_filters import rest_framework as filters
from reproduction.models import Pregnancy, Heat


class PregnancyFilterSet(filters.FilterSet):
    """
    Filter set for querying Pregnancy instances based on specific criteria.

    Filters:
    - `cow`: A case-insensitive partial match filter for the name of the cow associated with the pregnancy.
    - `year`: An exact match filter for the year of the pregnancy start date.
    - `month`: An exact match filter for the month of the pregnancy start date.
    - `pregnancy_outcome`: A case-insensitive partial match filter for the outcome of the pregnancy.
    - `pregnancy_status`: A case-insensitive partial match filter for the status of the pregnancy.

    Meta:
    - `model`: The Pregnancy model for which the filter set is defined.
    - `fields`: The fields available for filtering, including 'cow', 'year', 'month', 'pregnancy_outcome',
                and 'pregnancy_status'.

    Usage:
        Use this filter set to apply filters when querying the list of Pregnancy instances.
        For example, to retrieve all pregnancies with a specific cow name.

    Example:
        ```
        /api/pregnancies/?cow=jersey
        ```
    """
    cow = filters.CharFilter(field_name="cow__name", lookup_expr="icontains")
    year = filters.NumberFilter(field_name="start_date__year", lookup_expr="exact")
    month = filters.NumberFilter(field_name="start_date__month", lookup_expr="exact")
    pregnancy_outcome = filters.CharFilter(field_name="pregnancy_outcome", lookup_expr="icontains")
    pregnancy_status = filters.CharFilter(field_name="pregnancy_status", lookup_expr="icontains")

    class Meta:
        model = Pregnancy
        fields = [
            "cow",
            "year",
            "month",
            "pregnancy_outcome",
            "pregnancy_status"
        ]


class HeatFilterSet(filters.FilterSet):
    """
    Filter set for querying Heat instances based on specific criteria.

    Filters:
    - `cow`: A case-insensitive partial match filter for the name of the cow associated with the heat observation.
    - `observation_time`: An exact match filter for the time of the heat observation.
    - `month`: An exact match filter for the month of the heat observation time.

    Meta:
    - `model`: The Heat model for which the filter set is defined.
    - `fields`: The fields available for filtering, including 'cow', 'observation_time', and 'month'.

    Usage:
        Use this filter set to apply filters when querying the list of Heat instances.
        For example, to retrieve all heat observations for a specific cow.

    Example:
        ```
        /api/heats/?cow=jersey
        ```
    """
    cow = filters.CharFilter(field_name="cow__name", lookup_expr="icontains")
    observation_time = filters.DateTimeFilter(
        field_name="observation_time", lookup_expr="exact"
    )
    month = filters.NumberFilter(field_name="observation_time__month", lookup_expr="exact")

    class Meta:
        model = Heat
        fields = [
            "cow",
            "month",
            "observation_time",
        ]
