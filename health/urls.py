
from django.urls import path, include
from rest_framework import routers

from health.views import WeightRecordViewSet

app_name = 'health'

router = routers.DefaultRouter()
router.register(r'weight-records', WeightRecordViewSet, basename='weight-records')

urlpatterns = [
    path('', include(router.urls))
]


