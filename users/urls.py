from django.urls import path
from djoser.views import TokenCreateView, TokenDestroyView

# Set the app name for namespacing
app_name = "users"

# Define URL patterns for the 'users' app
urlpatterns = [
    # URL for user authentication (login)
    path("api/login/", TokenCreateView.as_view(), name="login"),
    # URL for user logout
    path("api/logout/", TokenDestroyView.as_view(), name="logout"),
]
