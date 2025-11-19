# WebSocket Implementations for Real-Time MUD Gameplay

## Overview
WebSockets enable bidirectional, real-time communication between the game server and web clients, essential for MUD gameplay where immediate feedback and continuous world updates are critical.

## Why WebSockets for MUDs?

### Traditional Approach Problems
- **HTTP Polling**: Inefficient, high latency, server overhead
- **Long Polling**: Better but still wasteful
- **AJAX**: One-directional, requires constant requests

### WebSocket Advantages
- **Full-duplex communication**: Server can push updates instantly
- **Low latency**: Critical for combat, movement, chat
- **Reduced overhead**: Single persistent connection vs. multiple HTTP requests
- **Real-time events**: World changes propagate immediately
- **Efficient**: Lower bandwidth usage for ongoing communication

## WebSocket Protocol Basics

### Connection Lifecycle
1. **Handshake**: HTTP upgrade request to WebSocket protocol
2. **Open**: Persistent connection established
3. **Message Exchange**: Bidirectional communication
4. **Close**: Graceful connection termination

### Message Format
- Text frames (JSON for structured data)
- Binary frames (for optimized data)
- Ping/Pong frames (keep-alive)

## Django Channels Implementation

### Architecture Overview
- **ASGI**: Asynchronous Server Gateway Interface
- **Channel Layers**: Message passing between consumers
- **Consumers**: WebSocket connection handlers
- **Routing**: URL-based WebSocket routing

### Core Components

#### 1. ASGI Configuration
```python
# asgi.py
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            game.routing.websocket_urlpatterns
        )
    ),
})
```

#### 2. WebSocket Consumer
```python
# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'game_room_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        # Process game command
        result = await self.process_action(action, data)

        # Send to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'game_update',
                'message': result
            }
        )

    async def game_update(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'update',
            'data': event['message']
        }))
```

#### 3. Routing Configuration
```python
# routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/game/(?P<room_id>\w+)/$', consumers.GameConsumer.as_asgi()),
]
```

#### 4. Channel Layers with Redis
```python
# settings.py
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
```

### Benefits of Django Channels
- Seamless integration with Django authentication
- Access to ORM within async consumers
- Distributed message passing via channel layers
- Scalable across multiple server instances
- Standard WebSocket protocol compliance

## Flask-SocketIO Implementation

### Architecture Overview
- **Socket.IO Protocol**: Enhanced WebSocket with fallbacks
- **Event-based communication**: Named events for different actions
- **Rooms**: Group connections for broadcasting
- **Namespaces**: Logical separation of connections

### Core Components

#### 1. Basic Setup
```python
# app.py
from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")
```

#### 2. Event Handlers
```python
# Socket.IO events
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('connection_response', {'status': 'connected'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('player_action')
def handle_player_action(data):
    action_type = data.get('action')
    player_id = data.get('player_id')

    # Process game action
    result = process_game_action(action_type, player_id, data)

    # Broadcast to all clients in the room
    emit('world_update', result, room=data.get('room_id'), broadcast=True)

@socketio.on('join_room')
def handle_join_room(data):
    room = data['room_id']
    join_room(room)
    emit('room_joined', {'room': room})

@socketio.on('leave_room')
def handle_leave_room(data):
    room = data['room_id']
    leave_room(room)
    emit('room_left', {'room': room})
```

#### 3. Background Tasks
```python
from threading import Thread
import time

def background_game_loop():
    """Simulate continuous game world updates"""
    while True:
        time.sleep(1)  # Tick rate
        # Update game state
        world_state = update_world_state()
        # Broadcast to all connected clients
        socketio.emit('world_tick', world_state, broadcast=True)

# Start background task
thread = Thread(target=background_game_loop)
thread.daemon = True
thread.start()
```

#### 4. Running the Server
```python
if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
```

### Benefits of Flask-SocketIO
- Simple event-driven model
- Automatic fallback to long-polling
- Excellent cross-browser compatibility
- Easy to learn and implement
- Built-in room management

## Client-Side Implementation

### JavaScript WebSocket (Native)
```javascript
// For Django Channels (standard WebSocket)
const socket = new WebSocket('ws://localhost:8000/ws/game/room1/');

socket.onopen = function(e) {
    console.log('Connected to game server');
    socket.send(JSON.stringify({
        action: 'join',
        player_id: playerId
    }));
};

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    handleGameUpdate(data);
};

socket.onclose = function(event) {
    console.log('Disconnected from server');
};

socket.onerror = function(error) {
    console.error('WebSocket error:', error);
};

// Send game command
function sendCommand(command, args) {
    socket.send(JSON.stringify({
        action: command,
        data: args,
        player_id: playerId
    }));
}
```

