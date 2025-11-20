# Manual Testing Checklist

This document provides step-by-step instructions for manually testing the user account and chat features.

## Prerequisites

Before starting manual tests:
- [ ] Backend server is running (`python manage.py runserver`)
- [ ] Frontend server is running (`npm start`)
- [ ] PostgreSQL is running
- [ ] Redis is running
- [ ] Test data has been generated (`python manage.py shell < tests/generate_test_data.py`)

## Test Environment Setup

### Check Services Status

```bash
# Check PostgreSQL
psql -U postgres -c "SELECT version();"

# Check Redis
redis-cli ping

# Check Backend
curl http://localhost:8000/api/v1/

# Check Frontend
curl http://localhost:3000/
```

---

## Section A: User Registration

### Test A1: Valid Registration

**Objective**: Verify a new user can successfully register

**Steps**:
1. Open browser to `http://localhost:3000/register`
2. Enter the following information:
   - Username: `manual_test_user1`
   - Email: `manual1@example.com`
   - Character Name: `Tester1` (optional)
   - Password: `TestPassword123!`
   - Confirm Password: `TestPassword123!`
3. Click "Register" button

**Expected Result**:
- [✓] Form submits without errors
- [✓] Redirected to game page (`/game`)
- [✓] Welcome message appears in terminal
- [✓] Player stats visible in sidebar
- [✓] Character name shows as "Tester1"

---

### Test A2: Registration Validation

**Objective**: Verify form validates input correctly

**Test Cases**:

#### A2.1: Duplicate Username
1. Navigate to `/register`
2. Try to register with username: `testuser1` (already exists)
3. **Expected**: Error message "username already exists"

#### A2.2: Duplicate Email
1. Navigate to `/register`
2. Try to register with email: `test1@example.com` (already exists)
3. **Expected**: Error message "email already in use"

#### A2.3: Password Mismatch
1. Navigate to `/register`
2. Enter different passwords in password fields
3. **Expected**: Error message "passwords do not match"

#### A2.4: Weak Password
1. Navigate to `/register`
2. Enter password: `weak`
3. **Expected**: Error message about password requirements

#### A2.5: Invalid Email
1. Navigate to `/register`
2. Enter email: `not-an-email`
3. **Expected**: Error message "invalid email"

**Results**:
- [ ] A2.1 Passed
- [ ] A2.2 Passed
- [ ] A2.3 Passed
- [ ] A2.4 Passed
- [ ] A2.5 Passed

---

## Section B: User Login

### Test B1: Valid Login

**Objective**: Verify existing user can login

**Steps**:
1. Open browser to `http://localhost:3000/login`
2. Enter credentials:
   - Username: `testuser1`
   - Password: `TestPassword123!`
3. Click "Login" button

**Expected Result**:
- [✓] Login successful
- [✓] Redirected to `/game`
- [✓] WebSocket connects
- [✓] Welcome message displayed
- [✓] Room description displayed

---

### Test B2: Invalid Login

#### B2.1: Wrong Password
1. Navigate to `/login`
2. Username: `testuser1`, Password: `WrongPassword`
3. **Expected**: Error "Invalid credentials"

#### B2.2: Non-existent User
1. Navigate to `/login`
2. Username: `fake_user`, Password: `anything`
3. **Expected**: Error "Invalid credentials"

**Results**:
- [ ] B2.1 Passed
- [ ] B2.2 Passed

---

## Section C: WebSocket Connection

### Test C1: Connection Status

**Objective**: Verify WebSocket connects properly

**Steps**:
1. Login as `testuser1`
2. Open browser DevTools (F12)
3. Go to Network tab
4. Filter by WS (WebSocket)
5. Observe connection to `ws://localhost:8000/ws/game/`

**Expected Result**:
- [✓] WebSocket connection established (status 101)
- [✓] Connection shows as "Open" in DevTools
- [✓] No "Connecting..." message in UI
- [✓] Terminal is enabled and accepting input

---

### Test C2: Reconnection

**Objective**: Verify auto-reconnect works

**Steps**:
1. Login as `testuser1`
2. In DevTools Network tab, find WebSocket connection
3. Stop backend server (`Ctrl+C`)
4. Observe connection status
5. Restart backend server
6. Wait 3-5 seconds

**Expected Result**:
- [✓] "Connecting..." message appears when disconnected
- [✓] Terminal input disabled during disconnect
- [✓] Automatically reconnects when server is back
- [✓] Terminal re-enabled after reconnect

