from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import SpeciesViewSet, PetViewSet, RandomPetViewSet, ReviewViewSet

router = DefaultRouter()

router.register('species', SpeciesViewSet)
router.register('list', PetViewSet)
router.register('random-pets', RandomPetViewSet, basename="random_pets")
router.register('reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]