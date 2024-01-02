from django.urls import path, include
from rest_framework import routers

from reproduction.views import PregnancyViewSet, HeatViewSet

app_name = 'reproduction'

router = routers.DefaultRouter()
router.register(r'pregnancy-records', PregnancyViewSet, basename='pregnancy-records')
router.register(r'heat-records', HeatViewSet, basename='heat-records')

urlpatterns = [
    path('', include(router.urls))
]
