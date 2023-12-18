from django.urls import path, include
from djoser.views import TokenCreateView, TokenDestroyView
from rest_framework import routers

from users.views import CustomUserViewSet

# Set the app name for namespacing
app_name = "users"

router = routers.DefaultRouter()
router.register(r"users", CustomUserViewSet, basename="users")

# Add a new router for CowBreed
#cow_breed_router = routers.DefaultRouter()
#cow_breed_router.register(r"cowbreeds", CowBreedViewSet, basename="cowbreeds")

# Define URL patterns for the 'users' app
urlpatterns = [
    # URL for user authentication (login)
    path("auth/login/", TokenCreateView.as_view(), name="login"),
    # URL for user logout
    path("auth/logout/", TokenDestroyView.as_view(), name="logout"),
    path("", include(router.urls)),
    #path("", include(cow_breed_router.urls)),
]
