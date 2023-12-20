from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from rest_framework.permissions import BasePermission


class IsSelfProfile(BasePermission):
    """
    Custom permission class that allows actions only if the user is the owner of the profile.

    Raises:
    - `PermissionDenied`: If the user is not the owner of the profile.

    Usage:
        Add the permission class to the view or viewset that requires access to the user's own profile:
        permission_classes = [IsSelfProfile]
    """

    message = {
        "error": "You do not have permission to perform this action on another user's profile."
    }

    def has_object_permission(self, request, view, obj):
        # Check if the current user is the owner of the profile
        return obj == request.user


class IsFarmOwner(BasePermission):
    """
    Custom permission class that allows only farm owners to perform an action.

    Raises:
    - `PermissionDenied`: If the user is not a farm owner.

    Usage:
        Add the permission class to the view or viewset that requires farm owners access:
        permission_classes = [IsFarmOwner]
    """

    message = {"error": "Only farm owners have permission to perform this action."}

    def has_permission(self, request, view):
        # Check if the current user is a farm owner
        if request.user.is_authenticated and request.user.is_farm_owner:
            return True
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                {"error": "Authentication credentials were not provided! Please login to proceed."}
            )
        raise PermissionDenied(self.message)


class IsFarmManager(BasePermission):
    """
    Custom permission class that allows only farm owners and managers to perform an action.

    Raises:
    - `PermissionDenied`: If the user is not a farm owner or a farm manager.

    Usage:
        Add the permission class to the view or viewset that requires farm owners and managers access:
        permission_classes = [IsFarmManager]
    """

    message = {
        "error": "Only farm owners and managers have permission to perform this action."
    }

    def has_permission(self, request, view):
        # Check if the current user is a farm manager
        if request.user.is_authenticated and (
                request.user.is_farm_manager or request.user.is_farm_owner
        ):
            return True
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                {"error": "Authentication credentials were not provided! Please login to proceed."}
            )
        raise PermissionDenied(self.message)


class IsAssistantFarmManager(BasePermission):
    """
    Custom permission class that allows only farm owners, managers, and assistants to perform an action.

    Raises:
    - `PermissionDenied`: If the user is not a farm owner, a farm manager, or an assistant farm manager.

    Usage:
        Add the permission class to the view or viewset that requires farm owners, managers, and assistants access:
        permission_classes = [IsAssistantFarmManager]
    """

    message = {
        "error": "Only farm owners, managers, and assistants have permission to perform this action."
    }

    def has_permission(self, request, view):
        # Check if the current user is an assistant farm manager
        if request.user.is_authenticated and (
                request.user.is_assistant_farm_manager
                or request.user.is_farm_manager
                or request.user.is_farm_owner
        ):
            return True
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                {"error": "Authentication credentials were not provided! Please login to proceed."}
            )
        raise PermissionDenied(self.message)


class IsTeamLeader(BasePermission):
    """
    Custom permission class that allows only team leaders to perform an action.

    Raises:
    - `PermissionDenied`: If the user is not a team leader, an assistant farm manager, a farm manager, or a farm owner.

    Usage:
        Add the permission class to the view or viewset that requires team leaders access:
        permission_classes = [IsTeamLeader]
    """

    message = {"error": "Only team leaders have permission to perform this action."}

    def has_permission(self, request, view):
        # Check if the current user is a team leader
        if request.user.is_authenticated and (
                request.user.is_team_leader
                or request.user.is_assistant_farm_manager
                or request.user.is_farm_manager
                or request.user.is_farm_owner
        ):
            return True
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                {"error": "Authentication credentials were not provided! Please login to proceed."}
            )
        raise PermissionDenied(self.message)


class IsFarmWorker(BasePermission):
    """
    Custom permission class that allows only farm staff and workers to perform an action.

    Raises:
    - `PermissionDenied`: If the user is not a farm owner, a farm worker, a farm manager, or an assistant farm manager.

    Usage:
        Add the permission class to the view or viewset that requires farm workers access:
        permission_classes = [IsFarmWorker]
    """

    message = {
        "error": "Only farm staff and workers have permission to perform this action."
    }

    def has_permission(self, request, view):
        # Check if the current user is a farm worker
        if request.user.is_authenticated and (
                request.user.is_farm_owner
                or request.user.is_farm_worker
                or request.user.is_farm_manager
                or request.user.is_assistant_farm_manager
        ):
            return True
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                {"error": "Authentication credentials were not provided! Please login to proceed."}
            )
        raise PermissionDenied(self.message)
