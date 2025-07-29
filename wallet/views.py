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

from decimal import Decimal, InvalidOperation

class TransferView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        sender = request.user
        recipient_username = request.data.get('recipient_username')
        amount = request.data.get('amount')

        
        # 필수 값 체크
        if not recipient_username or amount is None:
            return Response({'error': 'recipient_username and amount are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = Decimal(str(amount))  # float 대신 Decimal 변환
            if amount <= 0:
                return Response({'error': 'Amount must be positive.'}, status=status.HTTP_400_BAD_REQUEST)
        except (InvalidOperation, ValueError):
            return Response({'error': 'Invalid amount format.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            recipient = User.objects.get(username=recipient_username)
        except User.DoesNotExist:
            return Response({'error': 'Recipient user not found.'}, status=status.HTTP_404_NOT_FOUND)

        if recipient == sender:
            return Response({'error': 'Cannot transfer to yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        # 지갑 가져오기
        try:
            sender_wallet = Wallet.objects.get(user=sender)
            recipient_wallet = Wallet.objects.get(user=recipient)
        except Wallet.DoesNotExist:
            return Response({'error': 'Wallet not found for sender or recipient.'}, status=status.HTTP_404_NOT_FOUND)

        # 잔액 부족 체크
        if sender_wallet.balance < amount:
            return Response({'error': 'Insufficient balance.'}, status=status.HTTP_400_BAD_REQUEST)

        # 잔액 업데이트 (트랜잭션 처리 권장)
        sender_wallet.balance -= amount
        recipient_wallet.balance += amount

        sender_wallet.save()
        recipient_wallet.save()

        return Response({'message': f'{amount}시간이 {recipient_username}님께 성공적으로 전송되었습니다.'})