# Testing Documentation

## Test Suite Overview

The test suite consists of 58 tests covering:
- **Account Management** (23 tests): Registration, login, logout, password reset, player creation
- **Chat Commands** (20 tests): Say, whisper, emote, shout commands
- **Command Registry** (3 tests): Command registration and aliases
- **WebSocket Utilities** (3 tests): Message sending and broadcasting
- **WebSocket Integration** (10 tests): Async WebSocket connections and real-time messaging

## Running Tests

### Quick Start (SQLite - Default)

```bash
./test.sh all
```

This runs all tests using SQLite in-memory database. **48 out of 58 tests pass** with this configuration.

### With PostgreSQL (Recommended for Full Coverage)

To run all tests including async WebSocket tests:

1. **Install PostgreSQL** (if not already installed):
   ```bash
   brew install postgresql@14
   brew services start postgresql@14
   ```

2. **Create test database and user**:
   ```bash
   createdb test_forgotten_ruin
   ```

3. **Run tests with PostgreSQL**:
   ```bash
   USE_POSTGRES_FOR_TESTS=1 ./test.sh all
   ```

## Test Results

### With SQLite (Default)
- ✅ **48 tests passing** (83% pass rate)
- ❌ **10 async WebSocket tests failing** due to SQLite concurrency limitations

### With PostgreSQL
- ✅ **All 58 tests should pass**
- Async tests work properly with PostgreSQL's better concurrency support

## Known Issues

### SQLite Async Test Failures

The following 10 tests fail with SQLite due to database locking issues:
- `test_connect_with_valid_token`
- `test_player_marked_online_on_connect`
- `test_player_marked_offline_on_disconnect`
- `test_send_command`
- `test_ping_pong`
- `test_global_chat_message`
- `test_multiple_clients_global_chat`
- `test_room_broadcast_to_multiple_players`
- `test_join_room_group`
- `test_join_zone_group`

**Cause**: SQLite doesn't handle concurrent writes well in async contexts when using `database_sync_to_async()`.

**Solution**: Use PostgreSQL for testing (see above) or skip async tests:
```bash
pytest -m "not asyncio"
```

## Test Organization

```
tests/
├── conftest.py           # Shared fixtures (users, players, rooms, etc.)
├── test_accounts.py      # Account management tests
├── test_chat_commands.py # Chat command tests
└── test_websocket.py     # WebSocket integration tests
```

## Key Fixtures

- `api_client`: REST API test client
- `user`: Test user account
- `player`: Test player character
- `room`: Test game room
- `zone`: Test game zone
- `authenticated_client`: Pre-authenticated API client

## Configuration Files

- `pytest.ini`: Pytest configuration
- `server/test_settings.py`: Django settings for testing
- `conftest.py`: Shared test fixtures

## Environment Variables

- `USE_POSTGRES_FOR_TESTS`: Set to '1' to use PostgreSQL instead of SQLite
- `DB_USER`: Database user (default: 'postgres')
- `DB_PASSWORD`: Database password (default: '')
- `DB_HOST`: Database host (default: 'localhost')
- `DB_PORT`: Database port (default: '5432')
