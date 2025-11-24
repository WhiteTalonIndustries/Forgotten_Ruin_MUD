# Chat System and Player Character Integration

## Overview

This document describes the integrated chat system and player character features that enable real-time communication and character management in the Forgotten Ruin MUD.

## Features Implemented

### 1. Player Character Integration

#### Automatic Character Creation
- Players are automatically created when users register
- Character names can be customized during registration
- Players start in a designated starting room
- All character stats are initialized with default values

#### Character Data Management
- **API Endpoints:**
  - `GET /api/v1/players/me/` - Get current player data
  - `GET /api/v1/player/stats/` - Get player statistics
  - `GET /api/v1/character/me/` - Get detailed character sheet

#### Real-Time Stats Updates
- Player stats update in real-time via WebSocket
- Changes to health, mana, experience, etc. are reflected immediately
- Stats panel auto-refreshes when receiving `player_update` messages

### 2. Chat System

#### Available Chat Commands

##### 1. Say (Room Chat)
```
say <message>
"<message>
'<message>
```
Sends a message to all players in the same room.

**Example:**
```
say Hello everyone!
```

##### 2. Whisper (Private Message)
```
whisper <player_name> <message>
tell <player_name> <message>
w <player_name> <message>
```
Sends a private message to a specific online player.

**Example:**
```
whisper Alice Can you help me with this quest?
```

##### 3. Emote (Action)
```
emote <action>
me <action>
em <action>
```
Performs an action visible to everyone in the room.

**Example:**
```
emote waves happily
```

##### 4. Shout (Zone-Wide)
```
shout <message>
yell <message>
```
Broadcasts a message to all players in the current zone.

**Example:**
```
shout Need help at the dungeon entrance!
```

##### 5. Global Chat
```
global <message>
g <message>
chat <message>
```
Sends a message to all online players across all zones.

**Example:**
```
global Anyone up for a raid?
```

### 3. Frontend Components

#### GameTerminal
- Main command input interface
- Command history navigation (Arrow Up/Down)
- Auto-completion support
- Filters chat messages to ChatPanel

#### ChatPanel
- Displays all chat messages with color coding
- Filters by message type: All, Say, Whisper, Shout, Global
- Username highlighting for better readability
- Auto-scroll to newest messages
- Clear chat button

#### PlayerStats
- Displays character name, level, and experience
- Health and mana bars with visual indicators
- Core attributes (Strength, Dexterity, Intelligence, Constitution)
- Currency and inventory space tracking
- Real-time updates via WebSocket

#### CharacterSheet
- Comprehensive character information
- Equipped items with stat modifiers
- Inventory management
- Active quests display
- Full character description

### 4. WebSocket Integration

#### Message Types
- `command` - Game command execution
- `broadcast` - Room-wide message (say)
- `whisper` - Private message
- `shout` - Zone-wide message
- `zone_broadcast` - Zone broadcast
- `global` - Global chat message
- `player_update` - Real-time stat updates
- `system` - System messages
- `error` - Error messages

#### Channel Groups
Players automatically join the following WebSocket groups:
- **Room Group** (`room_{room_id}`) - Room-specific messages
- **Player Group** (`player_{player_id}`) - Direct messages
- **Zone Group** (`zone_{zone_id}`) - Zone-wide broadcasts
- **Global Chat Group** (`global_chat`) - Global messages

## Technical Architecture

### Backend Structure

```
backend/
├── game/
│   ├── models/
│   │   └── player.py          # Player model with stats
│   ├── commands/
│   │   ├── social.py          # Chat commands
│   │   └── __init__.py        # Command registry
├── websocket/
│   ├── consumers.py           # WebSocket handlers
│   └── utils.py               # Broadcast utilities
└── api/v1/
    ├── views.py               # REST API endpoints
    └── serializers.py         # Data serializers
```

### Frontend Structure

```
frontend/src/
├── components/
│   ├── GameTerminal.js        # Command input
│   ├── ChatPanel.js           # Chat display
│   ├── PlayerStats.js         # Stats display
│   └── CharacterSheet.js      # Full character view
├── hooks/
│   └── useWebSocket.js        # WebSocket connection
└── pages/
    └── GamePage.js            # Main game interface
```

