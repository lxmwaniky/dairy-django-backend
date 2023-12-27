from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from reproduction.filters import PregnancyFilterSet
from reproduction.models import Pregnancy
from reproduction.serializers import PregnancySerializer
from users.permissions import IsFarmManager, IsFarmOwner, IsFarmWorker, IsAssistantFarmManager, IsTeamLeader


class PregnancyViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle operations related to pregnancy records.

    Provides CRUD functionality for pregnancy records.

    Actions:
    - list: Get a list of pregnancy records based on applied filters.
           Returns a 404 response if no pregnancy records match the provided filters,
           and a 200 response with an empty list if there are no pregnancy records in the database.
    - retrieve: Retrieve details of a specific pregnancy record.
    - create: Create a new pregnancy record.
    - update: Update an existing pregnancy record.
    - partial_update: Partially update an existing pregnancy record.
    - destroy: Delete an existing pregnancy record.

    Serializer class used for request/response data: PregnancySerializer.

    Permissions:
    - For 'list', 'retrieve': Accessible to all users (farm workers, team leaders, assistant farm managers, farm managers, farm owners).
    - For 'create', 'update', 'partial_update', 'destroy': Accessible to farm managers and farm owners only.

    """

    queryset = Pregnancy.objects.all()
    serializer_class = PregnancySerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PregnancyFilterSet
    ordering_fields = ["-start_date"]

    def get_permissions(self):
        """
        Get the permissions based on the action.

        - For 'create', 'update', 'partial_update', 'destroy':
          Only farm managers or farm owners are allowed.
        - For other actions, accessible to farm workers, team leaders, assistant farm managers,
          farm managers, and farm owners.

        """
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsFarmManager | IsFarmOwner]
        else:
            permission_classes = [IsFarmWorker | IsTeamLeader | IsAssistantFarmManager | IsFarmManager | IsFarmOwner]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        """
        List pregnancy records based on applied filters.

        Returns a 404 response if no pregnancy records match the provided filters,
        and a 200 response with an empty list if there are no pregnancy records in the database.

        """
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            if request.query_params:
                # If query parameters are provided, but there are no matching pregnancy records
                return Response(
                    {
                        "detail": "No Pregnancy record(s) found matching the provided filters."
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            else:
                # If no query parameters are provided, and there are no pregnancy records in the database
                return Response(
                    {"detail": "No Pregnancy records found."},
                    status=status.HTTP_200_OK
                )

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
