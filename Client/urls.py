from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('technology_option', Technology_optionViewSet,basename='Technology_option')
router.register('technology', TechnologyViewSet,basename='Technology')
router.register('payment_method', Payment_methodViewSet,basename='Payment_method')
router.register('tax', TaxViewSet,basename='Tax')



urlpatterns = [
    path('api/',include(router.urls)),
    path('client/',ClientAPI.as_view()),
    path('client_filter/', ClientListView.as_view()),
    path('invoice/',InvoiceAPI.as_view()),
    path('invoice_filter/',invoicefilter),
    path('team/',TeamAPIView.as_view()),
    path('project/',ProjectAPIView.as_view()),
    path('project_filter/',projectFilter),
    path('invoice_item/',InvoiceitemAPI.as_view()),
    path('payment/',PaymentAPIView.as_view()),
    path('technology_filter/',TechnologyListView.as_view()),
    path('team_filter/',TeamListView.as_view()),
    path('chart/',invoice_chart),   ##-chart url
    path('payment_filter/',PaymentListView.as_view()),
    
] 