## Security Features

- **HTML Sanitization**: All user input is sanitized to prevent XSS attacks
- **Authentication**: Token-based authentication for all WebSocket connections
- **Rate Limiting**: Command rate limiting (to be implemented)
- **Input Validation**: All commands are validated before execution

## Usage Guide

### For Players

1. **Login**: Use your credentials to access the game
2. **Navigate**: Your character appears in the starting room
3. **Chat**: Use any of the chat commands to communicate
4. **Check Stats**: View your stats in the left sidebar
5. **Character Sheet**: Click "Character Sheet" to view full details

### For Developers

#### Adding New Chat Commands

1. Create a new command class in `backend/game/commands/social.py`:
```python
class NewCommand(Command):
    key = "newcmd"
    aliases = ["nc"]
    help_text = "Description of command"
    category = "Social"

    def execute(self, player, **kwargs):
        message = kwargs.get('args', '').strip()
        # Command logic here
        return "Result message"
```

2. Register the command in `backend/game/commands/__init__.py`:
```python
from .social import NewCommand

COMMAND_REGISTRY = {
    'newcmd': NewCommand,
    'nc': NewCommand,
}
```

#### Sending Custom WebSocket Messages

```python
from websocket.utils import send_to_player, broadcast_to_room

# Send to specific player
send_to_player(player, "Message", message_type='custom')

# Broadcast to room
broadcast_to_room(room, "Message", message_type='broadcast')
```

## Testing

### Manual Testing Checklist

- [ ] Register a new user and verify character creation
- [ ] Login and verify WebSocket connection
- [ ] Test each chat command (say, whisper, emote, shout, global)
- [ ] Verify messages appear in ChatPanel with correct formatting
- [ ] Check that username highlighting works correctly
- [ ] Verify chat filters work (All, Say, Whisper, Shout, Global)
- [ ] Confirm player stats load correctly
- [ ] Test character sheet display
- [ ] Verify real-time stat updates work

### Unit Tests

Unit tests for chat commands are located in:
- `backend/tests/test_chat_commands.py`

Run tests with:
```bash
cd backend
pytest tests/test_chat_commands.py -v
```

## Future Enhancements

- [ ] Rate limiting for commands
- [ ] Chat message persistence
- [ ] Ignore/block player feature
- [ ] Custom chat channels
- [ ] Rich text formatting
- [ ] Emote shortcuts
- [ ] Message timestamps display
- [ ] Sound notifications for messages
- [ ] Player status indicators (online/offline/busy)
- [ ] Chat command suggestions/auto-complete

## Troubleshooting

### WebSocket Connection Issues
- Verify the backend server is running
- Check that Redis is running (required for channel layers)
- Confirm the WS_URL is correctly set in frontend environment

### Chat Messages Not Appearing
- Check browser console for errors
- Verify player is authenticated
- Ensure WebSocket connection is active (check connection status in terminal)

### Stats Not Updating
- Verify `lastMessage` prop is passed to PlayerStats
- Check that player_update messages are being sent from backend
- Confirm WebSocket connection is stable

## API Reference

### Player Endpoints

#### GET /api/v1/players/me/
Get current player data.

**Response:**
```json
{
  "id": 1,
  "username": "player1",
  "character_name": "Hero",
  "level": 5,
  "experience": 1250,
  "health": 100,
  "max_health": 100,
  "mana": 80,
  "max_mana": 100
}
```

#### GET /api/v1/player/stats/
Get player statistics.

**Response:**
```json
{
  "character_name": "Hero",
  "level": 5,
  "experience": 1250,
  "health": 100,
  "max_health": 100,
  "mana": 80,
  "max_mana": 100,
  "strength": 15,
  "dexterity": 12,
  "intelligence": 10,
  "constitution": 14,
  "currency": 500,
  "inventory_count": 8,
  "inventory_size": 20
}
```

## Contributing

When contributing to the chat system or player features:

1. Follow the existing code style
2. Add unit tests for new commands
3. Update this documentation
4. Test with multiple concurrent users
5. Ensure HTML sanitization for user input
6. Update command registry when adding new commands

## License

See main project LICENSE file.
