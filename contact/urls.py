from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ContactViewSet

router = DefaultRouter()

router.register('contact', ContactViewSet)

urlpatterns = [
    path('', include(router.urls)),
]