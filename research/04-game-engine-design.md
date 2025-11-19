# MUD Game Engine Design Patterns

## Overview
This document outlines the core design patterns and architecture for a MUD game engine, focusing on world representation, entity management, game mechanics, and extensibility.

## Core Engine Components

### 1. Entity System
The foundation of the game world where everything (players, NPCs, items, rooms) is an entity.

#### Base Entity Model
```python
# Django model example
from django.db import models

class Entity(models.Model):
    """Base class for all game objects"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    entity_type = models.CharField(max_length=50)  # player, npc, item, room
    attributes = models.JSONField(default=dict)  # Flexible attribute storage
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```

#### Location-Based Object Model
```python
class GameObject(Entity):
    """Objects that can exist in the world"""
    location = models.ForeignKey('Room', on_delete=models.SET_NULL, null=True)
    home = models.ForeignKey('Room', on_delete=models.SET_NULL, null=True)

class Room(Entity):
    """Locations in the game world"""
    @property
    def contents(self):
        return GameObject.objects.filter(location=self)

    def get_exits(self):
        return Exit.objects.filter(source=self)
```

### 2. World Representation

#### Room System
- **Rooms**: Discrete locations with descriptions
- **Exits**: Connections between rooms (north, south, east, west, up, down)
- **Zones/Areas**: Groupings of related rooms
- **Coordinates**: Optional grid system for mapping

```python
class Room(models.Model):
    key = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    zone = models.ForeignKey('Zone', on_delete=models.CASCADE)
    coordinates = models.JSONField(null=True)  # {x: 0, y: 0, z: 0}

    # Room flags
    is_dark = models.BooleanField(default=False)
    is_safe = models.BooleanField(default=False)  # No combat
    is_private = models.BooleanField(default=False)

    # Dynamic elements
    state = models.JSONField(default=dict)  # Puzzle state, conditions, etc.

class Exit(models.Model):
    source = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='exits_out')
    destination = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='exits_in')
    direction = models.CharField(max_length=20)

    # Exit properties
    is_locked = models.BooleanField(default=False)
    required_key = models.ForeignKey('Item', null=True, on_delete=models.SET_NULL)
    is_hidden = models.BooleanField(default=False)
    is_one_way = models.BooleanField(default=False)
```

### 3. Character System

#### Player Model
```python
class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    character_name = models.CharField(max_length=100, unique=True)
    location = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)

    # Core stats
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)
    health = models.IntegerField(default=100)
    max_health = models.IntegerField(default=100)
    mana = models.IntegerField(default=100)
    max_mana = models.IntegerField(default=100)

    # Attributes (could be JSONField for flexibility)
    strength = models.IntegerField(default=10)
    dexterity = models.IntegerField(default=10)
    intelligence = models.IntegerField(default=10)

    # State
    is_online = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True)
    position = models.CharField(max_length=20, default='standing')  # standing, sitting, lying

    # Inventory
    inventory_size = models.IntegerField(default=20)

    def get_inventory(self):
        return Item.objects.filter(owner=self)
```

#### NPC Model
```python
class NPC(models.Model):
    name = models.CharField(max_length=100)
    location = models.ForeignKey(Room, on_delete=models.CASCADE)

    # Behavior
    ai_type = models.CharField(max_length=50)  # passive, aggressive, merchant, quest_giver
    dialogue_tree = models.JSONField(null=True)
    patrol_route = models.JSONField(null=True)  # List of room IDs

    # Combat stats
    health = models.IntegerField(default=100)
    level = models.IntegerField(default=1)

    # Loot table
    loot_table = models.JSONField(default=list)

    # Respawn
    respawn_time = models.IntegerField(default=300)  # seconds
    is_alive = models.BooleanField(default=True)
    death_time = models.DateTimeField(null=True)
```

### 4. Item System

```python
class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    item_type = models.CharField(max_length=50)  # weapon, armor, consumable, quest, misc

    # Location (inventory or room)
    owner = models.ForeignKey(Player, null=True, on_delete=models.CASCADE)
    location = models.ForeignKey(Room, null=True, on_delete=models.CASCADE)

    # Properties
    weight = models.FloatField(default=1.0)
    value = models.IntegerField(default=0)

    # Item flags
    is_takeable = models.BooleanField(default=True)
    is_droppable = models.BooleanField(default=True)
    is_unique = models.BooleanField(default=False)
    is_quest_item = models.BooleanField(default=False)

    # Equipment
    equipment_slot = models.CharField(max_length=50, null=True)  # head, chest, weapon, etc.
    is_equipped = models.BooleanField(default=False)

    # Stats modification
    stat_modifiers = models.JSONField(default=dict)  # {strength: +5, defense: +10}

    # Consumables
    uses_remaining = models.IntegerField(null=True)
    effect = models.JSONField(null=True)  # {type: 'heal', amount: 50}
```

