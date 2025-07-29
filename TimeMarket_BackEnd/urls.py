# project/urls.py
from django.urls import path, include

urlpatterns = [
    # ... 기존 URL들
    path('api/wallet/', include('wallet.urls')),
]
