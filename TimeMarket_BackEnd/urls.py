# project/urls.py
from django.urls import path, include

urlpatterns = [
    # ... 기존 URL들
    path('api/wallet/', include('wallet.urls')),
    path('api/', include('users.urls')),
    path('api/map/', include('map.urls')),
    path('api/time-posts/', include('posts.urls'))
]

from django.conf import settings
from django.conf.urls.static import static


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)