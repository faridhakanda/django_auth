from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegisterSerializer, UserLoginSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout


# User register
class UserRegister(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = User(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email']
            )
            user.set_password(serializer.validated_data['password'])
            user.save()
            response_serializer = UserRegisterSerializer(user)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# user login

# def authenticate_with_email(email, password):
#     try:
#         user = User.objects.get(email=email)
#         if user.check_password(password):
#             return user
#     except User.DoesNotExist:
#         return None
    
def authenticate_with_email(username, password):
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            return user
    except User.DoesNotExist:
        return None

class UserLoginWithEmail(APIView):
    def post(self, request):
        #email = request.data.get("email")
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response({"detail": "Email and password are required!"})
        user = authenticate_with_email(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            serializer = UserLoginSerializer(user)
            return Response({
                "id": user.id,
                "user": serializer.data,
                "email": user.email,
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        
        return Response({"detail": "Invalid credentials!"}, status=status.HTTP_401_UNAUTHORIZED )

# Create your views here.
class Home(APIView):
    #permission_classes = [IsAuthenticated]
    def get(self, request):
       
        return Response({"message": "Hello, World! from my django backend and nextjs frontend!"})
    




class UserLogin(APIView):
    def post(self, request):
        username = request.data.get("username")
        #email = request.data.get("email"),
        password = request.data.get("password")
        if not username or not password:
        #if not email or not password:
            return Response({"detail": "Username and password are required!"})
        
        user = authenticate(username=username, password=password)
        #user = authenticate(email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            serializer = UserLoginSerializer(user)
            return Response({
                "id": user.id,
                "user": serializer.data,
                "email": user.email,
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid credentials!"}, status=status.HTTP_401_UNAUTHORIZED)

# user logout 
class UserLogout(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({"detail": "Refresh token is required!"}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": "Invalid or expired token!"}, status=status.HTTP_400_BAD_REQUEST)
        

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logout successfully!"}, status=status.HTTP_200_OK)