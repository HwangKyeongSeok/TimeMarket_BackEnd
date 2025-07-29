from django.test import TestCase
from wallet.models import Wallet
from django.contrib.auth import get_user_model

User = get_user_model()

class WalletModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_wallet_creation(self):
        wallet = Wallet.objects.create(user=self.user, balance=10000)
        self.assertEqual(wallet.balance, 10000)
        self.assertEqual(wallet.user.username, 'testuser')
