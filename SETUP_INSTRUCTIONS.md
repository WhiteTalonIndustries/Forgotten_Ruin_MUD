# Setup Instructions for Forgotten Ruin MUD

## ✅ What's Been Done

All testing infrastructure has been created:
- 75+ automated tests
- Test data generation scripts
- Manual testing checklists
- Complete test documentation
- Setup and test runner scripts

## 🚀 Quick Start (3 Steps)

### Step 1: Install PostgreSQL and Redis

**macOS (with Homebrew):**
```bash
# Install
brew install postgresql@13 redis

# Start services
brew services start postgresql@13
brew services start redis

# Add PostgreSQL to PATH (for Apple Silicon Macs)
echo 'export PATH="/opt/homebrew/opt/postgresql@13/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verify
psql --version
redis-cli ping  # Should return PONG

# Create databases
psql postgres -c "CREATE DATABASE forgotten_ruin;"
psql postgres -c "CREATE DATABASE forgotten_ruin_test;"
```

**Don't have Homebrew or not on macOS?** See [PREREQUISITES.md](PREREQUISITES.md)

### Step 2: Run Setup Script

```bash
# From anywhere in the project
./scripts/setup_test_environment.sh
```

This will:
- Install Python and Node.js dependencies
- Create virtual environment
- Run database migrations
- Generate test data
- Create .env files

### Step 3: Start Development

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python manage.py runserver
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

**Terminal 3 - Run Tests:**
```bash
./test.sh all
```

Visit: http://localhost:3000

## 📝 Test Accounts

All accounts use password: `TestPassword123!`

| Username | Email |
|----------|-------|
| testuser1 | test1@example.com |
| testuser2 | test2@example.com |
| alice | alice@example.com |
| bob | bob@example.com |

## 🧪 Running Tests

```bash
# All tests
./test.sh all

# Specific suites
./test.sh accounts      # User account tests (35+ tests)
./test.sh chat          # Chat command tests (25+ tests)
./test.sh websocket     # WebSocket tests (15+ tests)

# With coverage
./test.sh coverage

# Quick smoke tests
./test.sh quick
```

## 📚 Documentation

| File | Description |
|------|-------------|
| [PREREQUISITES.md](PREREQUISITES.md) | How to install PostgreSQL, Redis |
| [TESTING_QUICK_START.md](TESTING_QUICK_START.md) | Quick testing guide |
| [DEVELOPMENT.md](DEVELOPMENT.md) | Development workflow |
| [TEST_PLAN.md](TEST_PLAN.md) | Comprehensive test plan |
| [tests/MANUAL_TESTS.md](tests/MANUAL_TESTS.md) | Manual testing procedures |

## ⚠️ Troubleshooting

### "psql: command not found"

PostgreSQL not in PATH. Add to ~/.zshrc:
```bash
# Apple Silicon Mac
echo 'export PATH="/opt/homebrew/opt/postgresql@13/bin:$PATH"' >> ~/.zshrc

# Intel Mac
echo 'export PATH="/usr/local/opt/postgresql@13/bin:$PATH"' >> ~/.zshrc

source ~/.zshrc
```

### "redis-cli: command not found"

Install Redis:
```bash
brew install redis
brew services start redis
```

### "Virtual environment not found"

Run setup script:
```bash
./scripts/setup_test_environment.sh
```

### Database connection errors

Make sure PostgreSQL is running:
```bash
# Check status
brew services list

# Start if needed
brew services start postgresql@13
```

### Tests failing

Regenerate test data:
```bash
cd backend
source venv/bin/activate
python manage.py shell < tests/generate_test_data.py
```

## 🎯 What to Test

### Quick Test (2 minutes)

1. Register new account at http://localhost:3000/register
2. Login with test account
3. Open two browser windows
4. Chat between windows using `say Hello!`

### Full Test (15 minutes)

Follow the manual testing checklist:
```bash
open tests/MANUAL_TESTS.md
```

### Automated Tests (30 seconds)

```bash
./test.sh quick  # Smoke tests
./test.sh all    # All tests (~2 minutes)
```

## 📂 Project Structure

```
Forgotten_Ruin_MUD/
├── backend/                    # Django backend
│   ├── tests/                 # 75+ automated tests ✅
│   │   ├── test_accounts.py   # User account tests
│   │   ├── test_chat_commands.py # Chat tests
│   │   └── test_websocket.py  # WebSocket tests
│   └── ...
│
├── frontend/                  # React frontend
│   └── src/
│       ├── components/       # ChatPanel ✅
│       └── pages/           # Login, Register ✅
│
├── scripts/
│   ├── setup_test_environment.sh ✅
│   └── run_tests.sh         ✅
│
├── tests/
│   ├── MANUAL_TESTS.md      # Manual test procedures ✅
│   └── README.md            # Testing guide ✅
│
├── test.sh                   # Quick test runner ✅
├── TEST_PLAN.md             # Master test plan ✅
├── TESTING_QUICK_START.md   # Quick reference ✅
├── PREREQUISITES.md         # Installation guide ✅
└── DEVELOPMENT.md           # Dev workflow ✅
```

## ✨ Features Implemented

### Backend
- ✅ User registration with validation
- ✅ Login/logout with token auth
- ✅ Password reset system
- ✅ Auto-creation of player characters
- ✅ WebSocket real-time communication
- ✅ Chat commands (say, whisper, emote, shout)
- ✅ Room/zone broadcasting
- ✅ Direct messaging

### Frontend
- ✅ Registration page with character name
- ✅ Login page
- ✅ Game terminal
- ✅ Chat panel with filtering
- ✅ WebSocket integration
- ✅ Color-coded message types

### Testing
- ✅ 35+ user account tests
- ✅ 25+ chat command tests
- ✅ 15+ WebSocket integration tests
- ✅ Manual testing checklist
- ✅ Test data generator
- ✅ Automated setup scripts

## 🎉 You're Ready!

Everything is set up. Just install PostgreSQL/Redis and run:

```bash
./scripts/setup_test_environment.sh
```

Then start developing! 🚀

For questions, see [DEVELOPMENT.md](DEVELOPMENT.md) or [TESTING_QUICK_START.md](TESTING_QUICK_START.md)
