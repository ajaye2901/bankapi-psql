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
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={"is_bankstaff" : True}, related_name="bankstaff")
    staff_id = models.CharField(max_length=4, unique=True)
    dob = models.DateField()
    Address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    Branch = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if not self.staff_id :
            self.staff_id = self.generate_unique_staff_id()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_unique_staff_id() :
        while True :
            staff_id = f"{random.randint(1000,9999)}"
            if not BankStaff.objects.filter(staff_id=staff_id).exists():
                return staff_id
            
    def __str__(self) -> str:
        return f"{self.user.name} - {self.staff_id}"
    
class Customer(models.Model) :

    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={"is_customer" : True}, related_name='customer')
    dob = models.DateField()
    fathers_name = models.CharField(max_length=50)
    mothers_name = models.CharField(max_length=50)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state =  models.CharField(max_length=50)
    pin_number = models.PositiveIntegerField(max_length=6)
    aadhar_no = models.PositiveBigIntegerField(max_length=16)


    
