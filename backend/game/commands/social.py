"""
Social Commands

Commands for player communication and emotes.
"""
from .base import Command


class SayCommand(Command):
    """Say something to everyone in the room"""
    key = "say"
    aliases = ['"', "'"]
    help_text = "Say something to everyone in the room"
    category = "Social"

    def execute(self, player, **kwargs):
        """Execute say command"""
        message = kwargs.get('args', '').strip()

        if not message:
            return "Say what?"

        if not player.location:
            return "You are nowhere and your voice echoes into the void."

        # Sanitize message (prevent script injection)
        from django.utils.html import escape
        message = escape(message)

        # Broadcast to room
        room = player.location
        room.broadcast(
            f"{player.character_name} says, \"{message}\"",
            exclude=player
        )

        return f"You say, \"{message}\""


class EmoteCommand(Command):
    """Perform an emote action"""
    key = "emote"
    aliases = ["me", "em"]
    help_text = "Perform an action or emote"
    category = "Social"

    def execute(self, player, **kwargs):
        """Execute emote command"""
        action = kwargs.get('args', '').strip()

        if not action:
            return "Emote what?"

        if not player.location:
            return "You emote into the void, but nobody sees it."

        # Sanitize action
        from django.utils.html import escape
        action = escape(action)

        # Broadcast emote
        room = player.location
        message = f"{player.character_name} {action}"

        room.broadcast(message, exclude=player)

        return message


class WhisperCommand(Command):
    """Whisper to a specific player"""
    key = "whisper"
    aliases = ["tell", "w"]
    help_text = "Whisper to a specific player"
    category = "Social"

    def execute(self, player, **kwargs):
        """Execute whisper command"""
        args = kwargs.get('args', '').strip()

        if not args:
            return "Usage: whisper <player> <message>"

        parts = args.split(maxsplit=1)
        if len(parts) < 2:
            return "Usage: whisper <player> <message>"

        target_name, message = parts

        # Find target player
        from game.models import Player
        target = Player.objects.filter(
            character_name__iexact=target_name,
            is_online=True
        ).first()

        if not target:
            return f"Player '{target_name}' is not online."

        # Sanitize message
        from django.utils.html import escape
        message = escape(message)

        # Send message to target via WebSocket
        from websocket.utils import send_to_player
        whisper_message = f"{player.character_name} whispers to you: {message}"
        send_to_player(target, whisper_message, message_type='whisper')

        return f"You whisper to {target.character_name}: {message}"


class ShoutCommand(Command):
    """Shout to entire zone"""
    key = "shout"
    aliases = ["yell"]
    help_text = "Shout to everyone in the zone"
    category = "Social"

    def execute(self, player, **kwargs):
        """Execute shout command"""
        message = kwargs.get('args', '').strip()

        if not message:
            return "Shout what?"

        if not player.location:
            return "You shout into the void."

        # Sanitize message
        from django.utils.html import escape
        message = escape(message)

        # Broadcast to entire zone
        if player.location and player.location.zone:
            from websocket.utils import broadcast_to_zone
            shout_message = f"{player.character_name} shouts: {message}"
            broadcast_to_zone(player.location.zone, shout_message, message_type='shout')
        else:
            return "You shout into the void."

        return f"You shout: {message}"
