# Forgotten Ruin MUD

A modern, web-based Multi-User Dungeon (MUD) built with Python Django and React.

## Project Overview

Forgotten Ruin is an open-source, text-based multiplayer online game that brings the classic MUD experience to the modern web. Built with security, scalability, and community contribution in mind.

### Key Features

- **Web-based Interface**: Play directly in your browser with a modern React frontend
- **Real-time Multiplayer**: WebSocket-powered real-time gameplay
- **Rich Game World**: Explore zones, complete quests, battle NPCs
- **Character Progression**: Level up, gain experience, collect items
- **Secure**: Built with security best practices from day one
- **Open Source**: Community-driven development

## Technology Stack

### Backend
- **Framework**: Django 4.2+
- **Real-time**: Django Channels + WebSockets
- **Database**: PostgreSQL
- **Task Queue**: Celery + Redis
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

See [docs/SETUP.md](./docs/SETUP.md) for detailed setup instructions.

### Prerequisites

- Python 3.10+
- Node.js 16+
- PostgreSQL 13+
- Redis 6+

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/forgotten-ruin-mud.git
   cd forgotten-ruin-mud
   ```

2. **Set up backend** (see [docs/SETUP.md](./docs/SETUP.md))
3. **Set up frontend** (see [docs/SETUP.md](./docs/SETUP.md))

## Documentation

- [Setup Guide](./docs/SETUP.md)
- [Project Documentation](./project.md)
- [Research Materials](./research/README.md)
- [API Documentation](./docs/api/)
- [Architecture](./docs/architecture/)

## Contributing

We welcome contributions! Please see the [research](./research/) directory for implementation guidelines.

## License

This project is open-source. License details to be determined.

## Status

**Active Development** | Version 0.1.0 | Last Updated: 2025-11-19