---

## Section D: Chat Commands

### Test D1: Say Command (Room Broadcast)

**Objective**: Test room-wide communication

**Setup**: Open two browser windows
- Window 1: Login as `testuser1`
- Window 2: Login as `testuser2`

**Steps**:
1. In Window 1, type in terminal: `say Hello everyone!`
2. Press Enter
3. Observe both windows

**Expected Result**:
- [✓] Window 1 shows: `You say, "Hello everyone!"`
- [✓] Window 2 shows: `testuser1 says, "Hello everyone!"`
- [✓] Message appears in Chat Panel with [SAY] prefix
- [✓] Message is green colored

---

### Test D2: Whisper Command (Direct Message)

**Setup**: Two browser windows logged in as different users

**Steps**:
1. In Window 1 (testuser1), type: `whisper testuser2 This is a secret`
2. Press Enter
3. Observe both windows

**Expected Result**:
- [✓] Window 1 shows: `You whisper to testuser2: This is a secret`
- [✓] Window 2 shows: `testuser1 whispers to you: This is a secret`
- [✓] Message in Chat Panel has [WHISPER] prefix
- [✓] Message is purple/magenta colored
- [✓] No other players see the message

---

### Test D3: Emote Command

**Setup**: Two browser windows logged in

**Steps**:
1. In Window 1, type: `emote waves cheerfully`
2. Press Enter
3. Observe both windows

**Expected Result**:
- [✓] Window 1 shows: `testuser1 waves cheerfully`
- [✓] Window 2 shows: `testuser1 waves cheerfully`
- [✓] Message appears in Chat Panel

---

### Test D4: Shout Command (Zone Broadcast)

**Setup**: Multiple players in same zone but different rooms

**Steps**:
1. Window 1 (testuser1): Ensure in same zone
2. Window 2 (testuser2): Move to different room in same zone
3. In Window 1, type: `shout Can anyone hear me?`
4. Press Enter

**Expected Result**:
- [✓] Window 1 shows: `You shout: Can anyone hear me?`
- [✓] Window 2 shows: `testuser1 shouts: Can anyone hear me?`
- [✓] Message in Chat Panel has [SHOUT] prefix
- [✓] Message is red/orange colored
- [✓] Players in different zones don't see it

---

## Section E: Chat Panel UI

### Test E1: Message Display

**Steps**:
1. Login and navigate to game
2. Execute various chat commands (say, whisper, shout)
3. Observe Chat Panel on right side

**Expected Result**:
- [✓] Chat Panel is visible
- [✓] Messages appear in chronological order
- [✓] Each message type has distinct color
- [✓] [SAY] messages are green
- [✓] [WHISPER] messages are purple
- [✓] [SHOUT] messages are red/orange
- [✓] Auto-scrolls to bottom

---

### Test E2: Message Filtering

**Steps**:
1. Generate mix of different message types
2. Click "Say" filter button
3. Click "Whisper" filter button
4. Click "Shout" filter button
5. Click "All" filter button

**Expected Result**:
- [✓] Say filter shows only say messages
- [✓] Whisper filter shows only whispers
- [✓] Shout filter shows only shouts
- [✓] All filter shows all messages
- [✓] Active filter button is highlighted

---

### Test E3: Clear Chat

**Steps**:
1. Have several messages in chat panel
2. Click "Clear" button

**Expected Result**:
- [✓] All messages removed from chat panel
- [✓] "No messages yet..." appears
- [✓] Terminal messages unaffected

---

## Section F: Multi-User Scenarios

### Test F1: Three Player Chat

**Setup**: Open three browser windows
- Window 1: `alice`
- Window 2: `bob`
- Window 3: `testuser1`

**Steps**:
1. All three users in same room
2. Alice: `say Hello Bob and testuser1!`
3. Bob: `say Hi Alice!`
4. testuser1: `emote waves at everyone`
5. Alice: `whisper bob Want to team up?`

**Expected Result**:
- [✓] All three see say messages from each other
- [✓] All three see emote
- [✓] Only Bob sees whisper from Alice
- [✓] Messages appear in correct order
- [✓] No message duplication

---

### Test F2: Cross-Room Communication

**Setup**: Two users in different rooms, same zone

