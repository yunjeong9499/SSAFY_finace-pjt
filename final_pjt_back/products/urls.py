from django.urls import path
from products.views import DepositListAPIView
from products.views import SavingListAPIView
from rest_framework.routers import DefaultRouter
from .views import ScrapViewSet, ScrapCreateView, DepositViewSet, SavingViewSet

router = DefaultRouter()
router.register(r'scraps', ScrapViewSet, basename='scrap')
router.register(r'deposits', DepositViewSet)
router.register(r'savings', SavingViewSet)

urlpatterns = [
    path('deposits/', DepositListAPIView.as_view(), name='deposit-list'),
    path('savings/', SavingListAPIView.as_view(), name='saving-list'),
    # path('scraps/', ScrapCreateView.as_view(), name='scrap-create'),
    # path('savings/', SavingViewSet.as_view({'get': 'list'}), name='savings-list'),
    # path('savings/<int:pk>/', SavingViewSet.as_view({'get': 'retrieve'}), name='savings-detail'),
] + router.urls