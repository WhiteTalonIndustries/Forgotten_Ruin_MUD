# Quick Start Guide: Testing Chat and Player Features

## Prerequisites

Before testing, ensure you have:
- Python 3.8+ installed
- Node.js 14+ installed
- Redis server installed and running

## Setup Instructions

### 1. Install Backend Dependencies

```bash
cd backend
pip3 install -r requirements.txt
```

### 2. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 3. Start Redis (Required for WebSocket channels)

**macOS (using Homebrew):**
```bash
brew services start redis
```

**Linux:**
```bash
sudo systemctl start redis
```

**Windows:**
```bash
redis-server
```

### 4. Initialize Database

```bash
cd backend
python manage.py migrate
```

### 5. Create Starting Room (Optional but recommended)

```bash
cd backend
python manage.py shell
```

```python
from game.models import Room, Zone

# Create default zone
zone = Zone.objects.create(
    key='starter_zone',
    name='Starter Zone',
    description='The beginning area for new players',
    level_min=1,
    level_max=10
)

# Create starting room
room = Room.objects.create(
    key='start',
    name='Town Square',
    description='A bustling town square where adventurers gather.',
    zone=zone
)

print(f"Created starting room: {room.name}")
exit()
```

## Running the Application

### Terminal 1: Start Backend Server

```bash
cd backend
python manage.py runserver
```

Expected output:
```
Starting development server at http://127.0.0.1:8000/
```

### Terminal 2: Start Frontend Development Server

```bash
cd frontend
npm start
```

Expected output:
```
Compiled successfully!
Local: http://localhost:3000
```

## Testing the Features

### Test 1: Player Registration and Character Creation

1. Open browser to `http://localhost:3000`
2. Click "Register" or navigate to `/register`
3. Fill in the form:
   - Username: `testplayer1`
   - Email: `test1@example.com`
   - Password: `testpass123`
   - Character Name: `Hero1`
4. Click "Register"
5. **Expected Result:**
   - Redirected to login page
   - Success message displayed
   - Player character created with name "Hero1"

### Test 2: Login and WebSocket Connection

1. Navigate to `/login`
2. Enter credentials:
   - Username: `testplayer1`
   - Password: `testpass123`
3. Click "Login"
4. **Expected Result:**
   - Redirected to game page
   - WebSocket connection established (check browser console)
   - Welcome message appears in terminal
   - Player stats visible in left sidebar

### Test 3: Chat Commands

Open two browser windows side-by-side with different accounts to test chat.

#### 3a. Say Command (Room Chat)

**Window 1:**
```
say Hello from player 1!
```

**Expected Result:**
- Window 1 shows: `You say, "Hello from player 1!"`
- Window 2 shows (if in same room): `Hero1 says, "Hello from player 1!"`
- Message appears in ChatPanel with green border

#### 3b. Whisper Command (Private Message)

**Window 1:**
```
whisper Hero2 This is a private message
```

**Expected Result:**
- Window 1 shows: `You whisper to Hero2: This is a private message`
- Window 2 shows: `Hero1 whispers to you: This is a private message`
- Message appears in ChatPanel with purple border and italic text

#### 3c. Emote Command

**Window 1:**
```
emote waves enthusiastically
```

**Expected Result:**
- Both windows show: `Hero1 waves enthusiastically`
- Message appears in ChatPanel

#### 3d. Shout Command (Zone-Wide)

**Window 1:**
```
shout Can anyone hear me?
```

**Expected Result:**
- Window 1 shows: `You shout: Can anyone hear me?`
- Window 2 shows (if in same zone): `Hero1 shouts: Can anyone hear me?`
- Message appears in ChatPanel with red/orange border and bold text

#### 3e. Global Chat

**Window 1:**
```
global Anyone want to party up?
```

**Expected Result:**
- Window 1 shows: `[GLOBAL] You: Anyone want to party up?`
- Window 2 shows: `Hero1: Anyone want to party up?`
- Message appears in ChatPanel with blue border

### Test 4: Chat Panel Filters

1. Send several different types of messages (say, whisper, shout, global)
2. Click each filter button in the ChatPanel:
   - **All**: Shows all messages
   - **Say**: Shows only room chat messages
   - **Whisper**: Shows only private messages
   - **Shout**: Shows only zone-wide shouts
   - **Global**: Shows only global chat

**Expected Result:** Messages are filtered correctly based on selection

### Test 5: Player Stats Display

