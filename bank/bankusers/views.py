from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from .models import *

# Create your views here.

class SuperAdminLogin(APIView) :
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs) :
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser :
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh' : str(refresh),
                'access' : str(refresh.access_token),
            }, status = status.HTTP_200_OK)
        
        else :
            return Response({"error" : "Invalid Credentials"}, status=status.HTTP_403_FORBIDDEN)
        

