"""
WebSocket Consumers

Handles WebSocket connections and real-time game communication.
"""
import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone

logger = logging.getLogger('game')


class GameConsumer(AsyncWebsocketConsumer):
    """
    Main game WebSocket consumer

    Handles player connections, commands, and real-time updates.
    """

    async def connect(self):
        """Handle WebSocket connection"""
        self.user = self.scope['user']

        # Reject anonymous users
        if self.user.is_anonymous:
            await self.close(code=4001)
            return

        # Get player
        self.player = await self.get_player()
        if not self.player:
            await self.close(code=4002)
            return

        # Join player's room group
        await self.join_room_group()

        # Join personal player group for direct messages
        await self.join_player_group()

        # Join zone group for zone-wide messages
        await self.join_zone_group()

        # Mark player as online
        await self.set_player_online(True)

        # Accept connection
        await self.accept()

        # Send welcome message
        await self.send_message({
            'type': 'system',
            'message': f'Welcome, {self.player.character_name}!'
        })

        # Send room description
        await self.handle_look_command()

        logger.info(f"Player {self.player.character_name} connected")

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        if hasattr(self, 'player') and self.player:
            # Leave room group
            await self.leave_room_group()

            # Leave player group
            await self.leave_player_group()

            # Leave zone group
            await self.leave_zone_group()

            # Mark player as offline
            await self.set_player_online(False)

            logger.info(f"Player {self.player.character_name} disconnected")

    async def receive(self, text_data):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')

            if message_type == 'command':
                await self.handle_command(data)
            elif message_type == 'ping':
                await self.send_message({'type': 'pong'})
            else:
                await self.send_error(f"Unknown message type: {message_type}")

        except json.JSONDecodeError:
            await self.send_error("Invalid JSON")
        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            await self.send_error("An error occurred processing your request")

    async def handle_command(self, data):
        """Handle game command"""
        command = data.get('command', '').strip()

        if not command:
            return

        # Rate limiting
        # TODO: Implement rate limiting

        # Update last action time
        await self.update_last_action()

        # Execute command
        result = await self.execute_command(command)

        # Send result to player
        await self.send_message({
            'type': 'command_result',
            'message': result
        })

    @database_sync_to_async
    def execute_command(self, raw_command):
        """Execute a game command"""
        from game.commands import COMMAND_REGISTRY, CommandHandler

        return CommandHandler.handle_command(
            self.player,
            raw_command,
            COMMAND_REGISTRY
        )

    async def handle_look_command(self):
        """Send room description to player"""
        from game.commands.movement import LookCommand

        look_cmd = LookCommand()
        result = await database_sync_to_async(look_cmd.look_at_room)(self.player)

        await self.send_message({
            'type': 'room_description',
            'message': result
        })

    async def join_room_group(self):
        """Join the channel group for the player's current room"""
        if self.player.location:
            self.room_group_name = f'room_{self.player.location.id}'
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

    async def leave_room_group(self):
        """Leave the current room group"""
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def join_player_group(self):
        """Join the personal player group for direct messages"""
        self.player_group_name = f'player_{self.player.id}'
        await self.channel_layer.group_add(
            self.player_group_name,
            self.channel_name
        )

    async def leave_player_group(self):
        """Leave the personal player group"""
        if hasattr(self, 'player_group_name'):
            await self.channel_layer.group_discard(
                self.player_group_name,
                self.channel_name
            )

    async def join_zone_group(self):
        """Join the zone group for zone-wide messages"""
        if self.player.location and self.player.location.zone:
            self.zone_group_name = f'zone_{self.player.location.zone.id}'
            await self.channel_layer.group_add(
                self.zone_group_name,
                self.channel_name
            )

    async def leave_zone_group(self):
        """Leave the zone group"""
        if hasattr(self, 'zone_group_name'):
            await self.channel_layer.group_discard(
                self.zone_group_name,
                self.channel_name
            )

    async def room_broadcast(self, event):
        """Handle room broadcast messages"""
        # Skip if this player should be excluded
        exclude_player_id = event.get('exclude_player_id')
        if exclude_player_id and self.player.id == exclude_player_id:
            return

        await self.send_message({
            'type': event.get('message_type', 'broadcast'),
            'message': event['message']
        })

    async def player_message(self, event):
        """Handle direct player messages (whispers, etc)"""
        await self.send_message({
            'type': event.get('message_type', 'whisper'),
            'message': event['message']
        })

    async def zone_broadcast(self, event):
        """Handle zone-wide broadcast messages"""
        await self.send_message({
            'type': event.get('message_type', 'zone_broadcast'),
            'message': event['message']
        })

    async def send_message(self, message_dict):
        """Send a message to the client"""
        await self.send(text_data=json.dumps(message_dict))

    async def send_error(self, error_message):
        """Send an error message to the client"""
        await self.send_message({
            'type': 'error',
            'message': error_message
        })

    @database_sync_to_async
    def get_player(self):
        """Get the player for this user"""
        try:
            return self.user.player
        except:
            return None

    @database_sync_to_async
    def set_player_online(self, is_online):
        """Set player online status"""
        self.player.is_online = is_online
        if is_online:
            self.player.last_login = timezone.now()
        self.player.save(update_fields=['is_online', 'last_login'])

    @database_sync_to_async
    def update_last_action(self):
        """Update player's last action timestamp"""
        self.player.last_action = timezone.now()
        self.player.save(update_fields=['last_action'])


class ChatConsumer(AsyncWebsocketConsumer):
    """
    Global chat consumer

    Handles global/zone-wide chat messages.
    """

    async def connect(self):
        """Handle connection"""
        self.user = self.scope['user']

        if self.user.is_anonymous:
            await self.close(code=4001)
            return

        # Join global chat group
        self.chat_group = 'global_chat'
        await self.channel_layer.group_add(
            self.chat_group,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        """Handle disconnection"""
        if hasattr(self, 'chat_group'):
            await self.channel_layer.group_discard(
                self.chat_group,
                self.channel_name
            )

    async def receive(self, text_data):
        """Handle incoming chat messages"""
        try:
            data = json.loads(text_data)
            message = data.get('message', '').strip()

            if not message:
                return

            # Broadcast to group
            await self.channel_layer.group_send(
                self.chat_group,
                {
                    'type': 'chat_message',
                    'username': self.user.username,
                    'message': message
                }
            )

        except Exception as e:
            logger.error(f"Error in chat: {e}", exc_info=True)

    async def chat_message(self, event):
        """Send chat message to client"""
        await self.send(text_data=json.dumps({
            'type': 'chat',
            'username': event['username'],
            'message': event['message']
        }))
