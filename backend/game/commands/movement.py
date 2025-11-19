"""
Movement Commands

Commands for player movement and observation.
"""
from .base import Command


class LookCommand(Command):
    """Look at surroundings or specific object"""
    key = "look"
    aliases = ["l", "examine", "ex"]
    help_text = "Look at your surroundings or examine an object"
    category = "Movement"

    def execute(self, player, **kwargs):
        """Execute look command"""
        args = kwargs.get('args', '').strip()

        if not player.location:
            return "You are in the void."

        if not args:
            # Look at room
            return self.look_at_room(player)
        else:
            # Look at specific target
            return self.look_at_target(player, args)

    def look_at_room(self, player):
        """Look at current room"""
        room = player.location
        output = []

        # Room name
        output.append(f"\n{room.name}")
        output.append("-" * len(room.name))

        # Room description
        output.append(room.description)

        # Exits
        exits = room.get_exits()
        if exits:
            exit_list = [exit.display_name for exit in exits]
            output.append(f"\nExits: {', '.join(exit_list)}")
        else:
            output.append("\nNo obvious exits.")

        # Players
        other_players = room.get_players().exclude(id=player.id)
        if other_players:
            output.append("\nPlayers here:")
            for p in other_players:
                output.append(f"  {p.character_name} is {p.position} here.")

        # NPCs
        npcs = room.get_npcs()
        if npcs:
            output.append("\nYou see:")
            for npc in npcs:
                output.append(f"  {npc.name}")

        # Items
        items = room.get_contents()
        if items:
            output.append("\nItems here:")
            for item in items:
                output.append(f"  {item.name}")

        return "\n".join(output)

    def look_at_target(self, player, target_name):
        """Look at specific target"""
        room = player.location

        # Try to find player
        other_player = room.get_players().filter(
            character_name__iexact=target_name
        ).first()
        if other_player:
            return f"{other_player.character_name}\n{other_player.description}"

        # Try to find NPC
        npc = room.get_npcs().filter(name__iexact=target_name).first()
        if npc:
            return f"{npc.name}\n{npc.description}"

        # Try to find item
        item = room.get_contents().filter(name__iexact=target_name).first()
        if item:
            return f"{item.name}\n{item.description}"

        return f"You don't see '{target_name}' here."


class MoveCommand(Command):
    """Move in a direction"""
    key = "move"
    aliases = ["go", "north", "south", "east", "west", "up", "down", "n", "s", "e", "w", "u", "d"]
    help_text = "Move in a direction (north, south, east, west, up, down)"
    category = "Movement"

    # Direction mappings
    DIRECTION_MAP = {
        'n': 'north',
        's': 'south',
        'e': 'east',
        'w': 'west',
        'u': 'up',
        'd': 'down',
        'ne': 'northeast',
        'nw': 'northwest',
        'se': 'southeast',
        'sw': 'southwest',
    }

    def execute(self, player, **kwargs):
        """Execute move command"""
        args = kwargs.get('args', '').strip().lower()

        # Determine direction
        direction = self.DIRECTION_MAP.get(args, args)

        # Check if player can move
        if player.position == 'dead':
            return "You are dead and cannot move."

        if player.position != 'standing':
            return f"You must be standing to move. (You are {player.position})"

        if not player.location:
            return "You are nowhere and cannot move."

        # Find exit in that direction
        exit_obj = player.location.exits_out.filter(
            direction=direction,
            is_active=True
        ).first()

        if not exit_obj:
            return f"You cannot go {direction}."

        # Check if exit is hidden
        if exit_obj.is_hidden:
            # TODO: Check if player has discovered this exit
            return f"You cannot go {direction}."

        # Check if player can traverse
        can_traverse, message = exit_obj.can_traverse(player)
        if not can_traverse:
            return message

        # Move player
        old_room = player.location
        new_room = exit_obj.destination

        # Broadcast to old room
        old_room.broadcast(
            exit_obj.message_leave or f"{player.character_name} leaves {direction}.",
            exclude=player
        )

        # Move player
        player.move_to(new_room)

        # Broadcast to new room
        enter_direction = self.get_opposite_direction(direction)
        new_room.broadcast(
            f"{player.character_name} arrives from the {enter_direction}.",
            exclude=player
        )

        # Show new room to player
        look_cmd = LookCommand()
        return look_cmd.look_at_room(player)

    def get_opposite_direction(self, direction):
        """Get opposite direction for arrival message"""
        opposites = {
            'north': 'south',
            'south': 'north',
            'east': 'west',
            'west': 'east',
            'up': 'below',
            'down': 'above',
            'northeast': 'southwest',
            'northwest': 'southeast',
            'southeast': 'northwest',
            'southwest': 'northeast',
            'in': 'outside',
            'out': 'inside',
        }
        return opposites.get(direction, 'elsewhere')
