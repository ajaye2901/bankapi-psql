from django.urls import path
from .views import *

urlpatterns = [
    path('own-transactions/<int:account_id>/', OwnAccountTransactionView.as_view(), name='own-transaction'),
    path('transfer/', AccountToAccountTransactionView.as_view(), name='transfer'),
    path('staff/transfer/', BankStaffTransactionView.as_view(), name='staff-transfer'),
    path('staff/alltransactions/', AllTransactionView.as_view(), name='all-transactions')

]