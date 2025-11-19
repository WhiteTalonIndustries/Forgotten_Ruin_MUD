# Reference Implementations: Open-Source MUD Codebases

## Overview
This document analyzes notable open-source MUD implementations to learn from their architecture, design decisions, and best practices.

## Primary Reference: Evennia

### Project Information
- **Website**: https://www.evennia.com/
- **Repository**: https://github.com/evennia/evennia
- **License**: BSD 3-Clause
- **Language**: Python 3.10+
- **First Release**: 2010
- **Status**: Actively maintained

### What is Evennia?

Evennia is a modern Python library and MUD server used to create online multiplayer text games (MUD, MUX, MUSH, MUCK, MOO, etc.). It's not a game itself but a framework for building games.

### Key Features

#### 1. Modern Python Architecture
- Built on Django 4.1+ and Twisted
- Asynchronous, event-driven architecture
- No race conditions through careful design
- Full object-oriented approach
- Type hints and modern Python practices

#### 2. Web Integration
- HTML5 webclient included
- WebSocket support (with ajax/comet fallback)
- RESTful API for external integrations
- Admin web interface via Django
- Integrated website/forum capabilities

#### 3. Flexible Game System
- No imposed game mechanics or setting
- Build any type of text game
- Not forked from existing game (no legacy cruft)
- Highly customizable through Python code

#### 4. Developer Experience
- Use proper IDE with code completion
- Git version control integration
- Extensive documentation
- Active community support
- Tutorial system for learning

### Architecture Deep Dive

#### Core Components

```
Evennia Architecture:

┌─────────────────────────────────────────────────┐
│                   Players                       │
│  (Telnet, SSH, Web browser, External clients)   │
└────────────┬────────────────────┬────────────────┘
             │                    │
             v                    v
    ┌────────────────┐   ┌────────────────┐
    │  Telnet/SSH    │   │   Webclient    │
    │    Portal      │   │ (WebSocket/HTTP)│
    └────────┬───────┘   └────────┬───────┘
             │                    │
             v                    v
    ┌─────────────────────────────────────┐
    │         Portal (Twisted)            │
    │  - Connection management            │
    │  - Protocol handling                │
    │  - Session management               │
    └────────────────┬────────────────────┘
                     │
                     v (AMP protocol)
    ┌─────────────────────────────────────┐
    │         Server (Django)             │
    │  - Game logic                       │
    │  - Database (PostgreSQL/SQLite)     │
    │  - Commands                         │
    │  - Scripts/AI                       │
    │  - Typeclasses                      │
    └─────────────────────────────────────┘
```

#### Portal-Server Split
- **Portal**: Handles all network connections (persistent)
- **Server**: Handles game logic (can reload without disconnecting players)
- Communication via AMP (Asynchronous Messaging Protocol)
- Allows code updates without kicking players

#### Typeclass System
Evennia's unique inheritance system:

```python
# Base Evennia class
from evennia import DefaultObject

# Your custom object
class Sword(DefaultObject):
    """
    A weapon that can be wielded
    """
    def at_object_creation(self):
        """Called when object is first created"""
        self.db.damage = 10
        self.db.weapon_type = "sword"

    def at_wield(self, wielder):
        """Called when someone wields this weapon"""
        wielder.msg(f"You wield {self.key}.")
        self.location = None
        wielder.db.wielded_weapon = self

# Create in game
sword = create_object(Sword, key="Excalibur")
```

**Key Concepts:**
- Every game entity inherits from a base typeclass
- Override methods to customize behavior
- Database attributes stored in `.db` namespace
- No database schema changes needed for new attributes

#### Command System

```python
from evennia import Command

class CmdAttack(Command):
    """
    Attack a target

    Usage:
      attack <target>

    This will initiate combat with the target.
    """
    key = "attack"
    aliases = ["att", "fight"]
    locks = "cmd:all()"
    help_category = "Combat"

    def func(self):
        """Execute the command"""
        if not self.args:
            self.caller.msg("Attack whom?")
            return

        target = self.caller.search(self.args.strip())
        if not target:
            return

        # Initiate combat
        self.caller.msg(f"You attack {target.key}!")
        target.msg(f"{self.caller.key} attacks you!")

        # Call combat system
        self.caller.db.combat_handler.add_combatant(self.caller, target)

# Add to character's command set
from evennia import CmdSet

class CharacterCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdAttack())
```

