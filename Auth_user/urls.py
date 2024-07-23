from django.urls import path ,include
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()

router.register('city', CityViewSet,basename='City')
router.register('state', StateViewSet,basename='State')
router.register('country', CountryViewSet,basename='Country')

urlpatterns = [
     path('',include(router.urls)),
     path('login/', LoginView.as_view()),
     path('logout/',Logout.as_view()),
     path('user/', get_coreuser),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
