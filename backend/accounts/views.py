"""
Account Views

Handles user registration, login, and profile management.
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer,
    UserProfileSerializer, ChangePasswordSerializer
)

User = get_user_model()


class RegisterView(APIView):
    """
    User registration endpoint

    POST: Create a new user account
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            # Create auth token
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                },
                'token': token.key,
                'message': 'User registered successfully'
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    User login endpoint

    POST: Authenticate and get auth token
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)

            if user:
                # Create or get token
                token, created = Token.objects.get_or_create(user=user)

                # Update session
                login(request, user)

                return Response({
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                    },
                    'token': token.key,
                    'message': 'Login successful'
                })
            else:
                return Response({
                    'error': 'Invalid credentials'
                }, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    User logout endpoint

    POST: Logout and delete auth token
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Delete user's token
        try:
            request.user.auth_token.delete()
        except:
            pass

        # Logout from session
        logout(request)

        return Response({
            'message': 'Logout successful'
        })


class ProfileView(APIView):
    """
    User profile endpoint

    GET: Get current user profile
    PUT: Update user profile
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """
    Change password endpoint

    POST: Change user password
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user

            # Check old password
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({
                    'error': 'Invalid old password'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Set new password
            user.set_password(serializer.validated_data['new_password'])
            user.save()

            # Create new token
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)

            return Response({
                'message': 'Password changed successfully',
                'token': token.key
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
