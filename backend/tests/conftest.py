"""
Pytest Configuration and Shared Fixtures

This file contains common fixtures used across all tests.
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from game.models import Player, Room, Zone

User = get_user_model()


@pytest.fixture
def api_client():
    """Return Django REST Framework API client"""
    return APIClient()


@pytest.fixture
def create_user(db):
    """Factory fixture for creating users"""
    def make_user(username='testuser', email='test@example.com', password='TestPassword123!'):
        return User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
    return make_user


@pytest.fixture
def user(create_user):
    """Create a single test user"""
    return create_user()


@pytest.fixture
def authenticated_client(api_client, user):
    """Return API client authenticated with test user"""
    token, _ = Token.objects.get_or_create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    api_client.user = user
    api_client.token = token
    return api_client


@pytest.fixture
def create_zone(db):
    """Factory fixture for creating zones"""
    def make_zone(name='Test Zone', key='test_zone'):
        return Zone.objects.create(
            name=name,
            key=key,
            description='A test zone'
        )
    return make_zone


@pytest.fixture
def zone(create_zone):
    """Create a single test zone"""
    return create_zone()


@pytest.fixture
def create_room(db, zone):
    """Factory fixture for creating rooms"""
    def make_room(key='test_room', name='Test Room', zone_obj=None):
        if zone_obj is None:
            zone_obj = zone
        return Room.objects.create(
            key=key,
            name=name,
            description='A test room for testing purposes.',
            zone=zone_obj
        )
    return make_room


@pytest.fixture
def room(create_room):
    """Create a single test room"""
    return create_room()


@pytest.fixture
def starting_room(create_room):
    """Create the starting room"""
    return create_room(key='start', name='Starting Room')


@pytest.fixture
def create_player(db, starting_room):
    """Factory fixture for creating players"""
    def make_player(user_obj=None, character_name=None, location=None):
        if user_obj is None:
            # Create a new user for this player
            username = f'player_{Player.objects.count() + 1}'
            user_obj = User.objects.create_user(
                username=username,
                email=f'{username}@example.com',
                password='TestPassword123!'
            )

        if character_name is None:
            character_name = user_obj.username

        if location is None:
            location = starting_room

        # Check if a player already exists for this user
        existing_player = Player.objects.filter(user=user_obj).first()
        if existing_player:
            return existing_player

        return Player.objects.create(
            user=user_obj,
            character_name=character_name,
            location=location,
            home=location
        )
    return make_player


@pytest.fixture
def player(create_player, user, starting_room):
    """Create a single test player"""
    return create_player(user_obj=user, location=starting_room)


@pytest.fixture
def multiple_players(create_player, starting_room):
    """Create multiple test players in the same room"""
    players = []
    for i in range(3):
        username = f'player{i+1}'
        user = User.objects.create_user(
            username=username,
            email=f'{username}@example.com',
            password='TestPassword123!'
        )
        player = create_player(
            user_obj=user,
            character_name=username,
            location=starting_room
        )
        players.append(player)
    return players


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Enable database access for all tests"""
    pass


@pytest.fixture(scope='function')
def django_db_setup(django_db_setup, django_db_blocker):
    """Override database setup to handle async tests better"""
    with django_db_blocker.unblock():
        pass
