from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import SpeciesViewSet, PetViewSet, ReviewViewSet

router = DefaultRouter()

router.register('species', SpeciesViewSet)
router.register('list', PetViewSet)
router.register('reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]