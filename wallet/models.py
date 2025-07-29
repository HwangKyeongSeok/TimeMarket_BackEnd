# wallet/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone

class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # 시간 단위

    def __str__(self):
        return f"{self.user.username} Wallet: {self.balance} hours"

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', '입금'),
        ('withdraw', '출금'),
        ('transfer', '이체'),
    )

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)
    note = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.wallet.user.username} {self.transaction_type} {self.amount} hours"
