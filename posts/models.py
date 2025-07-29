from django.db import models
from django.conf import settings

class TimePost(models.Model):
    POST_TYPE_CHOICES = [
        ('sale', '시간 판매'),
        ('request', '구인'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=10, choices=POST_TYPE_CHOICES)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField(default=0)  # 가격 필드 추가 (필요에 따라 옵션 조정)


    def __str__(self):
        return f"{self.title} ({self.get_type_display()})"
