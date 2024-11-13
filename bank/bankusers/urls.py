from django.urls import path
from .views import *

urlpatterns = [
    path('admin-login/', SuperAdminLogin.as_view(), name='admin-login'),
    path('staff-regsiter/', BankStaffRegistrationView.as_view(), name='staff-register'),
    path('staff-login/', BankStaffLoginView.as_view(), name='staff-login'),
    path('customer-register/', CustomerRegistrationView.as_view(), name='customer-register'),
    path('customer-login/', CustomerLoginView.as_view(), name='customer-login'),
    
]