#### Script System (AI/Timers)

```python
from evennia import DefaultScript

class HeartbeatScript(DefaultScript):
    """
    Updates NPCs and game world
    """
    def at_script_creation(self):
        self.key = "heartbeat"
        self.desc = "Updates game world"
        self.interval = 60  # Every 60 seconds
        self.persistent = True  # Survives reload
        self.start_delay = True

    def at_repeat(self):
        """Called every interval"""
        # Update NPCs
        for npc in self.obj.location.contents:
            if npc.is_typeclass("evennia.objects.objects.DefaultCharacter"):
                npc.ai_tick()

# Global scripts run without being attached to an object
from evennia import create_script
create_script(HeartbeatScript)
```

### Database Design

#### Object Database Model
```python
# Simplified version of Evennia's object model
class ObjectDB(models.Model):
    """Core object model"""
    db_key = models.CharField(max_length=255)  # Object name
    db_typeclass_path = models.CharField(max_length=255)  # Python class
    db_location = models.ForeignKey('self', null=True)
    db_home = models.ForeignKey('self', null=True, related_name='homes_set')
    db_destination = models.ForeignKey('self', null=True, related_name='destinations_set')

    # Attributes stored separately for flexibility
    # attributes = Attribute.objects.filter(objectdb=self)

class Attribute(models.Model):
    """Flexible attribute storage"""
    db_obj = models.ForeignKey(ObjectDB, on_delete=models.CASCADE)
    db_key = models.CharField(max_length=255)
    db_value = models.TextField()  # Pickled Python object
    db_category = models.CharField(max_length=255, null=True)
```

**Benefits:**
- Single table for all game objects
- Attributes stored separately (no schema changes)
- Type information in typeclass_path
- Efficient querying through Django ORM

### Lessons from Evennia

#### What to Adopt
1. **Portal-Server split** - Allows code reload without disconnecting players
2. **Typeclass pattern** - Flexible object system without schema migrations
3. **Command system** - Clean, extensible command handling
4. **Script system** - Persistent background tasks and AI
5. **Web integration** - Built-in admin interface and webclient
6. **Documentation** - Comprehensive docs and tutorials

#### What to Adapt
1. **Simplify if needed** - Evennia is very feature-rich; start smaller
2. **Modern async** - Consider full async/await instead of Twisted
3. **API-first** - Stronger focus on RESTful API for external clients
4. **Microservices option** - Consider splitting services for scalability

## Other Notable Implementations

### 2. TaleFramework (Python)

- **Repository**: https://pypi.org/project/tale/
- **Focus**: Interactive fiction and MUDs
- **Language**: Python

**Key Features:**
- Lightweight compared to Evennia
- Good for smaller projects
- Story/narrative focused

### 3. Ranvier (Node.js)

- **Repository**: https://ranviermud.com/
- **Language**: JavaScript (Node.js)
- **License**: MIT

**Key Features:**
- Modern JavaScript/Node.js
- Bundle-based plugin architecture
- Event-driven design
- Good documentation
- Active community

**Architecture:**
```javascript
// Ranvier bundle structure
bundles/
  my-bundle/
    areas/
    behaviors/
    commands/
    effects/
    input-events/
    quests/
    skills/
```

**Lessons:**
- Plugin architecture for extensibility
- Clear separation of content and code
- Good for JavaScript developers

### 4. MuOxi (Rust)

- **Repository**: https://github.com/duysqubix/MuOxi
- **Language**: Rust
- **Status**: Experimental

**Key Features:**
- Modern systems language (Rust)
- Performance-focused
- Memory safety guarantees
- Built with Tokio (async runtime)

**Lessons:**
- Performance benefits of Rust
- Strong type safety
- Concurrent programming safety

### 5. MUD-Pi (Python)

- **Repository**: https://github.com/Frimkron/mud-pi
- **Language**: Python
- **Focus**: Educational

