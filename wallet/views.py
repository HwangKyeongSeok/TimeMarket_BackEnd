# wallet/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from decimal import Decimal

class WalletBalanceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        wallet, created = Wallet.objects.get_or_create(user=request.user)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)

class DepositView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        wallet, _ = Wallet.objects.get_or_create(user=request.user)
        amount = Decimal(request.data.get('amount', '0'))
        if amount <= 0:
            return Response({'error': '입금액은 0보다 커야 합니다.'}, status=status.HTTP_400_BAD_REQUEST)

        wallet.balance += amount
        wallet.save()

        Transaction.objects.create(wallet=wallet, transaction_type='deposit', amount=amount, note='충전')

        return Response({'message': f'{amount} 시간 입금 완료', 'balance': wallet.balance})

class WithdrawView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        wallet, _ = Wallet.objects.get_or_create(user=request.user)
        amount = Decimal(request.data.get('amount', '0'))
        if amount <= 0:
            return Response({'error': '출금액은 0보다 커야 합니다.'}, status=status.HTTP_400_BAD_REQUEST)
        if wallet.balance < amount:
            return Response({'error': '잔액이 부족합니다.'}, status=status.HTTP_400_BAD_REQUEST)

        wallet.balance -= amount
        wallet.save()

        Transaction.objects.create(wallet=wallet, transaction_type='withdraw', amount=amount, note='사용')

        return Response({'message': f'{amount} 시간 출금 완료', 'balance': wallet.balance})

class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        wallet, _ = Wallet.objects.get_or_create(user=self.request.user)
        return Transaction.objects.filter(wallet=wallet).order_by('-timestamp')
