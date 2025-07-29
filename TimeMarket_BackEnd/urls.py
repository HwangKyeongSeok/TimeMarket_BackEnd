# project/urls.py
from django.urls import path, include

urlpatterns = [
    # ... 기존 URL들
    path('api/wallet/', include('wallet.urls')),
    path('api/', include('users.urls')),
    path('api/map/', include('map.urls')),
    path('api/time-posts/', include('posts.urls'))
]
