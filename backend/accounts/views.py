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
    UserProfileSerializer, ChangePasswordSerializer,
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer
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

            # Create player character
            from game.models import Player, Room
            character_name = request.data.get('character_name', user.username)

            # Get starting room (or create a default one if needed)
            try:
                starting_room = Room.objects.filter(key='start').first()
            except:
                starting_room = None

            # Use get_or_create to avoid duplicate player creation
            player, created = Player.objects.get_or_create(
                user=user,
                defaults={
                    'character_name': character_name,
                    'location': starting_room,
                    'home': starting_room
                }
            )

            # If player was created by signal, update with custom character_name
            if not created and character_name != player.character_name:
                player.character_name = character_name
                if starting_room:
                    player.location = starting_room
                    player.home = starting_room
                player.save()

            return Response({
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                },
                'player': {
                    'character_name': player.character_name,
                    'level': player.level,
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


class PasswordResetRequestView(APIView):
    """
    Password reset request endpoint

    POST: Request a password reset token via email
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']

            # Find user by email
            try:
                user = User.objects.get(email=email)

                # Generate reset token
                from django.contrib.auth.tokens import default_token_generator
                from django.utils.http import urlsafe_base64_encode
                from django.utils.encoding import force_bytes

                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))

                # TODO: Send email with reset link
                # For now, return token in response (in production, send via email)

                return Response({
                    'message': 'Password reset instructions have been sent to your email',
                    'reset_token': token,  # Remove this in production
                    'uid': uid  # Remove this in production
                })
            except User.DoesNotExist:
                # Don't reveal that user doesn't exist
                return Response({
                    'message': 'Password reset instructions have been sent to your email'
                })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    """
    Password reset confirmation endpoint

    POST: Reset password using token
    """
    permission_classes = [AllowAny]

    def post(self, request):
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.http import urlsafe_base64_decode
        from django.utils.encoding import force_str

        serializer = PasswordResetConfirmSerializer(data=request.data)

        if serializer.is_valid():
            try:
                uid = request.data.get('uid')
                user_id = force_str(urlsafe_base64_decode(uid))
                user = User.objects.get(pk=user_id)

                # Verify token
                token = serializer.validated_data['token']
                if default_token_generator.check_token(user, token):
                    # Set new password
                    user.set_password(serializer.validated_data['new_password'])
                    user.save()

                    # Invalidate all existing tokens
                    Token.objects.filter(user=user).delete()

                    # Create new token
                    new_token = Token.objects.create(user=user)

                    return Response({
                        'message': 'Password reset successful',
                        'token': new_token.key
                    })
                else:
                    return Response({
                        'error': 'Invalid or expired reset token'
                    }, status=status.HTTP_400_BAD_REQUEST)

            except (User.DoesNotExist, ValueError, TypeError):
                return Response({
                    'error': 'Invalid reset link'
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
