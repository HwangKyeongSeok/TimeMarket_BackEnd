from django.urls import path
from .views import RegisterDeviceTokenView, UnregisterDeviceTokenView, TestSendPushView

urlpatterns = [
    path('device/register/', RegisterDeviceTokenView.as_view(), name='push-device-register'),
    path('device/unregister/', UnregisterDeviceTokenView.as_view(), name='push-device-unregister'),
    path('test/', TestSendPushView.as_view(), name='push-test'),
]

