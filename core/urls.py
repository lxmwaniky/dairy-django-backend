from django.urls import path, include
from rest_framework import routers
from core.views import CowBreedViewSet

app_name = "core"

router = routers.DefaultRouter()
router.register(r"cow-breed", CowBreedViewSet, basename="cow-breeds")

urlpatterns = [
    path(
        "", include(router.urls)
    ),  # URL Configuration for Core App: Includes a DefaultRouter to handle the endpoints for cow breeds.
    # Endpoints: 'cow-breed/': Maps to the CowBreedViewSet for CRUD operations on cow breeds.
    # Uses the 'list', 'retrieve', 'create', 'update', 'partial_update', and 'destroy' actions.
    # Usage: Include this URL configuration in your project's main urls.py.
    # Example: path('api/', include('core.urls')),
]
