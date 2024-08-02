from django.urls import path, include
from rest_framework import routers
from phaseapi.views import PhaseViewSet

router = routers.DefaultRouter()
router.register(r'phase', PhaseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
