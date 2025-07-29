from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TimeMarkerViewSet

router = DefaultRouter()
router.register(r'markers', TimeMarkerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
