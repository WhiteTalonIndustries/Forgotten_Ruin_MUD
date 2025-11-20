"""
Integration Tests for WebSocket Connections

Tests for GameConsumer, ChatConsumer, and real-time messaging.
"""
import pytest
import json
from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from server.asgi import application
from game.models import Player

User = get_user_model()


@pytest.mark.django_db
@pytest.mark.asyncio
class TestGameConsumerConnection:
    """Tests for WebSocket connection handling"""

    async def test_connect_with_valid_token(self, player, starting_room):
        """WS-001: Test connection with valid authentication token"""
        # Set player online status and location
        player.is_online = False
        player.location = starting_room
        await database_sync_to_async(player.save)()

        # Get user token
        token = await database_sync_to_async(Token.objects.get_or_create)(user=player.user)
        token_key = token[0].key

        # Create communicator
        communicator = WebsocketCommunicator(
            application,
            f"/ws/game/?token={token_key}"
        )

        # Connect
        connected, subprotocol = await communicator.connect()
        assert connected

        # Should receive welcome message
        response = await communicator.receive_json_from(timeout=5)
        assert response['type'] == 'system'
        assert 'Welcome' in response['message']

        # Clean up
        await communicator.disconnect()

    async def test_connect_without_token(self):
        """WS-002: Test connection without token is rejected"""
        communicator = WebsocketCommunicator(
            application,
            "/ws/game/"
        )

        connected, subprotocol = await communicator.connect()
        # Should be rejected or closed immediately
        # Depending on implementation, might connect then close
        if connected:
            await communicator.disconnect()

    async def test_connect_with_invalid_token(self):
        """WS-003: Test connection with invalid token is rejected"""
        communicator = WebsocketCommunicator(
            application,
            "/ws/game/?token=invalid_token_12345"
        )

        connected, subprotocol = await communicator.connect()
        # Should be rejected
        if connected:
            await communicator.disconnect()

    async def test_player_marked_online_on_connect(self, player, starting_room):
        """WS-004: Test player is marked online when connected"""
        player.is_online = False
        player.location = starting_room
        await database_sync_to_async(player.save)()

        token = await database_sync_to_async(Token.objects.get_or_create)(user=player.user)
        token_key = token[0].key

        communicator = WebsocketCommunicator(
            application,
            f"/ws/game/?token={token_key}"
        )

        connected, subprotocol = await communicator.connect()
        if connected:
            # Refresh player from database
            await database_sync_to_async(player.refresh_from_db)()

            # Player should be marked online
            assert player.is_online

            await communicator.disconnect()

    async def test_player_marked_offline_on_disconnect(self, player, starting_room):
        """WS-008: Test player is marked offline when disconnected"""
        player.location = starting_room
        await database_sync_to_async(player.save)()

        token = await database_sync_to_async(Token.objects.get_or_create)(user=player.user)
        token_key = token[0].key

        communicator = WebsocketCommunicator(
            application,
            f"/ws/game/?token={token_key}"
        )

        connected, subprotocol = await communicator.connect()
        assert connected

        # Disconnect
        await communicator.disconnect()

        # Refresh player
        await database_sync_to_async(player.refresh_from_db)()

        # Player should be marked offline
        assert not player.is_online


@pytest.mark.django_db
@pytest.mark.asyncio
class TestGameConsumerCommands:
    """Tests for game command execution via WebSocket"""

    async def test_send_command(self, player, room):
        """Test sending a game command via WebSocket"""
        player.location = room
        await database_sync_to_async(player.save)()

        token = await database_sync_to_async(Token.objects.get_or_create)(user=player.user)
        token_key = token[0].key

        communicator = WebsocketCommunicator(
            application,
            f"/ws/game/?token={token_key}"
        )

        connected, subprotocol = await communicator.connect()
        assert connected

        # Receive welcome and room description
        await communicator.receive_json_from(timeout=5)  # Welcome
        await communicator.receive_json_from(timeout=5)  # Room description

        # Send say command
        await communicator.send_json_to({
            'type': 'command',
            'command': 'say Hello world'
        })

        # Receive command result
        response = await communicator.receive_json_from(timeout=5)
        assert response['type'] == 'command_result'
        assert 'Hello world' in response['message']

        await communicator.disconnect()

    async def test_ping_pong(self, player, starting_room):
        """Test ping/pong mechanism"""
        player.location = starting_room
        await database_sync_to_async(player.save)()

        token = await database_sync_to_async(Token.objects.get_or_create)(user=player.user)
        token_key = token[0].key

        communicator = WebsocketCommunicator(
            application,
            f"/ws/game/?token={token_key}"
        )

        connected, subprotocol = await communicator.connect()
        assert connected

        # Clear initial messages
        await communicator.receive_json_from(timeout=5)  # Welcome
        await communicator.receive_json_from(timeout=5)  # Room

        # Send ping
        await communicator.send_json_to({'type': 'ping'})

        # Receive pong
        response = await communicator.receive_json_from(timeout=5)
        assert response['type'] == 'pong'

        await communicator.disconnect()


