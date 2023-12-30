from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.exceptions import MethodNotAllowed, PermissionDenied
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from production.filters import LactationFilterSet, MilkFilterSet
from production.models import Lactation, Milk
from production.serializers import LactationSerializer, MilkSerializer
from users.permissions import (
    IsFarmManager,
    IsFarmOwner,
    IsAssistantFarmManager,
    IsFarmWorker,
)


class LactationViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle operations related to lactation records.

    Provides CRUD functionality for lactation records.

    Actions:
    - list: Get a list of lactation records based on applied filters.
           Returns a 404 response if no lactation records match the provided filters,
           and a 200 response with an empty list if there are no lactation records in the database.
    - retrieve: Retrieve details of a specific lactation record.
    - create: Create a new lactation record.
    - update: Not allowed. Raises a MethodNotAllowed exception for PUT requests.
    - partial_update: Not allowed. Raises a MethodNotAllowed exception for PATCH requests.
    - destroy: Delete an existing lactation record, but not allowed if associated with a pregnancy.

    Serializer class used for request/response data: LactationSerializer.

    Permissions:
    - For 'list', 'retrieve': Accessible to all users (farm workers, assistant farm managers, farm managers, farm owners).
    - For 'create', 'destroy': Accessible to farm managers and farm owners only.

    Note: Updating and partial updating lactation records using PUT and PATCH methods are not allowed.

    """

    serializer_class = LactationSerializer
    queryset = Lactation.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = LactationFilterSet
    ordering_fields = ["start_date"]

    def get_permissions(self):
        """
        Get the permissions based on the action.

        - For 'create', 'destroy':
          Only farm managers or farm owners are allowed.
        - For other actions, accessible to farm workers, assistant farm managers,
          farm managers, and farm owners.

        """
        if self.action in ["create", "destroy"]:
            permission_classes = [IsFarmManager | IsFarmOwner]
        else:
            permission_classes = [
                IsFarmWorker | IsAssistantFarmManager | IsFarmManager | IsFarmOwner
            ]
        return [permission() for permission in permission_classes]

    def update(self, request, *args, **kwargs):
        """
        Not allowed. Raises a MethodNotAllowed exception for PUT requests.

        """
        raise MethodNotAllowed("PUT")

    def partial_update(self, request, *args, **kwargs):
        """
        Not allowed. Raises a MethodNotAllowed exception for PATCH requests.

        """
        raise MethodNotAllowed("PATCH")

    def destroy(self, request, *args, **kwargs):
        """
        Delete an existing lactation record, but not allowed if associated with a pregnancy.

        """
        instance = self.get_object()

        # Check if the lactation record is associated with a pregnancy
        if instance.pregnancy:
            raise PermissionDenied(
                "Deletion not allowed. Lactation record is associated with a pregnancy."
            )

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        """
        List lactation records based on applied filters.

        Returns a 404 response if no lactation records match the provided filters,
        and a 200 response with an empty list if there are no lactation records in the database.

        """
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            if request.query_params:
                # If query parameters are provided, but there are no matching lactation records
                return Response(
                    {
                        "detail": "No Lactation record(s) found matching the provided filters."
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            else:
                # If no query parameters are provided, and there are no lactation records in the database
                return Response(
                    {"detail": "No Lactation records found."}, status=status.HTTP_200_OK
                )

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class MilkViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle operations related to milk records.

    Provides CRUD functionality for milk records.

    Actions:
    - list: Get a list of milk records based on applied filters.
           Returns a 404 response if no milk records match the provided filters,
           and a 200 response with an empty list if there are no milk records in the database.
    - retrieve: Retrieve details of a specific milk record.
    - create: Create a new milk record.
    - update: Update an existing milk record.
    - partial_update: Partially update an existing milk record.
    - destroy: Delete an existing milk record.

    Serializer class used for request/response data: MilkSerializer.

    Permissions:
    - For 'list', 'retrieve': Accessible to farm managers and farm owners only.
    - For 'create': Accessible to farm workers, assistant farm managers, farm managers, and farm owners.
    - For 'update', 'partial_update', 'destroy': Accessible to farm managers and farm owners only.


    """

    serializer_class = MilkSerializer
    queryset = Milk.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = MilkFilterSet
    ordering_fields = ["-milking_date"]

    def get_permissions(self):
        """
        Get the permissions based on the action.

        - For 'create':
          Accessible to farm workers, assistant farm managers, farm managers, and farm owners.
        - For 'update', 'partial_update', 'destroy':
          Only farm managers or farm owners are allowed.
        - For 'list', 'retrieve':
          Accessible to farm managers and farm owners only.

        """
        if self.action == "create":
            permission_classes = [
                IsFarmWorker | IsAssistantFarmManager | IsFarmManager | IsFarmOwner
            ]
        else:
            permission_classes = [IsFarmManager | IsFarmOwner]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        """
        List milk records based on applied filters.

        Returns a 404 response if no milk records match the provided filters,
        and a 200 response with an empty list if there are no milk records in the database.

        """
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            if request.query_params:
                # If query parameters are provided, but there are no matching milk records
                return Response(
                    {
                        "detail": "No Milk record(s) found matching the provided filters."
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
            else:
                # If no query parameters are provided, and there are no milk records in the database
                return Response(
                    {"detail": "No Milk records found."}, status=status.HTTP_200_OK
                )

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
