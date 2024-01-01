
from django.urls import path, include
from rest_framework import routers

from health.views import WeightRecordViewSet, CullingRecordViewSet

app_name = 'health'

router = routers.DefaultRouter()
router.register(r'weight-records', WeightRecordViewSet, basename='weight-records')
router.register(r'culling-records', CullingRecordViewSet, basename='culling-records')

urlpatterns = [
    path('', include(router.urls))
]