**Key Features:**
- Simple implementation
- Good for learning
- Raspberry Pi compatible
- Minimal dependencies

**Lessons:**
- Start simple, add complexity as needed
- Clear, readable code over cleverness
- Good for understanding fundamentals

## Comparative Analysis

| Feature | Evennia | Ranvier | MuOxi | MUD-Pi |
|---------|---------|---------|-------|---------|
| Language | Python | JavaScript | Rust | Python |
| Complexity | High | Medium | Medium | Low |
| Scalability | Excellent | Good | Excellent | Limited |
| Documentation | Excellent | Good | Limited | Good |
| Community | Large | Medium | Small | Small |
| Learning Curve | Steep | Moderate | Steep | Gentle |
| Production Ready | Yes | Yes | No | No |
| Best For | Large games | Modern JS devs | Performance | Learning |

## Recommendations for Forgotten Ruin

### Primary Reference: Evennia
Use Evennia as the primary reference because:
1. Same language (Python)
2. Proven architecture
3. Production-ready
4. Active community
5. Extensive documentation
6. Similar technology stack (Django)

### Architecture to Adopt

```
Recommended Architecture (inspired by Evennia):

┌──────────────────────────────────────┐
│          Web Clients                 │
│    (Browser with React/Vue/etc)      │
└─────────────┬────────────────────────┘
              │
              v
┌──────────────────────────────────────┐
│      WebSocket/HTTP Gateway          │
│     (Django Channels + Redis)        │
└─────────────┬────────────────────────┘
              │
              v
┌──────────────────────────────────────┐
│       Game Server (Django)           │
│  - Game Logic                        │
│  - Command Processing                │
│  - World Management                  │
│  - Combat System                     │
└─────────────┬────────────────────────┘
              │
              v
┌──────────────────────────────────────┐
│      Database (PostgreSQL)           │
│  - Players, Rooms, Items, NPCs       │
│  - Game State                        │
└──────────────────────────────────────┘
```

### Simplifications from Evennia

1. **No Portal-Server split initially** - Add later if needed
2. **Django Channels instead of Twisted** - More modern async approach
3. **Focus on web client** - Skip telnet/SSH support initially
4. **RESTful API priority** - Better for modern clients
5. **Simpler typeclass system** - Use Django model inheritance directly

### Code Organization (Evennia-inspired)

```
forgotten_ruin/
├── game/
│   ├── models/           # Database models (Player, Room, Item, NPC)
│   ├── commands/         # Command classes
│   ├── typeclasses/      # Base classes for game objects
│   ├── scripts/          # Background tasks, AI
│   ├── world/            # World data, room builder
│   ├── combat/           # Combat system
│   └── api/              # REST API endpoints
├── web/
│   ├── static/           # Frontend assets
│   ├── templates/        # Django templates
│   └── webclient/        # React/Vue client
├── server/
│   ├── settings.py
│   ├── urls.py
│   ├── routing.py        # WebSocket routing
│   └── asgi.py
└── manage.py
```

## Learning Resources

### Evennia Documentation
- Official docs: https://www.evennia.com/docs/latest/
- Tutorial: https://github.com/evennia/evennia/wiki/Tutorial-World-Introduction
- Video tutorials available

### Code Reading Strategy
1. Start with Evennia's tutorial world
2. Examine command implementations
3. Study typeclass inheritance
4. Review combat systems (if available)
5. Understand object relationships

### Community Resources
- Evennia Discord: Active community for questions
- GitHub Discussions: Architecture discussions
- Code examples in contrib folder

## Conclusion

While building from scratch offers learning opportunities and customization, studying Evennia provides:
- Proven patterns and best practices
- Solutions to common MUD problems
- Architecture that scales
- Active community for questions

Use Evennia as a reference, adopt its successful patterns, but simplify where appropriate for your specific needs. Don't reinvent solved problems, but do customize for your game's unique requirements.

### Next Steps

1. **Install Evennia** - Run it locally to understand the player experience
2. **Read the code** - Study their implementations of systems you need
3. **Adapt patterns** - Don't copy directly, understand and adapt
4. **Start simple** - Begin with core features, add complexity gradually
5. **Contribute back** - Open source community benefits from shared knowledge
