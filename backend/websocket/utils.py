"""
WebSocket Utilities

Helper functions for sending messages via WebSocket.
"""
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def send_to_player(player, message, message_type='message'):
    """
    Send a message to a specific player via WebSocket

    Args:
        player: Player object
        message: Message content (string)
        message_type: Type of message (default: 'message')
    """
    if not player.is_online:
        return False

    channel_layer = get_channel_layer()
    room_group_name = f'player_{player.id}'

    try:
        async_to_sync(channel_layer.group_send)(
            room_group_name,
            {
                'type': 'player_message',
                'message': message,
                'message_type': message_type
            }
        )
        return True
    except Exception as e:
        import logging
        logger = logging.getLogger('game')
        logger.error(f"Error sending message to player {player.id}: {e}")
        return False


def broadcast_to_room(room, message, exclude_player=None, message_type='broadcast'):
    """
    Broadcast a message to all players in a room

    Args:
        room: Room object
        message: Message content (string)
        exclude_player: Optional player to exclude from broadcast
        message_type: Type of message (default: 'broadcast')
    """
    channel_layer = get_channel_layer()
    room_group_name = f'room_{room.id}'

    try:
        async_to_sync(channel_layer.group_send)(
            room_group_name,
            {
                'type': 'room_broadcast',
                'message': message,
                'message_type': message_type,
                'exclude_player_id': exclude_player.id if exclude_player else None
            }
        )
        return True
    except Exception as e:
        import logging
        logger = logging.getLogger('game')
        logger.error(f"Error broadcasting to room {room.id}: {e}")
        return False


def broadcast_to_zone(zone, message, message_type='zone_broadcast'):
    """
    Broadcast a message to all players in a zone

    Args:
        zone: Zone object
        message: Message content (string)
        message_type: Type of message (default: 'zone_broadcast')
    """
    channel_layer = get_channel_layer()
    zone_group_name = f'zone_{zone.id}'

    try:
        async_to_sync(channel_layer.group_send)(
            zone_group_name,
            {
                'type': 'zone_broadcast',
                'message': message,
                'message_type': message_type
            }
        )
        return True
    except Exception as e:
        import logging
        logger = logging.getLogger('game')
        logger.error(f"Error broadcasting to zone {zone.id}: {e}")
        return False


def broadcast_global(message, message_type='global'):
    """
    Broadcast a message to all connected players

    Args:
        message: Message content (string)
        message_type: Type of message (default: 'global')
    """
    channel_layer = get_channel_layer()

    try:
        async_to_sync(channel_layer.group_send)(
            'global_chat',
            {
                'type': 'global_broadcast',
                'message': message,
                'message_type': message_type
            }
        )
        return True
    except Exception as e:
        import logging
        logger = logging.getLogger('game')
        logger.error(f"Error broadcasting globally: {e}")
        return False
