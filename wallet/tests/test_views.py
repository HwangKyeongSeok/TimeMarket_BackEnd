from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from wallet.models import Wallet

User = get_user_model()

class TimeMarketAPITest(APITestCase):
    def setUp(self):
        # 유저 생성 및 로그인
        self.user1 = User.objects.create_user(username='user1', password='pass1234')
        self.user2 = User.objects.create_user(username='user2', password='pass1234')
        self.client.login(username='user1', password='pass1234')

        # 지갑 생성 (필요 시 직접 생성 or 시그널로 자동 생성된다면 생략)
        self.wallet1 = Wallet.objects.create(user=self.user1, balance=10000)
        self.wallet2 = Wallet.objects.create(user=self.user2, balance=5000)

    def test_wallet_balance(self):
        url = reverse('wallet-balance')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('balance', response.data)
        self.assertAlmostEqual(float(response.data['balance']), float(self.wallet1.balance), places=2)

    def test_wallet_deposit(self):
        url = reverse('wallet-deposit')
        data = {'amount': 3000}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.wallet1.refresh_from_db()
        self.assertEqual(self.wallet1.balance, 13000)

    def test_wallet_withdraw(self):
        url = reverse('wallet-withdraw')
        data = {'amount': 4000}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.wallet1.refresh_from_db()
        self.assertEqual(self.wallet1.balance, 6000)

    def test_wallet_withdraw_insufficient(self):
        url = reverse('wallet-withdraw')
        data = {'amount': 20000}  # 잔액 초과 출금
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_wallet_transfer(self):
        url = reverse('wallet-transfer')
        data = {'recipient_username': self.user2.username, 'amount': 3000}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.wallet1.refresh_from_db()
        self.wallet2.refresh_from_db()
        self.assertEqual(self.wallet1.balance, 7000)
        self.assertEqual(self.wallet2.balance, 8000)

    def test_wallet_transactions(self):
        # 출금, 입금, 전송 등의 거래 내역이 있다면 기록됐는지 테스트
        url = reverse('wallet-transactions')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