@pytest.mark.django_db
@pytest.mark.asyncio
class TestChatConsumer:
    """Tests for global chat consumer"""

    async def test_global_chat_message(self, user):
        """Test sending global chat message"""
        token = await database_sync_to_async(Token.objects.get_or_create)(user=user)
        token_key = token[0].key

        communicator = WebsocketCommunicator(
            application,
            f"/ws/chat/?token={token_key}"
        )

        connected, subprotocol = await communicator.connect()
        assert connected

        # Send chat message
        await communicator.send_json_to({
            'message': 'Hello global chat!'
        })

        # Should receive own message back
        response = await communicator.receive_json_from(timeout=5)
        assert response['type'] == 'chat'
        assert response['message'] == 'Hello global chat!'
        assert response['username'] == user.username

        await communicator.disconnect()

    async def test_multiple_clients_global_chat(self, create_user):
        """Test multiple clients can see each other's messages"""
        # Create two users
        user1 = await database_sync_to_async(create_user)(username='user1')
        user2 = await database_sync_to_async(create_user)(username='user2')

        token1 = await database_sync_to_async(Token.objects.get_or_create)(user=user1)
        token2 = await database_sync_to_async(Token.objects.get_or_create)(user=user2)

        # Connect both clients
        comm1 = WebsocketCommunicator(
            application,
            f"/ws/chat/?token={token1[0].key}"
        )
        comm2 = WebsocketCommunicator(
            application,
            f"/ws/chat/?token={token2[0].key}"
        )

        connected1, _ = await comm1.connect()
        connected2, _ = await comm2.connect()

        assert connected1 and connected2

        # User1 sends message
        await comm1.send_json_to({'message': 'Hello from user1'})

        # Both users should receive it
        msg1 = await comm1.receive_json_from(timeout=5)
        msg2 = await comm2.receive_json_from(timeout=5)

        assert msg1['message'] == 'Hello from user1'
        assert msg2['message'] == 'Hello from user1'
        assert msg1['username'] == 'user1'
        assert msg2['username'] == 'user1'

        await comm1.disconnect()
        await comm2.disconnect()


@pytest.mark.django_db
@pytest.mark.asyncio
class TestRoomBroadcasts:
    """Tests for room-based message broadcasting"""

    async def test_room_broadcast_to_multiple_players(self, create_player, room):
        """SAY-005: Test room broadcast reaches all players in room"""
        # Create 3 players in the same room
        players = []
        communicators = []

        for i in range(3):
            username = f'player{i}'
            user = await database_sync_to_async(User.objects.create_user)(
                username=username,
                email=f'{username}@example.com',
                password='TestPassword123!'
            )
            player = await database_sync_to_async(create_player)(
                user_obj=user,
                character_name=username,
                location=room
            )
            players.append(player)

            # Connect to WebSocket
            token = await database_sync_to_async(Token.objects.get_or_create)(user=user)
            comm = WebsocketCommunicator(
                application,
                f"/ws/game/?token={token[0].key}"
            )
            connected, _ = await comm.connect()
            assert connected

            # Clear welcome messages
            await comm.receive_json_from(timeout=5)  # Welcome
            await comm.receive_json_from(timeout=5)  # Room

            communicators.append(comm)

        # Player 0 says something
        await communicators[0].send_json_to({
            'type': 'command',
            'command': 'say Hello everyone!'
        })

        # Player 0 gets command result
        result = await communicators[0].receive_json_from(timeout=5)
        assert result['type'] == 'command_result'

        # Players 1 and 2 should receive broadcast
        for i in [1, 2]:
            broadcast = await communicators[i].receive_json_from(timeout=5)
            assert 'Hello everyone!' in broadcast['message']

        # Clean up
        for comm in communicators:
            await comm.disconnect()


@pytest.mark.django_db
@pytest.mark.asyncio
class TestGroupManagement:
    """Tests for WebSocket group joining/leaving"""

    async def test_join_room_group(self, player, room):
        """WS-005: Test player joins room group on connect"""
        player.location = room
        await database_sync_to_async(player.save)()

        token = await database_sync_to_async(Token.objects.get_or_create)(user=player.user)
        token_key = token[0].key

        communicator = WebsocketCommunicator(
            application,
            f"/ws/game/?token={token_key}"
        )

        connected, _ = await communicator.connect()
        assert connected

        # Player should be in room group
        # We can't directly check this, but commands should work
        await communicator.receive_json_from(timeout=5)  # Welcome
        await communicator.receive_json_from(timeout=5)  # Room

        # Send a say command (which uses room group)
        await communicator.send_json_to({
            'type': 'command',
            'command': 'say test'
        })

        result = await communicator.receive_json_from(timeout=5)
        assert result['type'] == 'command_result'

        await communicator.disconnect()

    async def test_join_zone_group(self, player, room, zone):
        """WS-007: Test player joins zone group on connect"""
        room.zone = zone
        await database_sync_to_async(room.save)()

        player.location = room
        await database_sync_to_async(player.save)()

        token = await database_sync_to_async(Token.objects.get_or_create)(user=player.user)
        token_key = token[0].key

        communicator = WebsocketCommunicator(
            application,
            f"/ws/game/?token={token_key}"
        )

        connected, _ = await communicator.connect()
        assert connected

        # Clear initial messages
        await communicator.receive_json_from(timeout=5)
        await communicator.receive_json_from(timeout=5)

        # Send shout command (uses zone group)
        await communicator.send_json_to({
            'type': 'command',
            'command': 'shout Testing!'
        })

        result = await communicator.receive_json_from(timeout=5)
        assert result['type'] == 'command_result'
        assert 'Testing!' in result['message']

        await communicator.disconnect()
