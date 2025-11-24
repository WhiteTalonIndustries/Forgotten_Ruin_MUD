# Forgotten Ruin MUD

A modern, web-based Multi-User Dungeon (MUD) built with Python Django and React.

## Project Overview

Forgotten Ruin is an open-source, text-based multiplayer online game that brings the classic MUD experience to the modern web. Built with security, scalability, and community contribution in mind.

### Key Features

- **Web-based Interface**: Play directly in your browser with a modern React frontend
- **Real-time Multiplayer**: WebSocket-powered real-time gameplay
- **Comprehensive Chat System**: Multiple chat channels (say, whisper, shout, global)
- **Player Characters**: Full character management with stats, inventory, and equipment
- **Rich Game World**: Explore zones, complete quests, battle NPCs
- **Character Progression**: Level up, gain experience, collect items
- **Real-time Updates**: Stats and messages update instantly via WebSockets
- **Secure**: Built with security best practices from day one
- **Open Source**: Community-driven development

## Technology Stack

### Backend
- **Framework**: Django 4.2+
- **Real-time**: Django Channels + WebSockets
- **Database**: SQLite (dev) / PostgreSQL (production)
- **Cache/Channels**: Redis
- **API**: Django REST Framework

### Frontend
- **Framework**: React 18
- **State Management**: React Hooks
- **Styling**: Custom CSS (terminal theme)
- **Communication**: Axios + WebSocket API

## Project Structure

```
Forgotten_Ruin_MUD/
├── backend/                 # Django backend
│   ├── server/             # Project configuration
│   ├── accounts/           # User authentication
│   ├── game/               # Core game logic
│   ├── world/              # World building tools
│   ├── combat/             # Combat systems
│   ├── api/                # REST API endpoints
│   └── websocket/          # WebSocket consumers
├── frontend/               # React frontend
│   ├── public/
│   └── src/
│       ├── components/     # React components
│       ├── pages/          # Page components
│       ├── services/       # API services
│       ├── hooks/          # Custom hooks
│       └── styles/         # CSS styles
├── docs/                   # Documentation
├── research/               # Research materials
└── tests/                  # Test suites
```

## Quick Start

### One-Command Startup (Recommended)

Start everything with a single command:

```bash
./start.sh
```

This will:
- ✅ Check and start Redis
- ✅ Install dependencies if needed
- ✅ Run database migrations
- ✅ Start backend (http://localhost:8000)
- ✅ Start frontend (http://localhost:3000)
- ✅ Open your browser automatically

To stop all servers:
```bash
./stop.sh
```

Or press **Ctrl+C** in the terminal where `start.sh` is running.

📖 See [STARTUP_GUIDE.md](./STARTUP_GUIDE.md) for detailed script usage.

### Prerequisites

- Python 3.9+
- Node.js 16+
- Redis 6+ (script will automatically start it)
- **SQLite** (built-in, no setup required) - Default for development
- PostgreSQL 13+ (optional, for production use)

### Manual Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/forgotten-ruin-mud.git
   cd forgotten-ruin-mud
   ```

2. **Install dependencies**
   ```bash
   # Backend
   cd backend
   pip3 install -r requirements.txt

   # Frontend
   cd ../frontend
   npm install
   ```

3. **Start services**
   ```bash
   # Use the startup script (recommended)
   ./start.sh

   # Or manually (see docs/SETUP.md)
   ```

📖 See [docs/SETUP.md](./docs/SETUP.md) for detailed manual setup instructions.

## Documentation

### Getting Started
- **[Startup Scripts Guide](./STARTUP_GUIDE.md)** - Quick one-command startup
- **[Quick Start Testing](./docs/QUICK_START_TESTING.md)** - Test all features
- **[Setup Guide](./docs/SETUP.md)** - Detailed manual setup

### Features
- **[Chat & Player Integration](./docs/CHAT_AND_PLAYER_INTEGRATION.md)** - Complete feature guide
- **[API Documentation](./docs/api/)** - REST API reference
- **[Architecture](./docs/architecture/)** - System architecture

### Development
- **[Project Documentation](./project.md)** - Project overview
- **[Research Materials](./research/README.md)** - Implementation guidelines

## Contributing

We welcome contributions! Please see the [research](./research/) directory for implementation guidelines.

## License

This project is open-source. License details to be determined.

## Recent Updates

### Version 0.2.0 (Latest)
- ✅ Complete chat system (say, whisper, emote, shout, global)
- ✅ Full player character integration
- ✅ Real-time stats updates via WebSocket
- ✅ Character sheet with inventory and quests
- ✅ One-command startup scripts
- ✅ Comprehensive documentation

### Version 0.1.0
- ✅ Login system integration
- ✅ Basic game structure
- ✅ WebSocket foundation

## Status

**Active Development** | Version 0.2.0 | Last Updated: 2025-11-24