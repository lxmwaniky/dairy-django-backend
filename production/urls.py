from django.urls import path, include
from rest_framework import routers

from production.views import LactationViewSet

app_name = "production"

router = routers.DefaultRouter()
router.register(r"lactation-records", LactationViewSet, basename="lactation-records")

urlpatterns = [path("", include(router.urls))]
