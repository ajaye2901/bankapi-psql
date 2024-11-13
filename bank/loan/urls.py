from django.urls import path
from .views import *

urlpatterns = [
    path('loan-application/', LoanApplicationView.as_view(), name='loan-application'),
    path('staff/all-loans/', AllLoansView.as_view(), name='all-loans'),
    path('staff/loan-status/<int:loan_id>/', LoanStatusUpdateView.as_view(), name='loan-status'),
    path('customer/all-loans/', CustomerAllLoanView.as_view(), name="customer-alloans")
]