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
        user = User.objects.create_user(**user_data)

        if not user.is_bankstaff:
            raise serializers.ValidationError("User must be assigned as a bank staff.")

        bank_staff = BankStaff.objects.create(user=user, **validated_data)
        return bank_staff


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = ['user', 'dob', 'fathers_name', 'mothers_name', 'address', 'city', 'state', 'pin_number', 'aadhar_no']

    def create(self, validated_data):
        # Extract user data from the validated data
        user_data = validated_data.pop('user')

        # Create the user using create_user method to handle password hashing
        user = User.objects.create_user(**user_data)

        # Ensure the user is assigned as a customer
        user.is_customer = True
        user.save()

        # Create the customer instance and associate the user
        customer = Customer.objects.create(user=user, **validated_data)
        return customer


