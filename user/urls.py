from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UserViewSet, UserRegistrationApiView, UserLoginApiView, UserLogOutApiView, activate, UpdatePasswordApiView

router = DefaultRouter()

router.register('list', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationApiView.as_view(), name='register'),
    path('login/', UserLoginApiView.as_view(), name='login'),
    path('logout/', UserLogOutApiView.as_view(), name='logout'),
    path('activate_email/<uid64>/<token>/', activate, name='activate'),
    path('update-password/', UpdatePasswordApiView.as_view(), name='update-password'),
]