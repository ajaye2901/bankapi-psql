from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from bankusers.permissions import IsCustomer, IsBankStaff, IsSuperAdmin
from bankusers.models import Account
from .serializers import LoanApplicationSerializers, LoanApplicationStatusSerializer
from .models import LoanApplications

# Create your views here.

class LoanApplicationView(APIView):
    permission_classes = [IsCustomer]

    def post(self, request):
        try:
            account = Account.objects.get(user__user=request.user)
        except Account.DoesNotExist:
            return Response({"error": "Account not found or unauthorized."}, status=status.HTTP_404_NOT_FOUND)

        serializer = LoanApplicationSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(account=account)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AllLoansView(APIView):
    permission_classes = [IsBankStaff]

    def get(self, request):
        loans = LoanApplications.objects.all()
        serializer = LoanApplicationSerializers(loans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class LoanStatusUpdateView(APIView):
    permission_classes = [IsBankStaff] 

    def patch(self, request, loan_id):
        try:
            loan_application = LoanApplications.objects.get(id=loan_id)
        except LoanApplications.DoesNotExist:
            return Response({"error": "Loan application not found."}, status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_bankstaff:
            return Response({"error": "You do not have permission to update the loan status."}, status=status.HTTP_403_FORBIDDEN)

        serializer = LoanApplicationStatusSerializer(loan_application, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CustomerAllLoanView(APIView):
    permission_classes = [IsCustomer] 

    def get(self, request):
        loans = LoanApplications.objects.filter(account__user__user=request.user)
        serializer = LoanApplicationSerializers(loans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)