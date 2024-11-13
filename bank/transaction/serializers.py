from rest_framework import serializers
from .models import Transaction
from bankusers.models import Account

class OwnAccountTransactionSerializers(serializers.ModelSerializer):
    transaction_type = serializers.ChoiceField(choices=['Deposit', 'Withdrawal'])

    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_type']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value
    
class AccountToAccountTransactionSerializers(serializers.ModelSerializer) :
    transaction_type = serializers.ChoiceField(choices=['Transfer'])

    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_type', 'recipient_account_no']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def validate_recipient_account_no(self, value):
        try:
            recipient_account = Account.objects.get(account_no=value)
        except Account.DoesNotExist:
            raise serializers.ValidationError("Recipient account does not exist.")
        return value
    
class StaffToAccountTransactionSerializers(serializers.ModelSerializer) :
    transaction_type = serializers.ChoiceField(choices=['Transfer'])

    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_type', 'recipient_account_no']

class BankStaffTransactionSerializer(serializers.ModelSerializer):
    account_no = serializers.IntegerField() 
    transaction_type = serializers.ChoiceField(choices=['Deposit', 'Withdrawal'])


    class Meta:
        model = Transaction
        fields = ['account_no', 'transaction_type', 'amount']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value
    
    def validate_account_no(self, value):
        if value <= 0:
            raise serializers.ValidationError("Account number must be a positive integer.")
        if not Account.objects.filter(account_no=value).exists():
            raise serializers.ValidationError("Account does not exist.")
        return value

class AllTransactionSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Transaction
        fields = ['id', 'account', 'transaction_type', 'amount', 'date']
