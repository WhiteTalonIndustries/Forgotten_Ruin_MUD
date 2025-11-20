# Testing Quick Start Guide

## Prerequisites

- Python 3.10+
- Node.js 16+
- PostgreSQL 13+ (running)
- Redis 6+ (running)

## One-Time Setup

```bash
# Option 1: From project root
./scripts/setup_test_environment.sh

# Option 2: From scripts directory
cd scripts
./setup_test_environment.sh

# The script works from anywhere!
```

**Note:** If you don't have PostgreSQL and Redis installed yet, see [PREREQUISITES.md](PREREQUISITES.md) first.

This will:
- Install Python and Node dependencies
- Create test database
- Run migrations
- Generate test data (users, rooms, zones)
- Create test credentials file

## Running Tests

### Automated Tests

```bash
# Quick way (from project root)
./test.sh all

# Or use the full script path
./scripts/run_tests.sh all

# Run specific suites
./test.sh accounts      # User account tests
./test.sh chat          # Chat command tests
./test.sh websocket     # WebSocket integration tests
./test.sh unit          # All unit tests
./test.sh integration   # All integration tests

# Run with coverage
./test.sh coverage

# Quick smoke tests
./test.sh quick
```

**The scripts work from any directory!** You can run them from project root, scripts folder, or even backend folder.

### Manual Tests

```bash
# 1. Start backend (Terminal 1)
cd backend
source venv/bin/activate
python manage.py runserver

# 2. Start frontend (Terminal 2)
cd frontend
npm start

# 3. Open browser to http://localhost:3000

# 4. Follow manual test checklist
open tests/MANUAL_TESTS.md
```

## Test Accounts

| Username | Password |
|----------|----------|
| testuser1 | TestPassword123! |
| testuser2 | TestPassword123! |
| testuser3 | TestPassword123! |
| alice | TestPassword123! |
| bob | TestPassword123! |

## Quick Testing Scenarios

### Test 1: User Registration
1. Go to http://localhost:3000/register
2. Register with username `mytest`, email `mytest@example.com`, password `TestPassword123!`
3. Should redirect to game and show welcome message

### Test 2: Two-Player Chat
1. Open two browser windows
2. Window 1: Login as `testuser1`
3. Window 2: Login as `testuser2`
4. Window 1: Type `say Hello!`
5. Both windows should show the message

### Test 3: Direct Message
1. Two players logged in (same room)
2. Player 1: Type `whisper testuser2 Secret message`
3. Only Player 2 should see the whisper

## File Organization

```
Forgotten_Ruin_MUD/
├── TEST_PLAN.md                   # Comprehensive test plan
├── TESTING_QUICK_START.md         # This file
├── TEST_CREDENTIALS.txt           # Auto-generated credentials
│
├── tests/
│   ├── README.md                  # Testing guide
│   └── MANUAL_TESTS.md            # Detailed manual test steps
│
├── backend/tests/
│   ├── conftest.py                # Test fixtures
│   ├── test_accounts.py           # Account tests (35+ tests)
│   ├── test_chat_commands.py      # Chat tests (25+ tests)
│   ├── test_websocket.py          # WebSocket tests (15+ tests)
│   └── generate_test_data.py      # Test data generator
│
└── scripts/
    ├── setup_test_environment.sh  # Setup script
    └── run_tests.sh               # Test runner
```

## Troubleshooting

### Redis not running
```bash
# macOS
brew services start redis

# Linux
sudo service redis-server start

# Verify
redis-cli ping  # Should return PONG
```

### PostgreSQL not running
```bash
# macOS
brew services start postgresql

# Linux  
sudo service postgresql start
```

### Tests failing
```bash
# Regenerate test data
cd backend
source venv/bin/activate
python manage.py shell < tests/generate_test_data.py
```

### WebSocket tests failing
```bash
# Ensure Redis is running
redis-cli ping

# Install async test dependencies
pip install pytest-asyncio channels-redis
```

## Next Steps

- Review [TEST_PLAN.md](TEST_PLAN.md) for comprehensive testing strategy
- Follow [tests/MANUAL_TESTS.md](tests/MANUAL_TESTS.md) for step-by-step manual tests
- Check coverage report: `./scripts/run_tests.sh coverage`

## Support

- Issues? Check logs in backend terminal
- WebSocket issues? Verify Redis is running
- Database issues? Check PostgreSQL is running
- All services status: `./scripts/setup_test_environment.sh --help`

Happy testing! 🧪
