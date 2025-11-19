"""
Inventory Commands

Commands for managing player inventory.
"""
from .base import Command


class InventoryCommand(Command):
    """View inventory"""
    key = "inventory"
    aliases = ["inv", "i"]
    help_text = "View your inventory"
    category = "Inventory"

    def execute(self, player, **kwargs):
        """Execute inventory command"""
        items = player.items.all()

        if not items:
            return "You are not carrying anything."

        output = ["Your inventory:"]
        output.append(f"Currency: {player.currency} gold")
        output.append(f"\nItems ({player.inventory_count}/{player.inventory_size}):")

        for item in items:
            equipped = " (equipped)" if item.is_equipped else ""
            output.append(f"  {item.name}{equipped}")

        return "\n".join(output)


class TakeCommand(Command):
    """Pick up an item"""
    key = "take"
    aliases = ["get", "pick up"]
    help_text = "Pick up an item from the room"
    category = "Inventory"

    def execute(self, player, **kwargs):
        """Execute take command"""
        item_name = kwargs.get('args', '').strip()

        if not item_name:
            return "Take what?"

        if not player.location:
            return "You are nowhere."

        if player.is_inventory_full:
            return "Your inventory is full."

        # Find item in room
        item = player.location.items_here.filter(name__iexact=item_name).first()

        if not item:
            return f"You don't see '{item_name}' here."

        if not item.is_takeable:
            return f"You cannot take {item.name}."

        # Transfer item to player
        item.room = None
        item.owner_player = player
        item.save()

        # Broadcast to room
        player.location.broadcast(
            f"{player.character_name} picks up {item.name}.",
            exclude=player
        )

        return f"You take {item.name}."


class DropCommand(Command):
    """Drop an item"""
    key = "drop"
    aliases = []
    help_text = "Drop an item from your inventory"
    category = "Inventory"

    def execute(self, player, **kwargs):
        """Execute drop command"""
        item_name = kwargs.get('args', '').strip()

        if not item_name:
            return "Drop what?"

        if not player.location:
            return "You are nowhere."

        # Find item in inventory
        item = player.items.filter(name__iexact=item_name).first()

        if not item:
            return f"You don't have '{item_name}'."

        if not item.is_droppable:
            return f"You cannot drop {item.name}."

        if item.is_equipped:
            return f"You must unequip {item.name} first."

        # Transfer item to room
        item.owner_player = None
        item.room = player.location
        item.save()

        # Broadcast to room
        player.location.broadcast(
            f"{player.character_name} drops {item.name}.",
            exclude=player
        )

        return f"You drop {item.name}."


class EquipCommand(Command):
    """Equip an item"""
    key = "equip"
    aliases = ["wear", "wield"]
    help_text = "Equip an item from your inventory"
    category = "Inventory"

    def execute(self, player, **kwargs):
        """Execute equip command"""
        item_name = kwargs.get('args', '').strip()

        if not item_name:
            return "Equip what?"

        # Find item in inventory
        item = player.items.filter(name__iexact=item_name).first()

        if not item:
            return f"You don't have '{item_name}'."

        success, message = item.equip(player)
        return message


class UnequipCommand(Command):
    """Unequip an item"""
    key = "unequip"
    aliases = ["remove"]
    help_text = "Unequip an equipped item"
    category = "Inventory"

    def execute(self, player, **kwargs):
        """Execute unequip command"""
        item_name = kwargs.get('args', '').strip()

        if not item_name:
            return "Unequip what?"

        # Find item in inventory
        item = player.items.filter(name__iexact=item_name).first()

        if not item:
            return f"You don't have '{item_name}'."

        success, message = item.unequip()
        return message
