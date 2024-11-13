from rest_framework import serializers
from .models import LoanApplications
from decimal import Decimal

class LoanApplicationSerializers(serializers.ModelSerializer) :
    total_amount_with_interest = serializers.SerializerMethodField()

    class Meta :
        model = LoanApplications
        fields = ['id', 'loan_type', 'loan_amount', 'tenure', 'applied_date', 'total_amount_with_interest', 'approved']
        read_only_fields = ['id', 'applied_date', 'approved']


    def get_total_amount_with_interest(self, obj):
        interest_rates = {
            'personal': Decimal('0.09'),
            'home': Decimal('0.12'),
            'education': Decimal('0.05')
        }
        interest_rate = interest_rates.get(obj.loan_type, Decimal('0'))
        total_interest = obj.loan_amount * (interest_rate / 12) * Decimal(obj.tenure)
        total_amount = obj.loan_amount + total_interest
        return total_amount
    
    def validate_loan_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Loan amount must be greater than zero.")
        return value

    def validate_tenure(self, value):
        if value <= 0:
            raise serializers.ValidationError("Tenure must be a positive number of months.")
        return value
    
class LoanApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApplications
        fields = ['approved']