### 5. Command System

#### Command Handler Pattern
```python
class Command:
    """Base command class"""
    key = ""  # Command name (e.g., "look", "move", "attack")
    aliases = []  # Alternative names
    help_text = ""

    def parse(self, raw_input):
        """Parse user input into command arguments"""
        pass

    def check_permissions(self, player):
        """Check if player can execute this command"""
        return True

    def execute(self, player, **kwargs):
        """Execute the command"""
        raise NotImplementedError

class LookCommand(Command):
    key = "look"
    aliases = ["l", "examine"]
    help_text = "Look at your surroundings or an object"

    def execute(self, player, target=None):
        if target:
            # Look at specific object
            obj = find_object(target, player.location)
            return obj.description if obj else "You don't see that here."
        else:
            # Look at room
            room = player.location
            output = f"{room.name}\n{room.description}\n"

            # Show exits
            exits = room.get_exits()
            output += f"Exits: {', '.join([e.direction for e in exits])}\n"

            # Show other players
            others = Player.objects.filter(location=room, is_online=True).exclude(id=player.id)
            if others:
                output += f"Players here: {', '.join([p.character_name for p in others])}\n"

            # Show items
            items = Item.objects.filter(location=room)
            if items:
                output += f"Items: {', '.join([i.name for i in items])}"

            return output

# Command registry
COMMAND_REGISTRY = {
    'look': LookCommand,
    'move': MoveCommand,
    'take': TakeCommand,
    'drop': DropCommand,
    'inventory': InventoryCommand,
    'attack': AttackCommand,
    'say': SayCommand,
    # ... more commands
}
```

#### Command Parser
```python
def parse_command(player, raw_input):
    """Parse and execute player commands"""
    parts = raw_input.strip().split()
    if not parts:
        return "Please enter a command."

    cmd_name = parts[0].lower()
    args = parts[1:]

    # Find command in registry
    command_class = None
    for cmd_key, cmd_cls in COMMAND_REGISTRY.items():
        if cmd_name == cmd_key or cmd_name in cmd_cls.aliases:
            command_class = cmd_cls
            break

    if not command_class:
        return f"Unknown command: {cmd_name}"

    # Instantiate and execute
    command = command_class()

    if not command.check_permissions(player):
        return "You don't have permission to do that."

    try:
        result = command.execute(player, *args)
        return result
    except Exception as e:
        return f"Error executing command: {str(e)}"
```

### 6. Combat System

```python
class CombatEngine:
    """Handles combat mechanics"""

    @staticmethod
    def initiate_combat(attacker, defender):
        """Start combat between two entities"""
        combat_session = CombatSession.objects.create(
            attacker=attacker,
            defender=defender,
            status='active'
        )
        return combat_session

    @staticmethod
    def calculate_damage(attacker, defender):
        """Calculate damage based on stats and equipment"""
        base_damage = attacker.strength

        # Add weapon damage
        weapon = Item.objects.filter(owner=attacker, equipment_slot='weapon', is_equipped=True).first()
        if weapon and 'damage' in weapon.stat_modifiers:
            base_damage += weapon.stat_modifiers['damage']

        # Calculate defense
        defense = defender.dexterity
        armor = Item.objects.filter(owner=defender, is_equipped=True)
        for piece in armor:
            if 'defense' in piece.stat_modifiers:
                defense += piece.stat_modifiers['defense']

        # Final damage calculation
        damage = max(1, base_damage - (defense // 2))

        # Add randomness
        import random
        damage = random.randint(int(damage * 0.8), int(damage * 1.2))

        return damage

    @staticmethod
    def apply_damage(entity, damage):
        """Apply damage to an entity"""
        entity.health = max(0, entity.health - damage)
        entity.save()

        if entity.health == 0:
            CombatEngine.handle_death(entity)

        return entity.health

    @staticmethod
    def handle_death(entity):
        """Handle entity death"""
        if isinstance(entity, Player):
            # Player death logic
            entity.position = 'dead'
            entity.location = Room.objects.get(key='respawn_point')
            entity.health = entity.max_health
            entity.save()
        elif isinstance(entity, NPC):
            # NPC death - drop loot, schedule respawn
            entity.is_alive = False
            entity.death_time = timezone.now()
            CombatEngine.drop_loot(entity)
            entity.save()

    @staticmethod
    def drop_loot(npc):
        """Drop items from NPC loot table"""
        import random
        for loot_entry in npc.loot_table:
            if random.random() < loot_entry['chance']:
                Item.objects.create(
                    name=loot_entry['item'],
                    location=npc.location
                )

class CombatSession(models.Model):
    attacker = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='attacks')
    defender = models.ForeignKey(NPC, on_delete=models.CASCADE, related_name='defends')
    status = models.CharField(max_length=20)  # active, ended
    started_at = models.DateTimeField(auto_now_add=True)
```

