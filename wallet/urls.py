# wallet/urls.py
from django.urls import path
from .views import WalletBalanceView, DepositView, WithdrawView, TransactionListView

urlpatterns = [
    path('balance/', WalletBalanceView.as_view(), name='wallet-balance'),
    path('deposit/', DepositView.as_view(), name='wallet-deposit'),
    path('withdraw/', WithdrawView.as_view(), name='wallet-withdraw'),
    path('transactions/', TransactionListView.as_view(), name='wallet-transactions'),
]
