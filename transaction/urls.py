from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TransactionViewSet, CreateTransactionApiViewSet

router = DefaultRouter()

router.register('list', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('deposit/', CreateTransactionApiViewSet.as_view(), name='deposit'),
    path('purchase/', CreateTransactionApiViewSet.as_view(), name='purchase'),
]