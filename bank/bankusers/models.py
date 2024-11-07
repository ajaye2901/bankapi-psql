from django.contrib.auth.models import AbstractUser
from django.db import models
import random

class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10)
    is_bankstaff = False
    is_customer = False

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'email']

    def __str__(self) -> str:
        return self.username

class BankStaff(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={"is_bankstaff" : True})
    staff_id = models.CharField(max_length=4, unique=True)
    DEP_STATUS = (
        ('')
    )

    # ROLE_CHOICES = (
    #     ('admin', 'Admin'),
    #     ('bankstaff', 'Bank Staff'),
    #     ('normal', 'Normal User'),
    # )
    # role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    # account_number = models.CharField(max_length=16, blank=True, unique=True, null=True)

    # def save(self, *args, **kwargs):
    #     if self.role == 'normal' and not self.account_number:
    #         self.account_number = self.generate_account_number()
    #     super().save(*args, **kwargs)

    # @staticmethod
    # def generate_account_number():
    #     return ''.join([str(random.randint(0, 9)) for _ in range(16)])
