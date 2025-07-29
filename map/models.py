from django.db import models
from django.conf import settings

class TimeMarker(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_help_request = models.BooleanField(default=False)  # True: 도움요청, False: 판매
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  # 거래 완료 시 False

    def __str__(self):
        return f"{self.title} ({'도움요청' if self.is_help_request else '판매'})"
