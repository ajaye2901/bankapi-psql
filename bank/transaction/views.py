from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Transaction
from .serializers import *
from bankusers.permissions import IsCustomer, IsBankStaff, IsSuperAdmin
from bankusers.models import Account

# Create your views here.

class OwnAccountTransactionView(APIView):
    permission_classes = [IsCustomer]

    def post(self, request, account_id):
        serializer = OwnAccountTransactionSerializers(data=request.data)
        if serializer.is_valid():
            transaction_type = serializer.validated_data['transaction_type']
            amount = serializer.validated_data['amount']

            try:
                account = Account.objects.get(id=account_id, user__user=request.user)
            except Account.DoesNotExist:
                return Response({"error": "Account not found or not authorized."}, status=status.HTTP_404_NOT_FOUND)

            if transaction_type == 'Deposit':
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, transaction_type='Deposit', amount=amount)
                return Response({"message": "Deposit successful", "balance": account.balance}, status=status.HTTP_200_OK)

            elif transaction_type == 'Withdrawal':
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, transaction_type='Withdrawal', amount=amount)
                    return Response({"message": "Withdrawal successful", "balance": account.balance}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Insufficient balance."}, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({"error": "Invalid transaction type. Use 'Deposit' or 'Withdrawal'."}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class AccountToAccountTransactionView(APIView):
    permission_classes = [IsCustomer]

    def post(self, request):
        serializer = AccountToAccountTransactionSerializers(data=request.data)
        
        if serializer.is_valid():
            sender_account = None
            recipient_account = None
            transaction_type = serializer.validated_data['transaction_type']
            amount = serializer.validated_data['amount']
            recipient_account_no = serializer.validated_data['recipient_account_no']

            try:
                sender_account = Account.objects.get(user__user=request.user)
            except Account.DoesNotExist:
                return Response({"error": "Sender account not found or not authorized."}, status=status.HTTP_404_NOT_FOUND)

            try:
                recipient_account = Account.objects.get(account_no=recipient_account_no)
            except Account.DoesNotExist:
                return Response({"error": "Recipient account not found."}, status=status.HTTP_404_NOT_FOUND)

            if sender_account.balance < amount:
                return Response({"error": "Insufficient balance."}, status=status.HTTP_400_BAD_REQUEST)

            sender_account.balance -= amount
            recipient_account.balance += amount
            sender_account.save()
            recipient_account.save()

            Transaction.objects.create(account=sender_account, transaction_type='Transfer', amount=-amount, recipient_account_no=recipient_account_no)
            Transaction.objects.create(account=recipient_account, transaction_type='Transfer', amount=amount, recipient_account_no=sender_account.account_no)

            return Response({
                "message": "Transfer successful",
                "My Balance": sender_account.balance
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BankStaffTransactionView(APIView):
    permission_classes = [IsBankStaff] 

    def post(self, request):
        serializer = BankStaffTransactionSerializer(data=request.data)
        
        if serializer.is_valid():
            account_no = serializer.validated_data['account_no']
            transaction_type = serializer.validated_data['transaction_type']
            amount = serializer.validated_data['amount']

            try:
                account = Account.objects.get(account_no=account_no)
            except Account.DoesNotExist:
                return Response({"error": "Account not found."}, status=status.HTTP_404_NOT_FOUND)

            if transaction_type == 'Deposit':
                account.balance += amount
                account.save()
                Transaction.objects.create(account=account, transaction_type='Deposit', amount=amount)
                return Response({"message": "Deposit successful", "balance": account.balance}, status=status.HTTP_200_OK)

            elif transaction_type == 'Withdrawal':
                if account.balance >= amount:
                    account.balance -= amount
                    account.save()
                    Transaction.objects.create(account=account, transaction_type='Withdrawal', amount=amount)
                    return Response({"message": "Withdrawal successful", "balance": account.balance}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Insufficient balance."}, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                return Response({"error": "Invalid transaction type. Use 'Deposit' or 'Withdrawal'."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AllTransactionView(APIView) :
    permission_classes = [IsBankStaff]

    def get(self, request, *args, **kwargs) :
       transactions = Transaction.objects.all().order_by("-date")
       serializer = AllTransactionSerializer(transactions, many=True)
       return Response(serializer.data, status=status.HTTP_200_OK)
