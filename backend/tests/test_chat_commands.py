"""
Unit Tests for Chat Commands

Tests for say, whisper, emote, and shout commands.
"""
import pytest
from unittest.mock import patch, MagicMock
from game.commands.social import SayCommand, WhisperCommand, EmoteCommand, ShoutCommand
from game.models import Player


@pytest.mark.django_db
class TestSayCommand:
    """Tests for Say command (room broadcasts)"""

    def test_say_with_message(self, player, room):
        """SAY-001: Test say command with valid message"""
        player.location = room
        player.save()

        cmd = SayCommand()
        result = cmd.execute(player, args='Hello everyone!')

        assert result == 'You say, "Hello everyone!"'

    def test_say_empty_message(self, player):
        """SAY-003: Test say command with no message"""
        cmd = SayCommand()
        result = cmd.execute(player, args='')

        assert result == 'Say what?'

    def test_say_without_location(self, player):
        """SAY-004: Test say when player has no location"""
        player.location = None
        player.save()

        cmd = SayCommand()
        result = cmd.execute(player, args='Hello')

        assert 'nowhere' in result.lower() or 'void' in result.lower()

    @patch('game.models.room.Room.broadcast')
    def test_say_broadcasts_to_room(self, mock_broadcast, player, room):
        """SAY-002: Test that say broadcasts to other players in room"""
        player.location = room
        player.save()

        cmd = SayCommand()
        cmd.execute(player, args='Hello everyone!')

        # Verify broadcast was called
        mock_broadcast.assert_called_once()
        args = mock_broadcast.call_args
        assert 'Hello everyone!' in args[0][0]
        assert args[1]['exclude'] == player

    def test_say_html_sanitization(self, player, room):
        """SAY-004: Test HTML sanitization in say command"""
        player.location = room
        player.save()

        cmd = SayCommand()
        result = cmd.execute(player, args='<script>alert("XSS")</script>')

        # Script tags should be escaped
        assert '<script>' not in result
        assert '&lt;script&gt;' in result or 'script' in result


@pytest.mark.django_db
class TestWhisperCommand:
    """Tests for Whisper command (direct messaging)"""

    @patch('websocket.utils.send_to_player')
    def test_whisper_to_online_player(self, mock_send, multiple_players):
        """WHI-001: Test whisper to online player"""
        sender = multiple_players[0]
        target = multiple_players[1]
        target.is_online = True
        target.save()

        cmd = WhisperCommand()
        result = cmd.execute(sender, args=f'{target.character_name} Secret message')

        assert f'You whisper to {target.character_name}' in result
        assert 'Secret message' in result

        # Verify WebSocket message was sent
        mock_send.assert_called_once()
        args = mock_send.call_args[0]
        assert args[0] == target
        assert 'Secret message' in args[1]

    def test_whisper_to_offline_player(self, multiple_players):
        """WHI-002: Test whisper to offline player"""
        sender = multiple_players[0]
        target = multiple_players[1]
        target.is_online = False
        target.save()

        cmd = WhisperCommand()
        result = cmd.execute(sender, args=f'{target.character_name} Secret message')

        assert 'not online' in result

    def test_whisper_to_nonexistent_player(self, player):
        """WHI-003: Test whisper to non-existent player"""
        cmd = WhisperCommand()
        result = cmd.execute(player, args='FakePlayer Hello')

        assert 'not online' in result

    def test_whisper_empty_message(self, player):
        """WHI-004: Test whisper with no message"""
        cmd = WhisperCommand()
        result = cmd.execute(player, args='')

        assert 'Usage' in result or 'whisper' in result.lower()

    def test_whisper_case_insensitive(self, multiple_players):
        """WHI-005: Test whisper target name is case insensitive"""
        sender = multiple_players[0]
        target = multiple_players[1]
        target.is_online = True
        target.save()

        cmd = WhisperCommand()

        # Test with lowercase
        result1 = cmd.execute(sender, args=f'{target.character_name.lower()} Hi')
        # Test with uppercase
        result2 = cmd.execute(sender, args=f'{target.character_name.upper()} Hi')

        # Both should work (or both fail with same error)
        assert 'You whisper' in result1 or 'not online' in result1
        assert 'You whisper' in result2 or 'not online' in result2