### Socket.IO Client
```javascript
// For Flask-SocketIO
const socket = io('http://localhost:5000');

socket.on('connect', () => {
    console.log('Connected to game server');
    socket.emit('join_room', { room_id: 'room1' });
});

socket.on('world_update', (data) => {
    handleGameUpdate(data);
});

socket.on('disconnect', () => {
    console.log('Disconnected from server');
});

// Send game command
function sendCommand(command, args) {
    socket.emit('player_action', {
        action: command,
        data: args,
        player_id: playerId,
        room_id: currentRoom
    });
}
```

## Message Protocol Design

### Command Messages (Client → Server)
```json
{
    "type": "command",
    "action": "move",
    "direction": "north",
    "player_id": "player_123",
    "timestamp": 1635789012345
}
```

### Update Messages (Server → Client)
```json
{
    "type": "update",
    "event": "room_description",
    "data": {
        "room_id": "dungeon_entrance",
        "description": "You stand at the entrance...",
        "exits": ["north", "east"],
        "players": ["player_456"],
        "items": ["torch", "sword"]
    },
    "timestamp": 1635789012350
}
```

### Broadcast Messages (Server → All)
```json
{
    "type": "broadcast",
    "event": "player_action",
    "data": {
        "player_name": "Hero",
        "action": "says",
        "message": "Hello, world!"
    }
}
```

## Performance Optimization

### Connection Management
- **Heartbeat/Ping-Pong**: Detect disconnected clients
- **Reconnection Logic**: Automatic reconnection with state recovery
- **Connection Pooling**: Limit connections per user
- **Timeout Handling**: Close inactive connections

### Message Optimization
- **Message Batching**: Combine multiple updates
- **Delta Updates**: Send only changed data
- **Compression**: Enable WebSocket compression
- **Binary Protocols**: Use MessagePack or Protocol Buffers for efficiency

### Scalability
- **Load Balancing**: Distribute connections across servers
- **Redis Pub/Sub**: Share messages between server instances
- **Sticky Sessions**: Route user to same server instance
- **Horizontal Scaling**: Add more WebSocket servers as needed

## Security Considerations

### Authentication
```python
# Django Channels with JWT
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
import jwt

class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        token = scope['query_string'].decode().split('=')[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            scope['user'] = await get_user(payload['user_id'])
        except:
            scope['user'] = AnonymousUser()
        return await super().__call__(scope, receive, send)
```

### Input Validation
- Validate all incoming messages
- Sanitize user input before broadcasting
- Rate limiting to prevent spam/abuse
- Command whitelist to prevent injection

### Encryption
- Use WSS (WebSocket Secure) in production
- TLS/SSL certificate required
- Never send sensitive data unencrypted

## Testing WebSocket Connections

### Python Testing
```python
# Django Channels test
from channels.testing import WebsocketCommunicator
from myapp.consumers import GameConsumer

async def test_game_consumer():
    communicator = WebsocketCommunicator(GameConsumer.as_asgi(), "/ws/game/1/")
    connected, _ = await communicator.connect()
    assert connected

    await communicator.send_json_to({"action": "move", "direction": "north"})
    response = await communicator.receive_json_from()
    assert response['type'] == 'update'

    await communicator.disconnect()
```

### Browser Testing
- Chrome DevTools → Network → WS tab
- Monitor WebSocket frames
- Inspect message content

## Recommended Implementation

**For Forgotten Ruin MUD: Use Django Channels**

Reasons:
1. Standard WebSocket protocol (not proprietary)
2. Better scalability with Redis backend
3. Seamless Django integration
4. Production-ready for large-scale deployment
5. True async/await support
6. Distributed server architecture support

## Deployment Considerations

### ASGI Server Options
- **Daphne**: Official Django Channels server
- **Uvicorn**: High-performance ASGI server
- **Hypercorn**: HTTP/2 and HTTP/3 support

### Production Setup
```bash
# Install dependencies
pip install channels channels-redis daphne

# Run with Daphne
daphne -b 0.0.0.0 -p 8000 myproject.asgi:application

# Or with Uvicorn
uvicorn myproject.asgi:application --host 0.0.0.0 --port 8000
```

### Reverse Proxy (Nginx)
```nginx
upstream django {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name example.com;

    location /ws/ {
        proxy_pass http://django;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

## Conclusion

WebSocket implementation is critical for real-time MUD gameplay. Django Channels provides a robust, scalable solution that integrates seamlessly with the recommended Django backend while supporting distributed architectures for growth.
