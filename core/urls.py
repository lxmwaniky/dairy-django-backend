from django.urls import path, include
from rest_framework import routers
from core.views import CowBreedViewSet, CowViewSet, InseminatorViewset

app_name = "core"

router = routers.DefaultRouter()
router.register(r"cow-breeds", CowBreedViewSet, basename="cow-breeds")
router.register(r"cows", CowViewSet, basename="cows")
router.register(r'inseminator-records', InseminatorViewset, basename='inseminator-records')

urlpatterns = [
    path("", include(router.urls)),
]
