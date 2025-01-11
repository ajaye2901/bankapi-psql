from rest_framework import serializers
from .models import User, BankStaff, Customer, Account

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'phone_number', 'password', 'is_bankstaff']
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user



class BankStaffSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = BankStaff
        fields = ['user', 'staff_id', 'dob', 'address', 'city', 'state', 'branch']
        read_only_fields = ['staff_id']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['is_bankstaff'] = True
        user = User.objects.create_user(**user_data)

        bank_staff = BankStaff.objects.create(user=user, **validated_data)
        return bank_staff


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = ['user', 'dob', 'fathers_name', 'mothers_name', 'address', 'city', 'state', 'pin_number', 'aadhar_no']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['is_customer'] = True
        user = User.objects.create_user(**user_data)

        customer = Customer.objects.create(user=user, **validated_data)
        return customer

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['user', 'account_type', 'account_no', 'balance']
        read_only_fields = ['account_no']
    
    def create(self, validated_data):
        customer = validated_data.get('user')
        if not isinstance(customer, Customer):
            raise serializers.ValidationError("The provided user is not a customer.")
        
        return super().create(validated_data)
    
class DashboardSerializer(serializers.ModelSerializer) :
    account_type = serializers.CharField(source='account.account_type')
    account_no = serializers.CharField(source='account.account_no')
    balance = serializers.DecimalField(source='account.balance', max_digits=10, decimal_places=2)

    class Meta:
        model = Customer
        fields = ['user__name', 'user__email', 'user__phone_number', 'account_type', 'account_no', 'balance']

