# System Architecture

High-level architecture overview for Forgotten Ruin MUD.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Layer                         │
├─────────────────────────────────────────────────────────────┤
│  Web Browser (React)                                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  UI Pages    │  │  Components  │  │  Styles      │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│         │                  │                                │
│         v                  v                                │
│  ┌──────────────────────────────────────────┐              │
│  │  Services (API + WebSocket)              │              │
│  └──────────────────────────────────────────┘              │
└────────────────┬────────────────┬───────────────────────────┘
                 │ HTTP/REST      │ WebSocket
                 v                v
┌─────────────────────────────────────────────────────────────┐
│                     Application Layer                       │
├─────────────────────────────────────────────────────────────┤
│  ASGI Server (Daphne/Uvicorn)                              │
│                                                             │
│  ┌─────────────────────┐   ┌──────────────────────────┐   │
│  │   Django Channels   │   │   Django REST Framework  │   │
│  │   (WebSocket)       │   │   (HTTP API)             │   │
│  └─────────────────────┘   └──────────────────────────┘   │
│            │                           │                    │
│            v                           v                    │
│  ┌────────────────────────────────────────────────┐       │
│  │         Business Logic Layer                    │       │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐       │       │
│  │  │  Game    │ │  Combat  │ │  World   │       │       │
│  │  │  Logic   │ │  System  │ │  Manager │       │       │
│  │  └──────────┘ └──────────┘ └──────────┘       │       │
│  └────────────────────────────────────────────────┘       │
│                          │                                  │
│                          v                                  │
│  ┌────────────────────────────────────────────────┐       │
│  │         Django ORM (Data Access)                │       │
│  └────────────────────────────────────────────────┘       │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            v
┌─────────────────────────────────────────────────────────────┐
│                      Data Layer                             │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐         ┌──────────────────┐         │
│  │   PostgreSQL     │         │      Redis       │         │
│  │  (Game Data)     │         │  (Sessions,      │         │
│  │                  │         │   Channels)      │         │
│  └──────────────────┘         └──────────────────┘         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                  Background Tasks Layer                     │
├─────────────────────────────────────────────────────────────┤
│                    Celery Workers                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Game Tick   │  │  NPC AI      │  │  World       │     │
│  │  (1 second)  │  │  Updates     │  │  Events      │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## Component Overview

### Frontend (React)

**Purpose**: User interface for the game

**Key Components**:
- Pages: Home, Login, Register, Game
- Components: GameTerminal, PlayerStats
- Services: API client, WebSocket hooks
- Routing: React Router for navigation

**Communication**:
- REST API for authentication and data fetching
- WebSocket for real-time game commands and updates

### Backend (Django)

**Purpose**: Game server and API

**Key Applications**:
- **accounts**: User authentication and registration
- **game**: Core game logic, models, commands
- **world**: World building and management
- **combat**: Combat system implementation
- **api**: REST API endpoints
- **websocket**: WebSocket consumers

**Communication**:
- ASGI for async WebSocket support
- Django ORM for database access
- Channel layers for distributed messaging

### Database (PostgreSQL)

**Purpose**: Persistent data storage

**Key Data**:
- User accounts
- Player characters
- Game world (rooms, zones)
- Items and NPCs
- Quests and progress

### Cache/Message Broker (Redis)

**Purpose**: Real-time messaging and caching

**Uses**:
- Django Channels layer backend
- Session storage
- Celery message broker
- Caching frequently accessed data

### Background Tasks (Celery)

**Purpose**: Asynchronous task processing

**Tasks**:
- Game world tick (every second)
- NPC AI updates
- World events
- Scheduled maintenance

## Data Flow

### Player Command Flow

1. Player enters command in browser
2. WebSocket sends command to GameConsumer
3. GameConsumer authenticates and validates
4. Command handler processes command
5. Game logic updates database
6. Response sent back via WebSocket
7. UI updates to show result

### Real-time Updates Flow

1. Game event occurs (e.g., player enters room)
2. Event triggers broadcast to room group
3. Channel layer distributes message to all connections
4. WebSocket consumers send updates to clients
5. Clients update UI in real-time

### Authentication Flow

1. User submits login credentials
2. API endpoint validates credentials
3. Token generated and returned
4. Token stored in browser localStorage
5. Token included in all subsequent requests
6. WebSocket connection authenticated via token

## Security Layers

1. **Transport Security**: HTTPS/WSS in production
2. **Authentication**: Token-based auth for API and WebSocket
3. **Authorization**: Permission checks on all actions
4. **Input Validation**: All user input sanitized
5. **SQL Injection Prevention**: ORM usage
6. **XSS Prevention**: Template escaping
7. **CSRF Protection**: Django middleware

## Scalability Considerations

### Horizontal Scaling

- Multiple Django/Channels instances behind load balancer
- Redis for shared state across instances
- Database connection pooling
- Static files served via CDN

### Performance Optimization

- Database query optimization (select_related, prefetch_related)
- Redis caching for frequently accessed data
- WebSocket connection pooling
- Async task processing

## Monitoring

- Application logs (game events, errors)
- Performance metrics (response times, query counts)
- WebSocket connection monitoring
- Database query analysis

## See Also

- [research/01-mud-architecture-patterns.md](../research/01-mud-architecture-patterns.md)
- [research/03-websocket-implementations.md](../research/03-websocket-implementations.md)
- [project.md](../project.md)
