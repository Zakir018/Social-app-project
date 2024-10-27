from django.shortcuts import render
from django.shortcuts import get_object_or_404
from social_app.models import Profile, Post, Comment, Like, Social_group
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import AnonRateThrottle
from django.contrib.auth import authenticate, login

# Create your views here.

class UserLoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({"status":"success", "message":"login successfully", 'token': token.key})

        return Response({'status':"username or password incorrect", "message": "username or password incorrect"})


class UserSignupView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data.get('signup_username')
        first_name =request.data.get('signup_firstname')
        last_name = request.data.get('signup_lastname')
        email = request.data.get('signup_email')
        password = request.data.get('signup_password')
        repeat_password = request.data.get('signup_confirm_password')
        gender = request.data.get('gender')
        age = request.data.get('age')
        country = request.data.get('country')
        

        if User.objects.filter(username=username).exists():
            return Response({"status":"error",  "message":"username already regester"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"status":"error",  "message":"email already regester"}, status=status.HTTP_400_BAD_REQUEST)

        if len(password) < 8 :
            return Response({"status":"error",  "message":"password must be 8 charachter long"}, status=status.HTTP_400_BAD_REQUEST)

        if password != repeat_password :
            return Response({"status":"error",  "message":"password and repeat password must be same"}, status=status.HTTP_400_BAD_REQUEST)
        
        register_user = User.objects.create_user(
            username=username.lower(),
            email=email,
            password=password,
        )
    
        Profile.objects.create(
            user = register_user,
            first_name = first_name,
            last_name = last_name,
            age = age,
            gender = gender,
            country = country
        )
        register_user.save()
        token = Token.objects.create(user = register_user)

        return Response({"status":"success", "token":token.key, 'message': "Accout created successfuly"},status=status.HTTP_201_CREATED)