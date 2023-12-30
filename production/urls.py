from django.urls import path, include
from rest_framework import routers

from production.views import LactationViewSet, MilkViewSet

app_name = "production"

router = routers.DefaultRouter()
router.register(r"lactation-records", LactationViewSet, basename="lactation-records")
router.register(r'milk-records', MilkViewSet, basename='milk-records')

urlpatterns = [path("", include(router.urls))]
