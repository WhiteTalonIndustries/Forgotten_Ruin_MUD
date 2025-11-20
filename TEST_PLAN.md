# Forgotten Ruin MUD - Test Plan

## Overview
This document outlines the testing strategy for the user account creation and chat features implemented in the Forgotten Ruin MUD project.

## Test Scope

### In Scope
- User registration and account creation
- User login and authentication
- Password reset functionality
- Player character auto-creation
- WebSocket connections
- Chat commands (say, whisper, emote, shout)
- Room broadcasts
- Zone broadcasts
- Direct player messaging
- Chat panel UI functionality

### Out of Scope
- Combat system
- Quest system
- NPC interactions
- World generation
- Advanced game mechanics

## Test Levels

### 1. Unit Tests
- Backend API endpoints
- Serializers
- WebSocket utilities
- Command handlers
- Model methods

### 2. Integration Tests
- WebSocket message flow
- Database operations
- Authentication flow
- Command execution pipeline

### 3. End-to-End Tests
- Complete user registration flow
- Login to game flow
- Multi-player chat scenarios

### 4. Manual Tests
- UI/UX verification
- Visual testing
- Edge cases
- Performance under load

## Test Environment

### Prerequisites
- Python 3.10+
- PostgreSQL 13+ (running)
- Redis 6+ (running)
- Node.js 16+
- All dependencies installed

### Test Database
- Use separate test database: `forgotten_ruin_test`
- Isolated from development data
- Clean state before each test run

## Test Cases

### A. User Account Tests

#### A1. User Registration
| Test ID | Description | Steps | Expected Result |
|---------|-------------|-------|-----------------|
| REG-001 | Valid registration | POST /auth/register/ with valid data | 201 Created, user & player created, token returned |
| REG-002 | Duplicate username | Register with existing username | 400 Bad Request, error message |
| REG-003 | Duplicate email | Register with existing email | 400 Bad Request, error message |
| REG-004 | Password mismatch | password != password_confirm | 400 Bad Request, validation error |
| REG-005 | Weak password | Password < 12 chars | 400 Bad Request, validation error |
| REG-006 | Invalid email | Invalid email format | 400 Bad Request, validation error |
| REG-007 | Custom character name | Provide character_name field | Character created with custom name |
| REG-008 | Missing character name | Omit character_name field | Character created with username |

#### A2. User Login
| Test ID | Description | Steps | Expected Result |
|---------|-------------|-------|-----------------|
| LOG-001 | Valid login | POST /auth/login/ with correct credentials | 200 OK, token returned |
| LOG-002 | Invalid username | Login with non-existent username | 401 Unauthorized |
| LOG-003 | Invalid password | Login with wrong password | 401 Unauthorized |
| LOG-004 | Case sensitivity | Test username case variations | Should match exact case |

