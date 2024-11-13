from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsBankStaff, IsCustomer, IsSuperAdmin
from .models import *
from .serializers import *

# Create your views here.

class SuperAdminLogin(APIView) :
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs) :
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None and user.is_superuser :
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh' : str(refresh),
                'access' : str(refresh.access_token),
            }, status = status.HTTP_200_OK)
        
        else :
            return Response({"error" : "Invalid Credentials"}, status=status.HTTP_403_FORBIDDEN)
        
class BankStaffRegistrationView(APIView):
    permission_classes = [IsSuperAdmin]

    def post(self, request, *args, **kwargs):
        request.data['user']['is_bankstaff'] = True
        
        serializer = BankStaffSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BankStaffLoginView(APIView) :
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs) :
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None and user.is_bankstaff :
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh' : str(refresh),
                'access' : str(refresh.access_token),
            }, status = status.HTTP_200_OK)
        
        else :
            return Response({"error" : "Invalid Credentials"}, status=status.HTTP_403_FORBIDDEN)
        
class CustomerRegistrationView(APIView):
    permission_classes = [IsBankStaff]

    def post(self, request, *args, **kwargs):
        serializer = CustomerSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CustomerLoginView(APIView) :
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs) :
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None and user.is_customer :
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh' : str(refresh),
                'access' : str(refresh.access_token),
            }, status = status.HTTP_200_OK)
        
        else :
            return Response({"error" : "Invalid Credentials"}, status=status.HTTP_403_FORBIDDEN)

class AccountCreationView(APIView):
    permission_classes = [IsBankStaff]

    def post(self, request, *args, **kwargs):
        serializer = AccountSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CustomerDashboardView(APIView) :
    permission_classes = [IsCustomer]

    def get(self, request, *args, **kwargs):
        try:
            customer = Customer.objects.get(user=request.user)
            account = Account.objects.get(user=customer)

            data = {
                "name": customer.user.name,
                "email": customer.user.email,
                "phone_number": customer.user.phone_number,
                "account_type": account.account_type,
                "account_no": account.account_no,
                "balance": account.balance
            }
            return Response(data, status=200)

        except Customer.DoesNotExist:
            return Response({"detail": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)
        except Account.DoesNotExist:
            return Response({"detail": "Account not found."}, status=status.HTTP_404_NOT_FOUND)
