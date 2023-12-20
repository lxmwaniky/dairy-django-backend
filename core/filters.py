from django_filters import rest_framework as filters

from core.models import CowBreed


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
