from django.contrib.auth.models import AbstractUser
from django.db import models
import random

class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10)
    is_bankstaff = models.BooleanField(default=False)  
    is_customer = models.BooleanField(default=False)   

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name'] 

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  
        blank=True
    )

    def __str__(self) -> str:
        return self.username

class BankStaff(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bankstaff")
    staff_id = models.CharField(max_length=4, unique=True)
    dob = models.DateField()
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    branch = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if not self.staff_id:
            self.staff_id = self.generate_unique_staff_id()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_unique_staff_id():
        while True:
            staff_id = f"{random.randint(1000, 9999)}"
            if not BankStaff.objects.filter(staff_id=staff_id).exists():
                return staff_id
            
    def __str__(self) -> str:
        return f"{self.user.name} - {self.staff_id}"

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer')
    dob = models.DateField()
    fathers_name = models.CharField(max_length=50)
    mothers_name = models.CharField(max_length=50)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pin_number = models.CharField(max_length=6)
    aadhar_no = models.CharField(max_length=12, unique=True)

    def __str__(self) -> str:
        return f"{self.user.name} - {self.aadhar_no}"

class Account(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    ACCOUNT_CHOICES = (
        ('Savings', 'Savings'),
        ('Current', 'Current'),
        ('Salary', 'Salary'),
        ('NRI', 'NRI'),
        ('FD', 'FD'),
    )
    account_type = models.CharField(max_length=20, choices=ACCOUNT_CHOICES)
    account_no = models.PositiveBigIntegerField(unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if not self.account_no:
            self.account_no = self.generate_unique_account_no()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_unique_account_no():
        while True:
            account_no = random.randint(10**15, 10**16 - 1) 
            if not Account.objects.filter(account_no=account_no).exists():
                return account_no

    def __str__(self) -> str:
        return f"{self.user.user.name} - {self.account_type} - {self.account_no} - {self.balance}"
