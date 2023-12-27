from django.urls import path, include
from rest_framework import routers

from .views import *

app_name = 'reproduction'

router = routers.DefaultRouter()
router.register(r'pregnancy-records', PregnancyViewSet, basename='pregnancy-records')

urlpatterns = [
    path('', include(router.urls))
]
