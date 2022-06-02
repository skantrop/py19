from email import message
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404 
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
User = get_user_model()


class RegistrationView(APIView):
    def post(self, request):
        print(dir(request))
        print(request.data)
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            message = """
            You're done!
            """
            return Response(message)


class ActivationView(APIView):
    def get(self, request, activation_code):
        print(dir(request))
        user = get_object_or_404(User, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response('Your account is successfullyy activated!', status=status.HTTP_200_OK)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


















