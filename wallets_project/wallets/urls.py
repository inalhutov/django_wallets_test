from django.urls import path
from . import views
from .views import (
    UserCreateAPIView,
    WalletCreateAPIView,
    WalletDetailAPIView,
    WalletOperationAPIView,
)

urlpatterns = [
    path('', views.index, name='index'),
    path('users/', UserCreateAPIView.as_view(), name='user-create'),
    path('users/<int:user_id>/wallets/', WalletCreateAPIView.as_view(), name='wallet-create'),
    path('wallets/<uuid:wallet_uuid>/', WalletDetailAPIView.as_view(), name='wallet-detail'),
    path('wallets/<uuid:wallet_uuid>/operation', WalletOperationAPIView.as_view(), name='wallet-operation'),
]
