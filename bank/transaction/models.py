from django.db import models
from bankusers.models import *
from decimal import Decimal

# Create your models here.

class Transaction(models.Model):
    TRANSACTION_TYPE = (
        ('Deposit', 'Deposit'),
        ('Withdrawal', 'Withdrawal'),
        ('Transfer', 'Transfer')
    )
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    date = models.DateTimeField(auto_now_add=True)
    recipient_account_no = models.PositiveBigIntegerField(null=True, blank=True)  # For Transfer only

    def __str__(self):
        return f"{self.account} - {self.transaction_type} - {self.amount}"
