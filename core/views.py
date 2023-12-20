from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from core.filters import CowBreedFilterSet
from core.models import CowBreed
from core.serializers import CowBreedSerializer
from users.permissions import (
    IsFarmOwner,
    IsFarmManager,
    IsAssistantFarmManager,
    IsFarmWorker,
)


class CowBreedViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle operations related to cow breeds.

    Provides CRUD functionality for cow breeds.

    Actions:
    - list: Get a list of cow breeds based on applied filters.
           Returns a 404 response if no cow breeds match the provided filters,
           and a 200 response with an empty list if there are no cow breeds in the database.
    - retrieve: Retrieve details of a specific cow breed.
    - create: Create a new cow breed.
    - update: Update an existing cow breed.
    - partial_update: Partially update an existing cow breed.
    - destroy: Delete an existing cow breed.

    Serializer class used for request/response data: CowBreedSerializer.

    Permissions:
    - For 'list', 'retrieve': Accessible to all users (farm workers, assistant farm managers, farm managers, farm owners).
    - For 'create', 'destroy', 'update', 'partial_update': Accessible to farm managers and farm owners only.

    """

    queryset = CowBreed.objects.all()
    serializer_class = CowBreedSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CowBreedFilterSet
    ordering_fields = ["name"]

    def get_permissions(self):
        """
        Get the permissions based on the action.

        - For 'create', 'destroy', 'update', 'partial_update':
          Only farm managers or farm owners are allowed.
        - For other actions, accessible to farm workers, assistant farm managers,
          farm managers, and farm owners.

        """
        if self.action in ["create", "destroy", "update", "partial_update"]:
            permission_classes = [IsFarmManager | IsFarmOwner]
        else:
            permission_classes = [
                IsFarmWorker | IsAssistantFarmManager | IsFarmManager | IsFarmOwner
            ]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        """
        List cow breeds based on applied filters.

        Returns a 404 response if no cow breeds match the provided filters,
        and a 200 response with an empty list if there are no cow breeds in the database.

        """
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            if request.query_params:
                # If query parameters are provided, but there are no matching cow breeds
                return Response(
                    {"detail": "No cow breed(s) found matching the provided filters."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            else:
                # If no query parameters are provided, and there are no cow breeds in the database
                return Response(
                    {"detail": "No cow breeds found in the farm yet."},
                    status=status.HTTP_200_OK,
                )

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