**Steps**:
1. User1: Starting Room
2. User2: Training Grounds
3. User1: `say Hello` (should only be in User1's room)
4. User1: `shout Can anyone hear me?` (should reach User2)
5. User2: `shout I hear you!` (should reach User1)

**Expected Result**:
- [✓] Say messages only in same room
- [✓] Shout messages reach across rooms in zone
- [✓] Both users see shouts in chat panel

---

## Section G: Password Reset

### Test G1: Request Password Reset

**Steps**:
1. Navigate to `/login`
2. Click "Forgot Password" (if link exists) or go to password reset endpoint
3. Enter email: `test1@example.com`
4. Submit form

**Expected Result**:
- [✓] Success message displayed
- [✓] (In dev mode) Reset token shown in response
- [✓] (In production) Email would be sent

---

### Test G2: Complete Password Reset

**Steps**:
1. Request password reset for `test1@example.com`
2. Copy reset token and UID from response
3. Navigate to password reset confirm page
4. Enter token, UID, and new password
5. Submit

**Expected Result**:
- [✓] Success message
- [✓] New token returned
- [✓] Can login with new password
- [✓] Old password no longer works

---

## Section H: Edge Cases & Error Handling

### Test H1: Special Characters in Chat

**Steps**:
1. Try: `say Hello with special chars: !@#$%^&*()`
2. Try: `say <script>alert('xss')</script>`
3. Try: `say Multi\nLine\nText`

**Expected Result**:
- [✓] Special characters display correctly
- [✓] HTML/script tags are escaped
- [✓] No XSS vulnerability
- [✓] Line breaks handled gracefully

---

### Test H2: Very Long Messages

**Steps**:
1. Type a message longer than 1000 characters
2. Submit command

**Expected Result**:
- [✓] Message either sent successfully or
- [✓] Error message about length limit
- [✓] No crash or hang

---

### Test H3: Rapid Fire Commands

**Steps**:
1. Type and submit commands very quickly (10+ in 5 seconds)

**Expected Result**:
- [✓] All commands processed or
- [✓] Rate limiting message shown
- [✓] No commands lost
- [✓] No server crash

---

### Test H4: Offline/Online Status

**Steps**:
1. User1 and User2 online
2. User1: `whisper user2 test`
3. User2 disconnects (close browser)
4. User1: `whisper user2 another test`
5. User2 reconnects

**Expected Result**:
- [✓] First whisper delivered
- [✓] Second whisper shows "not online"
- [✓] User marked offline when disconnected
- [✓] User marked online when reconnected

---

## Section I: Performance & Load

### Test I1: Multiple Simultaneous Users

**Steps**:
1. Open 5-10 browser windows
2. Login with different test accounts
3. All send messages rapidly

**Expected Result**:
- [✓] All users can connect
- [✓] Messages delivered to all users
- [✓] No significant lag (<1 second)
- [✓] No crashes

---

### Test I2: Long Session

**Steps**:
1. Login and stay connected for 30+ minutes
2. Periodically send messages

**Expected Result**:
- [✓] Connection stays stable
- [✓] No disconnects
- [✓] No memory leaks (check browser memory)

---

## Summary Checklist

### Critical Tests (Must Pass)
- [ ] User registration works
- [ ] User login works
- [ ] WebSocket connects
- [ ] Say command works
- [ ] Whisper command works
- [ ] Chat panel displays messages
- [ ] Multiple users can chat

### Important Tests (Should Pass)
- [ ] Input validation working
- [ ] HTML sanitization working
- [ ] Message filtering works
- [ ] Zone broadcasts work
- [ ] Password reset works

### Nice to Have (Can fail without blocking)
- [ ] Auto-reconnect works
- [ ] Performance under load
- [ ] Long session stability

---

## Bug Reporting

If any test fails, document using this template:

```
TEST: [Test ID]
STATUS: FAIL
EXPECTED: [What should happen]
ACTUAL: [What actually happened]
STEPS TO REPRODUCE:
1.
2.
3.

BROWSER: [Chrome/Firefox/Safari]
CONSOLE ERRORS: [Any JavaScript errors]
NETWORK ERRORS: [Any failed requests]
SCREENSHOTS: [Attach if applicable]
```

---

## Notes

- Always test in a clean browser session (incognito/private mode) to avoid cache issues
- Check browser console for any JavaScript errors
- Check backend console for any server errors
- Monitor Redis and PostgreSQL logs during testing
- Take screenshots of any visual issues

Good luck testing! 🧪
