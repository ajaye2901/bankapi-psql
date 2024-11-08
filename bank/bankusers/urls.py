from django.urls import path
from .views import *

urlpatterns = [
    path('admin-login/', SuperAdminLogin.as_view(), name='admin-login'),
]