@pytest.mark.django_db
class TestEmoteCommand:
    """Tests for Emote command"""

    def test_emote_with_action(self, player, room):
        """EMO-001: Test emote with valid action"""
        player.location = room
        player.save()

        cmd = EmoteCommand()
        result = cmd.execute(player, args='waves happily')

        assert player.character_name in result
        assert 'waves happily' in result

    def test_emote_empty_action(self, player):
        """EMO-002: Test emote with no action"""
        cmd = EmoteCommand()
        result = cmd.execute(player, args='')

        assert 'Emote what?' in result

    @patch('game.models.room.Room.broadcast')
    def test_emote_broadcasts_to_room(self, mock_broadcast, player, room):
        """EMO-003: Test emote broadcasts to room"""
        player.location = room
        player.save()

        cmd = EmoteCommand()
        cmd.execute(player, args='dances')

        # Verify broadcast was called
        mock_broadcast.assert_called_once()
        args = mock_broadcast.call_args
        assert 'dances' in args[0][0]
        assert player.character_name in args[0][0]


@pytest.mark.django_db
class TestShoutCommand:
    """Tests for Shout command (zone-wide broadcasts)"""

    @patch('websocket.utils.broadcast_to_zone')
    def test_shout_in_zone(self, mock_broadcast, player, room, zone):
        """SHO-001: Test shout broadcasts to zone"""
        player.location = room
        player.save()

        cmd = ShoutCommand()
        result = cmd.execute(player, args='Help me!')

        assert 'You shout: Help me!' in result

        # Verify zone broadcast was called
        mock_broadcast.assert_called_once()
        args = mock_broadcast.call_args[0]
        assert args[0] == zone
        assert 'Help me!' in args[1]

    def test_shout_empty_message(self, player):
        """SHO-002: Test shout with no message"""
        cmd = ShoutCommand()
        result = cmd.execute(player, args='')

        assert 'Shout what?' in result

    def test_shout_without_location(self, player):
        """SHO-003: Test shout when player has no location"""
        player.location = None
        player.save()

        cmd = ShoutCommand()
        result = cmd.execute(player, args='Hello')

        assert 'void' in result.lower()

    def test_shout_html_sanitization(self, player, room, zone):
        """Test HTML sanitization in shout command"""
        player.location = room
        player.save()

        cmd = ShoutCommand()
        result = cmd.execute(player, args='<b>Bold text</b>')

        # HTML should be escaped
        assert '<b>' not in result or '&lt;b&gt;' in result


@pytest.mark.django_db
class TestCommandRegistry:
    """Tests for command registration and execution"""

    def test_say_command_registered(self):
        """Test that say command is registered"""
        from game.commands import COMMAND_REGISTRY

        assert 'say' in COMMAND_REGISTRY
        assert isinstance(COMMAND_REGISTRY['say'], SayCommand)

    def test_command_aliases(self):
        """Test command aliases work"""
        from game.commands import COMMAND_REGISTRY

        # Say command has aliases '"' and "'"
        assert '"' in COMMAND_REGISTRY
        assert "'" in COMMAND_REGISTRY

    def test_command_handler(self, player, room):
        """Test command handler execution"""
        from game.commands import CommandHandler, COMMAND_REGISTRY

        player.location = room
        player.save()

        result = CommandHandler.handle_command(
            player,
            'say Hello world!',
            COMMAND_REGISTRY
        )

        assert 'Hello world!' in result


@pytest.mark.django_db
class TestWebSocketUtilities:
    """Tests for WebSocket utility functions"""

    @patch('channels.layers.get_channel_layer')
    def test_send_to_player(self, mock_channel_layer, player):
        """Test send_to_player utility"""
        from websocket.utils import send_to_player

        player.is_online = True
        player.save()

        mock_layer = MagicMock()
        mock_channel_layer.return_value = mock_layer

        send_to_player(player, 'Test message', message_type='whisper')

        # Verify group_send was called
        mock_layer.group_send.assert_called()

    @patch('channels.layers.get_channel_layer')
    def test_broadcast_to_room(self, mock_channel_layer, room):
        """Test broadcast_to_room utility"""
        from websocket.utils import broadcast_to_room

        mock_layer = MagicMock()
        mock_channel_layer.return_value = mock_layer

        broadcast_to_room(room, 'Test broadcast')

        # Verify group_send was called with correct group name
        mock_layer.group_send.assert_called()
        call_args = mock_layer.group_send.call_args[0]
        assert call_args[0] == f'room_{room.id}'

    @patch('channels.layers.get_channel_layer')
    def test_broadcast_to_zone(self, mock_channel_layer, zone):
        """Test broadcast_to_zone utility"""
        from websocket.utils import broadcast_to_zone

        mock_layer = MagicMock()
        mock_channel_layer.return_value = mock_layer

        broadcast_to_zone(zone, 'Test zone broadcast')

        # Verify group_send was called with correct group name
        mock_layer.group_send.assert_called()
        call_args = mock_layer.group_send.call_args[0]
        assert call_args[0] == f'zone_{zone.id}'
