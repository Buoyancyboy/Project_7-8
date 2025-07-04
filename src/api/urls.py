from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LogDataViewSet

router = DefaultRouter()
router.register(r'log_data', LogDataViewSet, basename='log_data')

urlpatterns = [
    path('', include(router.urls)),
]
