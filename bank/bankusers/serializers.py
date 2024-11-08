from rest_framework import serializers
from .models import *

class UserSerializer(serializers.Serializer) :
    class Meta :
        model = User
        fields = ['id','username', 'name', 'email', 'phone_number', 'is_bankstaff', 'is_customer']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            name=validated_data['name'],
            phone_number=validated_data['phone_number']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class BankStaffSerializer(serializers.Serializer) :
    user = UserSerializer(read_only=True)

    class Meta:
        model = BankStaff
        fields = ['id', 'user', 'staff_id', 'dob', 'Address', 'city', 'state', 'Branch']

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user', 'dob', 'fathers_name', 'mothers_name', 'address', 'city', 'state', 'pin_number', 'aadhar_no']

class AccountSerializer(serializers.ModelSerializer):
    user = CustomerSerializer(read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'user', 'account_type', 'account_no', 'balance']