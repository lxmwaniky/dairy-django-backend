from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from users.models import CustomUser
from users.permissions import (
    IsFarmOwner,
    IsFarmManager,
    IsSelfProfile,
    IsAssistantFarmManager,
)
from users.serializers import CustomUserSerializer, CustomUserCreateSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    """
    ViewSet to handle operations related to custom user accounts.

    Provides CRUD functionality for user accounts.

    Actions:
    - list: Get a list of all custom users excluding the current user.
    - retrieve: Retrieve details of a specific custom user.
    - create: Create a new custom user account.
    - update: Update an existing custom user account.
    - destroy: Delete an existing custom user account.
    - assign_farm_owner: Assign the farm owner role to selected users.
    - assign_farm_manager: Assign the farm manager role to selected users.
    - assign_assistant_farm_manager: Assign the assistant farm manager role to selected users.
    - assign_farm_worker: Assign the farm worker role to selected users.
    - assign_team_leader_manager: Assign the team leader role to selected users.
    - dismiss_assistant_farm_manager: Dismiss the assistant farm manager role from selected users.
    - dismiss_farm_manager: Dismiss the farm manager role from selected users.
    - dismiss_farm_worker: Dismiss the farm worker role from selected users.
    - dismiss_team_leader_manager: Dismiss the team leader role from selected users.

    Serializer class used for request/response data depends on the action:
    - CustomUserCreateSerializer for the 'create' action.
    - CustomUserSerializer for other actions.
    """

    def get_queryset(self):
        """
        Get the queryset for the view.
        Exclude the current user from the list if the action is 'list'.
        """
        queryset = CustomUser.objects.all()

        if self.action == "list":
            # Exclude the current user from the list
            queryset = queryset.exclude(id=self.request.user.id)
        return queryset

    def get_serializer_class(self):
        """
        Get the serializer class based on the action.
        Use CustomUserCreateSerializer for the 'create' action, and CustomUserSerializer for other actions.
        """
        if self.action == "create":
            return CustomUserCreateSerializer
        return CustomUserSerializer

    def get_permissions(self):
        """
        Get the permissions based on the action.

        - For 'list', 'retrieve', 'destroy': Only farm owners or farm managers are allowed.
        - For 'update': Only the owner of the profile is allowed.
        - For 'assign_farm_owner', 'assign_farm_manager', 'assign_assistant_farm_manager': Only farm owners are allowed.
        - For 'assign_farm_worker': Only farm managers or owners are allowed.
        - For 'assign_team_leader': Only farm managers, owners, or assistant farm managers are allowed.
        - For 'dismiss_farm_manager', 'dismiss_assistant_farm_manager': Only farm owners are allowed.
        - For 'dismiss_team_leader': Farm owners, managers, and assistant farm managers are allowed.
        - For 'dismiss_farm_worker': Only farm managers or owners are allowed.

        """
        global permission_classes
        if self.action in ["list", "retrieve", "destroy"]:
            permission_classes = [IsFarmOwner | IsFarmManager]
        elif self.action == "update":
            permission_classes = [IsSelfProfile]
        elif self.action in [
            "assign_farm_owner",
            "assign_farm_manager",
            "assign_assistant_farm_manager",
        ]:
            permission_classes = [IsFarmOwner]
        elif self.action == "assign_farm_worker":
            permission_classes = [IsFarmManager | IsFarmOwner]
        elif self.action == "assign_team_leader":
            permission_classes = [IsFarmManager | IsFarmOwner | IsAssistantFarmManager]
        elif self.action in ["dismiss_farm_manager", "dismiss_assistant_farm_manager"]:
            permission_classes = [IsFarmOwner]
        elif self.action == "dismiss_team_leader":
            permission_classes = [IsFarmManager | IsFarmOwner | IsAssistantFarmManager]
        elif self.action == "dismiss_farm_worker":
            permission_classes = [IsFarmManager | IsFarmOwner]

        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["post"])
    def assign_farm_owner(self, request):
        """
        Assign the farm owner to selected users.

        Only authenticated users with farm owner permission can access this action.

        The action accepts a POST request with a list of user IDs in the request body
        and assigns the farm owner role to the corresponding users.

        If successful, it returns a response with a message indicating the users
        who have been assigned the farm owner role. If any user ID is not found or
        is invalid, appropriate error messages are returned in the response.
        """

        user_ids = request.data.getlist("user_ids", [])
        current_user_id = request.user.id

        assigned_users = []
        not_found_ids = []
        invalid_ids = []

        for user_id in user_ids:
            try:
                user_id_int = int(user_id)
                user = CustomUser.objects.get(id=user_id_int)

                if user.id == current_user_id:
                    raise ValidationError("Cannot assign roles to yourself.")

                user.assign_farm_owner()
                assigned_users.append(user.username)

            except (ValueError, CustomUser.DoesNotExist):
                if user_id.isdigit():
                    not_found_ids.append(user_id)
                else:
                    invalid_ids.append(user_id)

        response_data = {}

        if assigned_users:
            if len(assigned_users) > 1:
                response_data[
                    "message"
                ] = f"Users {', '.join(assigned_users)} have been assigned as farm owners."
            else:
                response_data[
                    "message"
                ] = f"User {assigned_users[0]} has been assigned as a farm owner."

        if not_found_ids:
            if len(not_found_ids) > 1:
                response_data[
                    "error"
                ] = f"Users with the following IDs were not found: {', '.join(not_found_ids)}."
            else:
                response_data[
                    "error"
                ] = f"User with ID {not_found_ids[0]} was not found."

        if invalid_ids:
            if len(invalid_ids) > 1:
                response_data[
                    "invalid"
                ] = f"The following IDs are invalid: {', '.join(invalid_ids)}."
            else:
                response_data["invalid"] = f"The ID {invalid_ids[0]} is invalid."

        return Response(response_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def assign_farm_manager(self, request):
        """
        Assign the farm manager to selected users.

        Only authenticated users with farm owner permission can access this action.

        The view accepts a POST request with a list of user IDs in the request body
        and assigns the farm manager role to the corresponding users.

        If successful, it returns a response with a message indicating the users
        who have been assigned the farm manager role. If any user ID is not found
        or is invalid, appropriate error messages are returned in the response.

        """

        user_ids = request.data.getlist("user_ids", [])
        current_user_id = request.user.id

        assigned_users = []
        not_found_ids = []
        invalid_ids = []

        for user_id in user_ids:
            try:
                user_id_int = int(user_id)
                user = CustomUser.objects.get(id=user_id_int)

                if user.id == current_user_id:
                    raise ValidationError("Cannot assign roles to yourself.")

                user.assign_farm_manager()
                assigned_users.append(user.username)

            except (ValueError, CustomUser.DoesNotExist):
                if user_id.isdigit():
                    not_found_ids.append(user_id)
                else:
                    invalid_ids.append(user_id)

        response_data = {}

        if assigned_users:
            if len(assigned_users) > 1:
                response_data[
                    "message"
                ] = f"Users {', '.join(assigned_users)} have been assigned as farm managers."
            else:
                response_data[
                    "message"
                ] = f"User {assigned_users[0]} has been assigned as a farm manager."

        if not_found_ids:
            if len(not_found_ids) > 1:
                response_data[
                    "error"
                ] = f"Users with the following IDs were not found: {', '.join(not_found_ids)}."
            else:
                response_data[
                    "error"
                ] = f"User with ID '{not_found_ids[0]}' was not found."

        if invalid_ids:
            if len(invalid_ids) > 1:
                response_data[
                    "invalid"
                ] = f"The following IDs are invalid: {', '.join(invalid_ids)}."
            else:
                response_data["invalid"] = f"The ID '{invalid_ids[0]}' is invalid."

        return Response(response_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def assign_assistant_farm_manager(self, request):
        """
        Assign the assistant farm manager to selected users.

        Only authenticated users with farm owner permission can access this action.

        The view accepts a POST request with a list of user IDs in the request body
        and assigns the assistant farm manager role to the corresponding users.

        If successful, it returns a response with a message indicating the users
        who have been assigned the assistant farm manager role. If any user ID is not found
        or is invalid, appropriate error messages are returned in the response.

        """

        user_ids = request.data.getlist("user_ids", [])
        current_user_id = request.user.id

        assigned_users = []
        not_found_ids = []
        invalid_ids = []

        for user_id in user_ids:
            try:
                user_id_int = int(user_id)
                user = CustomUser.objects.get(id=user_id_int)

                if user.id == current_user_id:
                    raise ValidationError("Cannot assign roles to yourself.")

                user.assign_assistant_farm_manager()
                assigned_users.append(user.username)

            except (ValueError, CustomUser.DoesNotExist):
                if user_id.isdigit():
                    not_found_ids.append(user_id)
                else:
                    invalid_ids.append(user_id)

        response_data = {}

        if assigned_users:
            if len(assigned_users) > 1:
                response_data[
                    "message"
                ] = f"Users {', '.join(assigned_users)} have been assigned as assistant farm managers."
            else:
                response_data[
                    "message"
                ] = f"User {assigned_users[0]} has been assigned as an assistant farm manager."

        if not_found_ids:
            if len(not_found_ids) > 1:
                response_data[
                    "error"
                ] = f"Users with the following IDs were not found: {', '.join(not_found_ids)}."
            else:
                response_data[
                    "error"
                ] = f"User with ID {not_found_ids[0]} was not found."

        if invalid_ids:
            if len(invalid_ids) > 1:
                response_data[
                    "invalid"
                ] = f"The following IDs are invalid: {', '.join(invalid_ids)}."
            else:
                response_data["invalid"] = f"The ID {invalid_ids[0]} is invalid."

        return Response(response_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def assign_team_leader(self, request):
        """
        Assign the team leader to selected users.

        Only authenticated users with assistant farm manager permission can access this action.

        The view accepts a POST request with a list of user IDs in the request body
        and assigns the team leader role to the corresponding users.

        If successful, it returns a response with a message indicating the users
        who have been assigned the team leader role. If any user ID is not found
        or is invalid, appropriate error messages are returned in the response.

        """

        user_ids = request.data.getlist("user_ids", [])
        current_user_id = request.user.id

        assigned_users = []
        not_found_ids = []
        invalid_ids = []

        for user_id in user_ids:
            try:
                user_id_int = int(user_id)
                user = CustomUser.objects.get(id=user_id_int)

                if user.id == current_user_id:
                    raise ValidationError("Cannot assign roles to yourself.")

                user.assign_team_leader()
                assigned_users.append(user.username)

            except (ValueError, CustomUser.DoesNotExist):
                if user_id.isdigit():
                    not_found_ids.append(user_id)
                else:
                    invalid_ids.append(user_id)

        response_data = {}

        if assigned_users:
            if len(assigned_users) > 1:
                response_data[
                    "message"
                ] = f"Users {', '.join(assigned_users)} have been assigned as team leaders."
            else:
                response_data[
                    "message"
                ] = f"User {assigned_users[0]} has been assigned as a team leader."

        if not_found_ids:
            if len(not_found_ids) > 1:
                response_data[
                    "error"
                ] = f"Users with the following IDs were not found: {', '.join(not_found_ids)}."
            else:
                response_data[
                    "error"
                ] = f"User with ID '{not_found_ids[0]}' was not found."

        if invalid_ids:
            if len(invalid_ids) > 1:
                response_data[
                    "invalid"
                ] = f"The following IDs are invalid: {', '.join(invalid_ids)}."
            else:
                response_data["invalid"] = f"The ID '{invalid_ids[0]}' is invalid."

        return Response(response_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def assign_farm_worker(self, request):
        """
        Assign the farm worker to selected users.

        Only authenticated users with farm manager permission can access this action.

        The view accepts a POST request with a list of user IDs in the request body
        and assigns the farm worker role to the corresponding users.

        If successful, it returns a response with a message indicating the users
        who have been assigned the farm worker role. If any user ID is not found
        or is invalid, appropriate error messages are returned in the response.

        """

        user_ids = request.data.getlist("user_ids", [])
        current_user_id = request.user.id

        assigned_users = []
        not_found_ids = []
        invalid_ids = []

        for user_id in user_ids:
            try:
                user_id_int = int(user_id)
                user = CustomUser.objects.get(id=user_id_int)

                if user.id == current_user_id:
                    raise ValidationError("Cannot assign roles to yourself.")

                user.assign_farm_worker()
                assigned_users.append(user.username)

            except (ValueError, CustomUser.DoesNotExist):
                if user_id.isdigit():
                    not_found_ids.append(user_id)
                else:
                    invalid_ids.append(user_id)

        response_data = {}

        if assigned_users:
            if len(assigned_users) > 1:
                response_data[
                    "message"
                ] = f"Users {', '.join(assigned_users)} have been assigned as farm workers."
            else:
                response_data[
                    "message"
                ] = f"User {assigned_users[0]} has been assigned as a farm worker."

        if not_found_ids:
            if len(not_found_ids) > 1:
                response_data[
                    "error"
                ] = f"Users with the following IDs were not found: {', '.join(not_found_ids)}."
            else:
                response_data[
                    "error"
                ] = f"User with ID {not_found_ids[0]} was not found."

        if invalid_ids:
            if len(invalid_ids) > 1:
                response_data[
                    "invalid"
                ] = f"The following IDs are invalid: {', '.join(invalid_ids)}."
            else:
                response_data["invalid"] = f"The ID {invalid_ids[0]} is invalid."

        return Response(response_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def dismiss_farm_manager(self, request):
        """
        Dismiss the farm manager from selected users.

        Only authenticated users with farm owner permission can access this action.

        The view accepts a POST request with a list of user IDs in the request body
        and dismisses the farm manager role from the corresponding users.

        If successful, it returns a response with a message indicating the users
        who have been dismissed from the farm manager role. If any user ID is not found
        or is invalid, appropriate error messages are returned in the response.

        """

        user_ids = request.data.getlist("user_ids", [])
        current_user_id = request.user.id

        dismissed_users = []
        not_found_ids = []
        invalid_ids = []

        for user_id in user_ids:
            try:
                user_id_int = int(user_id)
                user = CustomUser.objects.get(id=user_id_int)

                if user.id == current_user_id:
                    raise ValidationError("Cannot dismiss yourself.")

                user.dismiss_farm_manager()
                dismissed_users.append(user.username)

            except (ValueError, CustomUser.DoesNotExist):
                if user_id.isdigit():
                    not_found_ids.append(user_id)
                else:
                    invalid_ids.append(user_id)

        response_data = {}

        if dismissed_users:
            if len(dismissed_users) > 1:
                response_data[
                    "message"
                ] = f"Users {', '.join(dismissed_users)} have been dismissed as farm managers."
            else:
                response_data[
                    "message"
                ] = f"User {dismissed_users[0]} has been dismissed as a farm manager."

        if not_found_ids:
            if len(not_found_ids) > 1:
                response_data[
                    "error"
                ] = f"Users with the following IDs were not found: {', '.join(not_found_ids)}."
            else:
                response_data[
                    "error"
                ] = f"User with ID '{not_found_ids[0]}' was not found."

        if invalid_ids:
            if len(invalid_ids) > 1:
                response_data[
                    "invalid"
                ] = f"The following IDs are invalid: {', '.join(invalid_ids)}."
            else:
                response_data["invalid"] = f"The ID '{invalid_ids[0]}' is invalid."

        return Response(response_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def dismiss_assistant_farm_manager(self, request):
        """
        Dismiss the assistant farm manager from selected users.

        Only authenticated users with farm owner permission can access this action.

        The view accepts a POST request with a list of user IDs in the request body
        and dismisses the assistant farm manager role from the corresponding users.

        If successful, it returns a response with a message indicating the users
        who have been dismissed from the assistant farm manager role. If any user ID is not found
        or is invalid, appropriate error messages are returned in the response.

        """

        user_ids = request.data.getlist("user_ids", [])
        current_user_id = request.user.id

        dismissed_users = []
        not_found_ids = []
        invalid_ids = []

        for user_id in user_ids:
            try:
                user_id_int = int(user_id)
                user = CustomUser.objects.get(id=user_id_int)

                if user.id == current_user_id:
                    raise ValidationError("Cannot dismiss yourself.")

                user.dismiss_assistant_farm_manager()
                dismissed_users.append(user.username)

            except (ValueError, CustomUser.DoesNotExist):
                if user_id.isdigit():
                    not_found_ids.append(user_id)
                else:
                    invalid_ids.append(user_id)

        response_data = {}

        if dismissed_users:
            if len(dismissed_users) > 1:
                response_data[
                    "message"
                ] = f"Users {', '.join(dismissed_users)} have been dismissed as assistant farm managers."
            else:
                response_data[
                    "message"
                ] = f"User {dismissed_users[0]} has been dismissed as an assistant farm manager."

        if not_found_ids:
            if len(not_found_ids) > 1:
                response_data[
                    "error"
                ] = f"Users with the following IDs were not found: {', '.join(not_found_ids)}."
            else:
                response_data[
                    "error"
                ] = f"User with ID {not_found_ids[0]} was not found."

        if invalid_ids:
            if len(invalid_ids) > 1:
                response_data[
                    "invalid"
                ] = f"The following IDs are invalid: {', '.join(invalid_ids)}."
            else:
                response_data["invalid"] = f"The ID {invalid_ids[0]} is invalid."

        return Response(response_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def dismiss_team_leader(self, request):
        """
        Dismiss the team leader from selected users.

        Only authenticated users with assistant farm manager permission can access this action.

        The view accepts a POST request with a list of user IDs in the request body
        and dismisses the team leader role from the corresponding users.

        If successful, it returns a response with a message indicating the users
        who have been dismissed from the team leader role. If any user ID is not found
        or is invalid, appropriate error messages are returned in the response.

        """
        user_ids = request.data.getlist("user_ids", [])
        current_user_id = request.user.id

        dismissed_users = []
        not_found_ids = []
        invalid_ids = []

        for user_id in user_ids:
            try:
                try:
                    user_id_int = int(user_id)
                except ValueError:
                    invalid_ids.append(user_id)
                    continue

                user = CustomUser.objects.get(id=user_id_int)

                if user.id == current_user_id:
                    raise ValidationError("Cannot dismiss yourself.")

                user.dismiss_team_leader()
                dismissed_users.append(user.username)

            except (ValueError, CustomUser.DoesNotExist):
                if user_id.isdigit():
                    not_found_ids.append(user_id)
                else:
                    invalid_ids.append(user_id)

        response_data = {}

        if dismissed_users:
            if len(dismissed_users) > 1:
                response_data[
                    "message"
                ] = f"Users {', '.join(dismissed_users)} have been dismissed as team leaders."
            else:
                response_data[
                    "message"
                ] = f"User {dismissed_users[0]} has been dismissed as a team leader."

        if not_found_ids:
            if len(not_found_ids) > 1:
                response_data[
                    "error"
                ] = f"Users with the following IDs were not found: {', '.join(not_found_ids)}."
            else:
                response_data[
                    "error"
                ] = f"User with ID '{not_found_ids[0]}' was not found."

        if invalid_ids:
            if len(invalid_ids) > 1:
                response_data[
                    "invalid"
                ] = f"The following IDs are invalid: {', '.join(invalid_ids)}."
            else:
                response_data["invalid"] = f"The ID '{invalid_ids[0]}' is invalid."

        return Response(response_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def dismiss_farm_worker(self, request):
        """
        Dismiss the farm worker from selected users.

        Only authenticated users with farm manager permission or higher can access this view.

        The view accepts a POST request with a list of user IDs in the request body
        and dismisses the farm worker role from the corresponding users.

        If successful, it returns a response with a message indicating the users
        who have been dismissed from the farm worker role. If any user ID is not found
        or is invalid, appropriate error messages are returned in the response.

        """

        user_ids = request.data.getlist("user_ids", [])
        current_user_id = request.user.id

        dismissed_users = []
        not_found_ids = []
        invalid_ids = []

        for user_id in user_ids:
            try:
                user_id_int = int(user_id)
                user = CustomUser.objects.get(id=user_id_int)

                if user.id == current_user_id:
                    raise ValidationError("Cannot dismiss yourself.")

                user.dismiss_farm_worker()
                dismissed_users.append(user.username)

            except (ValueError, CustomUser.DoesNotExist):
                if user_id.isdigit():
                    not_found_ids.append(user_id)
                else:
                    invalid_ids.append(user_id)

        response_data = {}

        if dismissed_users:
            if len(dismissed_users) > 1:
                response_data[
                    "message"
                ] = f"Users {', '.join(dismissed_users)} have been dismissed as farm workers."
            else:
                response_data[
                    "message"
                ] = f"User {dismissed_users[0]} has been dismissed as a farm worker."

        if not_found_ids:
            if len(not_found_ids) > 1:
                response_data[
                    "error"
                ] = f"Users with the following IDs were not found: {', '.join(not_found_ids)}."
            else:
                response_data[
                    "error"
                ] = f"User with ID {not_found_ids[0]} was not found."

        if invalid_ids:
            if len(invalid_ids) > 1:
                response_data[
                    "invalid"
                ] = f"The following IDs are invalid: {', '.join(invalid_ids)}."
            else:
                response_data["invalid"] = f"The ID {invalid_ids[0]} is invalid."

        return Response(response_data, status=status.HTTP_200_OK)
