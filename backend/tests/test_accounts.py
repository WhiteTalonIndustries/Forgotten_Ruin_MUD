"""
Unit Tests for User Account Features

Tests for registration, login, logout, password reset, and player creation.
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from game.models import Player

User = get_user_model()


@pytest.mark.django_db
class TestUserRegistration:
    """Tests for user registration endpoint"""

    def test_valid_registration(self, api_client, starting_room):
        """REG-001: Test successful user registration"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecurePassword123!',
            'password_confirm': 'SecurePassword123!'
        }

        response = api_client.post('/auth/register/', data)

        assert response.status_code == status.HTTP_201_CREATED
        assert 'token' in response.data
        assert 'user' in response.data
        assert 'player' in response.data
        assert response.data['user']['username'] == 'newuser'

        # Verify user created in database
        assert User.objects.filter(username='newuser').exists()

        # Verify player created
        user = User.objects.get(username='newuser')
        assert hasattr(user, 'player')
        assert user.player.character_name == 'newuser'

    def test_registration_with_custom_character_name(self, api_client, starting_room):
        """REG-007: Test registration with custom character name"""
        data = {
            'username': 'john',
            'email': 'john@example.com',
            'password': 'SecurePassword123!',
            'password_confirm': 'SecurePassword123!',
            'character_name': 'JohnTheGreat'
        }

        response = api_client.post('/auth/register/', data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['player']['character_name'] == 'JohnTheGreat'

        user = User.objects.get(username='john')
        assert user.player.character_name == 'JohnTheGreat'

    def test_duplicate_username(self, api_client, user):
        """REG-002: Test registration with duplicate username"""
        data = {
            'username': user.username,
            'email': 'different@example.com',
            'password': 'SecurePassword123!',
            'password_confirm': 'SecurePassword123!'
        }

        response = api_client.post('/auth/register/', data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'username' in response.data

    def test_duplicate_email(self, api_client, user):
        """REG-003: Test registration with duplicate email"""
        data = {
            'username': 'differentuser',
            'email': user.email,
            'password': 'SecurePassword123!',
            'password_confirm': 'SecurePassword123!'
        }

        response = api_client.post('/auth/register/', data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data

    def test_password_mismatch(self, api_client):
        """REG-004: Test registration with mismatched passwords"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecurePassword123!',
            'password_confirm': 'DifferentPassword123!'
        }

        response = api_client.post('/auth/register/', data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password_confirm' in response.data or 'non_field_errors' in response.data

    def test_weak_password(self, api_client):
        """REG-005: Test registration with weak password"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'weak',
            'password_confirm': 'weak'
        }

        response = api_client.post('/auth/register/', data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password' in response.data

    def test_invalid_email(self, api_client):
        """REG-006: Test registration with invalid email"""
        data = {
            'username': 'newuser',
            'email': 'not-an-email',
            'password': 'SecurePassword123!',
            'password_confirm': 'SecurePassword123!'
        }

        response = api_client.post('/auth/register/', data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data


@pytest.mark.django_db
class TestUserLogin:
    """Tests for user login endpoint"""

    def test_valid_login(self, api_client, user):
        """LOG-001: Test successful login"""
        data = {
            'username': user.username,
            'password': 'TestPassword123!'
        }

        response = api_client.post('/auth/login/', data)

        assert response.status_code == status.HTTP_200_OK
        assert 'token' in response.data
        assert 'user' in response.data
        assert response.data['user']['username'] == user.username

    def test_invalid_username(self, api_client):
        """LOG-002: Test login with invalid username"""
        data = {
            'username': 'nonexistent',
            'password': 'TestPassword123!'
        }

        response = api_client.post('/auth/login/', data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'error' in response.data

    def test_invalid_password(self, api_client, user):
        """LOG-003: Test login with invalid password"""
        data = {
            'username': user.username,
            'password': 'WrongPassword123!'
        }

        response = api_client.post('/auth/login/', data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'error' in response.data


@pytest.mark.django_db
class TestUserLogout:
    """Tests for user logout endpoint"""

    def test_logout(self, authenticated_client):
        """Test successful logout"""
        token_key = authenticated_client.token.key

        response = authenticated_client.post('/auth/logout/')

        assert response.status_code == status.HTTP_200_OK
        assert 'message' in response.data

        # Verify token was deleted
        assert not Token.objects.filter(key=token_key).exists()

    def test_logout_without_auth(self, api_client):
        """Test logout without authentication"""
        response = api_client.post('/auth/logout/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPasswordReset:
    """Tests for password reset functionality"""

    def test_password_reset_request(self, api_client, user):
        """PWD-001: Test password reset request"""
        data = {'email': user.email}

        response = api_client.post('/auth/password-reset/', data)

        assert response.status_code == status.HTTP_200_OK
        assert 'message' in response.data
        # In development, token is returned (remove in production)
        assert 'reset_token' in response.data
        assert 'uid' in response.data

    def test_password_reset_invalid_email(self, api_client):
        """PWD-002: Test password reset with non-existent email"""
        data = {'email': 'nonexistent@example.com'}

        response = api_client.post('/auth/password-reset/', data)

        # Should return 200 to not reveal user existence
        assert response.status_code == status.HTTP_200_OK
        assert 'message' in response.data

    def test_password_reset_confirm_valid(self, api_client, user):
        """PWD-003: Test password reset confirmation with valid token"""
        # First request reset
        response = api_client.post('/auth/password-reset/', {'email': user.email})
        token = response.data['reset_token']
        uid = response.data['uid']

        # Confirm reset
        data = {
            'uid': uid,
            'token': token,
            'new_password': 'NewSecurePassword123!',
            'new_password_confirm': 'NewSecurePassword123!'
        }

        response = api_client.post('/auth/password-reset-confirm/', data)

        assert response.status_code == status.HTTP_200_OK
        assert 'token' in response.data

        # Verify can login with new password
        user.refresh_from_db()
        assert user.check_password('NewSecurePassword123!')

    def test_password_reset_confirm_invalid_token(self, api_client, user):
        """PWD-004: Test password reset with invalid token"""
        # Get valid uid
        response = api_client.post('/auth/password-reset/', {'email': user.email})
        uid = response.data['uid']

        data = {
            'uid': uid,
            'token': 'invalid-token-12345',
            'new_password': 'NewSecurePassword123!',
            'new_password_confirm': 'NewSecurePassword123!'
        }

        response = api_client.post('/auth/password-reset-confirm/', data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestPlayerCreation:
    """Tests for automatic player character creation"""

    def test_player_created_on_registration(self, api_client, starting_room):
        """PLR-001: Test player is automatically created on registration"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecurePassword123!',
            'password_confirm': 'SecurePassword123!'
        }

        response = api_client.post('/auth/register/', data)

        assert response.status_code == status.HTTP_201_CREATED

        user = User.objects.get(username='newuser')
        assert hasattr(user, 'player')
        assert isinstance(user.player, Player)

    def test_player_starting_location(self, api_client, starting_room):
        """PLR-002: Test player is placed in starting room"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecurePassword123!',
            'password_confirm': 'SecurePassword123!'
        }

        response = api_client.post('/auth/register/', data)

        user = User.objects.get(username='newuser')
        assert user.player.location == starting_room
        assert user.player.home == starting_room

    def test_player_default_stats(self, api_client, starting_room):
        """PLR-003: Test player has correct default stats"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecurePassword123!',
            'password_confirm': 'SecurePassword123!'
        }

        response = api_client.post('/auth/register/', data)

        user = User.objects.get(username='newuser')
        player = user.player

        assert player.level == 1
        assert player.health == 100
        assert player.max_health == 100
        assert player.mana == 100
        assert player.max_mana == 100
        assert player.strength == 10
        assert player.dexterity == 10
        assert player.intelligence == 10
        assert player.constitution == 10

    def test_one_player_per_user(self, api_client, starting_room):
        """PLR-004: Test one-to-one relationship between user and player"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecurePassword123!',
            'password_confirm': 'SecurePassword123!'
        }

        response = api_client.post('/auth/register/', data)

        user = User.objects.get(username='newuser')

        # Try to create another player for same user (should fail)
        with pytest.raises(Exception):
            Player.objects.create(
                user=user,
                character_name='AnotherCharacter'
            )


@pytest.mark.django_db
class TestUserProfile:
    """Tests for user profile endpoint"""

    def test_get_profile(self, authenticated_client, player):
        """Test getting user profile"""
        response = authenticated_client.get('/auth/profile/')

        assert response.status_code == status.HTTP_200_OK
        assert 'username' in response.data
        assert 'email' in response.data
        assert 'character_name' in response.data
        assert 'level' in response.data

    def test_update_profile(self, authenticated_client):
        """Test updating user profile"""
        data = {'email': 'newemail@example.com'}

        response = authenticated_client.put('/auth/profile/', data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == 'newemail@example.com'

    def test_profile_without_auth(self, api_client):
        """Test accessing profile without authentication"""
        response = api_client.get('/auth/profile/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