#### A3. Password Reset
| Test ID | Description | Steps | Expected Result |
|---------|-------------|-------|-----------------|
| PWD-001 | Request reset | POST /auth/password-reset/ with email | 200 OK, token generated |
| PWD-002 | Invalid email | Request reset for non-existent email | 200 OK (don't reveal) |
| PWD-003 | Confirm reset | POST /auth/password-reset-confirm/ with valid token | 200 OK, password changed |
| PWD-004 | Invalid token | Confirm with invalid token | 400 Bad Request |
| PWD-005 | Expired token | Use old token | 400 Bad Request |

#### A4. Player Character Creation
| Test ID | Description | Steps | Expected Result |
|---------|-------------|-------|-----------------|
| PLR-001 | Auto-creation on register | Register new user | Player object created |
| PLR-002 | Starting location | Check player.location | Set to starting room if exists |
| PLR-003 | Default stats | Check player stats | Health=100, Mana=100, Level=1 |
| PLR-004 | One-to-one relationship | Check user.player | Single player per user |

### B. Chat & WebSocket Tests

#### B1. WebSocket Connection
| Test ID | Description | Steps | Expected Result |
|---------|-------------|-------|-----------------|
| WS-001 | Connect with valid token | Connect to /ws/game/?token=<valid> | Connection accepted |
| WS-002 | Connect without token | Connect without token parameter | Connection rejected |
| WS-003 | Connect with invalid token | Connect with bad token | Connection rejected |
| WS-004 | Receive welcome message | Connect successfully | Welcome message received |
| WS-005 | Join room group | Connect with player in room | Added to room group |
| WS-006 | Join player group | Connect successfully | Added to personal group |
| WS-007 | Join zone group | Connect with player in zone | Added to zone group |
| WS-008 | Disconnect cleanup | Disconnect WebSocket | Player marked offline, left groups |

#### B2. Say Command (Room Broadcast)
| Test ID | Description | Steps | Expected Result |
|---------|-------------|-------|-----------------|
| SAY-001 | Say in room | Execute "say Hello" | Message broadcast to room |
| SAY-002 | Say excludes sender | Check received messages | Sender sees own message differently |
| SAY-003 | Empty say | Execute "say" with no message | Error: "Say what?" |
| SAY-004 | HTML sanitization | Execute 'say <script>alert()</script>' | Script tags escaped |
| SAY-005 | Multiple players | 3 players in room, one says | Other 2 receive message |

#### B3. Whisper Command (Direct Message)
| Test ID | Description | Steps | Expected Result |
|---------|-------------|-------|-----------------|
| WHI-001 | Whisper to online player | Execute "whisper Bob Hello" | Bob receives whisper |
| WHI-002 | Whisper to offline player | Whisper to offline player | Error: player not online |
| WHI-003 | Whisper to non-existent | Whisper to fake name | Error: player not online |
| WHI-004 | Empty whisper | Execute "whisper Bob" | Error: usage message |
| WHI-005 | Case insensitive target | "whisper bob" vs "whisper Bob" | Should work (case insensitive) |

#### B4. Emote Command
| Test ID | Description | Steps | Expected Result |
|---------|-------------|-------|-----------------|
| EMO-001 | Valid emote | Execute "emote waves" | "PlayerName waves" broadcast |
| EMO-002 | Empty emote | Execute "emote" | Error: "Emote what?" |
| EMO-003 | Emote in room | Multiple players present | All players see emote |

#### B5. Shout Command (Zone Broadcast)
| Test ID | Description | Steps | Expected Result |
|---------|-------------|-------|-----------------|
| SHO-001 | Shout in zone | Execute "shout Help!" | All zone players receive |
| SHO-002 | Empty shout | Execute "shout" | Error: "Shout what?" |
| SHO-003 | No location | Player not in room | Error: "shout into void" |
| SHO-004 | Cross-room shout | Players in different rooms, same zone | All receive shout |

#### B6. Chat Panel UI
| Test ID | Description | Steps | Expected Result |
|---------|-------------|-------|-----------------|
| UI-001 | Display say messages | Receive broadcast message | Shows in chat panel with [SAY] |
| UI-002 | Display whispers | Receive whisper | Shows in chat with [WHISPER] |
| UI-003 | Display shouts | Receive shout | Shows in chat with [SHOUT] |
| UI-004 | Message filtering | Click "Whisper" filter | Only whispers shown |
| UI-005 | Clear chat | Click clear button | All messages removed |
| UI-006 | Color coding | Check message colors | Different colors per type |
| UI-007 | Auto-scroll | Receive many messages | Scrolls to bottom |

### C. Integration Tests

#### C1. End-to-End User Flow
| Test ID | Description | Steps | Expected Result |
|---------|-------------|-------|-----------------|
| E2E-001 | Register to game | Register → Login → Connect WS → Send command | Full flow works |
| E2E-002 | Two player chat | 2 users register, login, connect, say | Both see messages |
| E2E-003 | Whisper between players | User A whispers to User B | Only B receives whisper |
| E2E-004 | Zone-wide communication | 3 players in same zone, one shouts | All 3 receive shout |

### D. Performance Tests

#### D1. Load Testing
| Test ID | Description | Steps | Expected Result |
|---------|-------------|-------|---|
| PERF-001 | 10 concurrent connections | Connect 10 WebSockets | All connect successfully |
| PERF-002 | 100 messages/second | Broadcast 100 msgs/sec | All delivered, <1s latency |
| PERF-003 | 50 concurrent users | 50 users in same room | Room broadcasts work |

## Test Data Requirements

### Users
- Minimum 5 test users with various configurations
- Mix of with/without custom character names
- Known credentials for automated testing

### World Data
- Starting room (key='start')
- At least 1 zone with multiple rooms
- Connected rooms with exits

### Test Accounts
```
Username: testuser1, Password: TestPassword123!, Email: test1@example.com
Username: testuser2, Password: TestPassword123!, Email: test2@example.com
Username: testuser3, Password: TestPassword123!, Email: test3@example.com
```

## Test Execution

### Automated Tests
```bash
# Backend unit tests
cd backend
pytest tests/unit/

# Backend integration tests
pytest tests/integration/

# Run all tests with coverage
pytest --cov=. --cov-report=html
```

### Manual Tests
Follow the manual test checklist in `tests/MANUAL_TESTS.md`

## Success Criteria

- All unit tests pass (>95% coverage)
- All integration tests pass
- Critical E2E flows work without errors
- No memory leaks in WebSocket connections
- Chat messages delivered within 100ms
- UI responsive and visually correct

## Bug Reporting

### Bug Template
```
ID: BUG-XXX
Title: [Brief description]
Severity: Critical/High/Medium/Low
Steps to Reproduce:
1.
2.
Expected Result:
Actual Result:
Environment:
Additional Notes:
```

## Test Schedule

- Day 1: Setup test environment, run unit tests
- Day 2: Run integration tests, fix critical issues
- Day 3: Manual testing, UI/UX verification
- Day 4: Performance testing, stress testing
- Day 5: Regression testing, documentation

## Tools & Frameworks

- **pytest**: Python unit/integration testing
- **pytest-django**: Django test utilities
- **pytest-asyncio**: Async test support
- **factory_boy**: Test data generation
- **websockets**: WebSocket testing client
- **Jest**: Frontend unit tests
- **React Testing Library**: Component tests
- **Postman/curl**: API testing
- **Redis Commander**: Redis inspection

## Notes

- Always use test database
- Clean up test data after runs
- Mock external services
- Test in isolation when possible
- Document any manual setup required