1. Check the left sidebar for player stats
2. Verify the following are displayed:
   - Character name
   - Level
   - Experience
   - Health bar (with current/max values)
   - Mana bar (with current/max values)
   - Strength, Dexterity, Intelligence, Constitution
   - Gold (currency)
   - Inventory count (X / Y format)

**Expected Result:** All stats display correctly with proper formatting

### Test 6: Character Sheet

1. Click the "Character Sheet" button in the header
2. **Expected Result:**
   - Modal overlay appears
   - Character sheet displays:
     - Character name and description
     - Primary stats (level, experience, health, mana)
     - Attributes (strength, dexterity, etc.)
     - Currency
     - Equipped items (if any)
     - Inventory items
     - Active quests
3. Click "Close"
4. **Expected Result:** Modal closes

### Test 7: Command History

1. In the game terminal, type several commands:
   ```
   look
   say test
   emote jumps
   ```
2. Press **Arrow Up** key multiple times
3. **Expected Result:** Previous commands appear in reverse order
4. Press **Arrow Down** key
5. **Expected Result:** Navigate forward through command history

### Test 8: WebSocket Reconnection

1. Stop the backend server (Ctrl+C in Terminal 1)
2. **Expected Result:** Terminal shows "Connecting to game server..."
3. Restart the backend server
4. **Expected Result:**
   - Connection automatically re-establishes
   - Welcome message appears again
   - Chat and commands work normally

## Common Issues and Solutions

### Issue: "WebSocket connection failed"

**Solutions:**
- Verify backend server is running on port 8000
- Check Redis is running: `redis-cli ping` (should return "PONG")
- Clear browser cache and cookies
- Check browser console for detailed error messages

### Issue: "Player not found" error

**Solutions:**
- Verify player was created during registration
- Check database:
  ```bash
  cd backend
  python manage.py shell
  ```
  ```python
  from game.models import Player
  print(Player.objects.all())
  ```
- If no players exist, re-register

### Issue: Chat messages not appearing

**Solutions:**
- Check WebSocket connection status in terminal
- Verify both players are online
- For whisper: Ensure target player name is spelled correctly
- Check browser console for JavaScript errors
- Verify ChatPanel is receiving messages (check React DevTools)

### Issue: Stats not loading

**Solutions:**
- Check API endpoint: `http://localhost:8000/api/v1/player/stats/`
- Verify authentication token is valid
- Check browser Network tab for failed requests
- Ensure player exists in database

## Testing with Python Shell

You can also test backend functionality directly:

```bash
cd backend
python manage.py shell
```

```python
from django.contrib.auth import get_user_model
from game.models import Player
from game.commands import COMMAND_REGISTRY, CommandHandler

User = get_user_model()

# Get a player
user = User.objects.get(username='testplayer1')
player = user.player

# Test a command
result = CommandHandler.handle_command(
    player,
    'say Hello from shell!',
    COMMAND_REGISTRY
)
print(result)

# Check player stats
print(f"Character: {player.character_name}")
print(f"Level: {player.level}")
print(f"Health: {player.health}/{player.max_health}")
print(f"Location: {player.location}")
```

## Running Unit Tests

```bash
cd backend
pytest tests/test_chat_commands.py -v
```

Expected output:
```
tests/test_chat_commands.py::TestSayCommand::test_say_with_message PASSED
tests/test_chat_commands.py::TestWhisperCommand::test_whisper_to_online_player PASSED
tests/test_chat_commands.py::TestEmoteCommand::test_emote_with_action PASSED
tests/test_chat_commands.py::TestShoutCommand::test_shout_in_zone PASSED
...
```

## Performance Testing

### Test with Multiple Concurrent Users

1. Open 5+ browser windows/tabs
2. Register and login with different accounts
3. Have all users send messages simultaneously
4. Verify:
   - All messages are received
   - No message loss
   - Reasonable latency (<500ms)
   - Server remains stable

### Monitor Resources

**Check Redis:**
```bash
redis-cli info stats
```

**Check WebSocket Connections:**
```bash
# In Django shell
from channels.layers import get_channel_layer
channel_layer = get_channel_layer()
# Monitor active connections
```

## Next Steps

After successful testing:

1. Review the full documentation in `CHAT_AND_PLAYER_INTEGRATION.md`
2. Explore additional game commands
3. Customize player stats and abilities
4. Add custom chat commands
5. Implement additional features

## Support

For issues or questions:
- Check the main documentation
- Review error logs in browser console and backend terminal
- Submit issues on the project repository

Happy Testing!