### 7. Event System

```python
class Event(models.Model):
    """World events and triggers"""
    event_type = models.CharField(max_length=50)  # time_based, player_action, npc_action
    trigger_condition = models.JSONField()  # Conditions for event to fire
    action = models.JSONField()  # What happens when event fires
    is_active = models.BooleanField(default=True)
    is_repeating = models.BooleanField(default=False)

class EventHandler:
    """Process game events"""

    @staticmethod
    def trigger_event(event_type, **context):
        """Trigger events matching the type and conditions"""
        events = Event.objects.filter(event_type=event_type, is_active=True)

        for event in events:
            if EventHandler.check_condition(event.trigger_condition, context):
                EventHandler.execute_action(event.action, context)

                if not event.is_repeating:
                    event.is_active = False
                    event.save()

    @staticmethod
    def check_condition(condition, context):
        """Check if event condition is met"""
        # Example: {"type": "player_level", "operator": ">=", "value": 10}
        # Implement condition evaluation logic
        pass

    @staticmethod
    def execute_action(action, context):
        """Execute the event action"""
        # Example: {"type": "spawn_npc", "npc_id": 123, "room_id": 456}
        # Implement action execution logic
        pass
```

### 8. Scripting System

For extensibility and custom content:

```python
class Script(models.Model):
    """Player-created scripts for custom behaviors"""
    name = models.CharField(max_length=100)
    script_type = models.CharField(max_length=50)  # room_script, item_script, npc_script
    code = models.TextField()  # Python code (sandboxed execution)
    attached_to = models.ForeignKey(Entity, on_delete=models.CASCADE)

    # Safety
    is_approved = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

class ScriptEngine:
    """Safe script execution"""

    @staticmethod
    def execute_script(script, context):
        """Execute script in sandboxed environment"""
        import restrictedpython
        # Implement safe execution with restricted Python
        # Limit available functions, prevent file access, etc.
        pass
```

### 9. Time and Tick System

```python
class WorldTick:
    """Manage game world time and periodic updates"""

    @staticmethod
    def tick():
        """Execute every game tick (e.g., 1 second)"""
        # Update NPC AI
        WorldTick.update_npcs()

        # Process combat rounds
        WorldTick.process_combat()

        # Regenerate player health/mana
        WorldTick.regenerate_players()

        # Check and execute scheduled events
        WorldTick.process_events()

        # Respawn dead NPCs
        WorldTick.respawn_npcs()

    @staticmethod
    def update_npcs():
        """Update NPC behaviors"""
        for npc in NPC.objects.filter(is_alive=True):
            ai = NPCAIFactory.get_ai(npc.ai_type)
            ai.update(npc)

    # ... other tick methods

# Celery task for periodic tick
@app.task
def game_tick():
    WorldTick.tick()

# Celery beat schedule
CELERYBEAT_SCHEDULE = {
    'game-tick': {
        'task': 'game.tasks.game_tick',
        'schedule': timedelta(seconds=1),
    },
}
```

### 10. Quest System

```python
class Quest(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    quest_giver = models.ForeignKey(NPC, on_delete=models.CASCADE)

    # Requirements
    required_level = models.IntegerField(default=1)
    prerequisite_quests = models.ManyToManyField('self', blank=True)

    # Objectives
    objectives = models.JSONField()  # [{"type": "kill", "target": "goblin", "count": 10}, ...]

    # Rewards
    experience_reward = models.IntegerField(default=0)
    item_rewards = models.ManyToManyField(Item, blank=True)

class PlayerQuest(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)  # active, completed, failed
    progress = models.JSONField()  # Track objective completion
    accepted_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True)
```

## Design Principles

### 1. Data-Driven Design
- Store game content in database, not hardcoded
- Allow easy content creation and modification
- Support dynamic world changes

### 2. Modularity
- Separate concerns (combat, movement, items, etc.)
- Pluggable systems for easy extension
- Clear interfaces between components

### 3. Extensibility
- Support custom commands
- Allow scripting for advanced users
- Plugin architecture for new features

### 4. Performance
- Efficient database queries (use select_related, prefetch_related)
- Caching for frequently accessed data
- Asynchronous processing for intensive tasks

### 5. Testability
- Unit tests for game mechanics
- Integration tests for command interactions
- Automated testing for balance and bugs

## Conclusion

A robust game engine design provides the foundation for a rich, extensible MUD experience. The entity-based architecture with clear separation of concerns enables complex gameplay while maintaining code quality and performance.
