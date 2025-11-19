"""
Game Commands Package

Contains all player command implementations.
"""

from .base import Command, CommandHandler
from .movement import MoveCommand, LookCommand
from .inventory import TakeCommand, DropCommand, InventoryCommand
from .social import SayCommand, EmoteCommand
from .combat import AttackCommand

# Command registry
COMMAND_REGISTRY = {
    # Movement
    'move': MoveCommand,
    'look': LookCommand,
    'l': LookCommand,

    # Inventory
    'take': TakeCommand,
    'get': TakeCommand,
    'drop': DropCommand,
    'inventory': InventoryCommand,
    'inv': InventoryCommand,
    'i': InventoryCommand,

    # Social
    'say': SayCommand,
    '"': SayCommand,
    'emote': EmoteCommand,
    'me': EmoteCommand,

    # Combat
    'attack': AttackCommand,
    'kill': AttackCommand,
}

__all__ = [
    'Command',
    'CommandHandler',
    'COMMAND_REGISTRY',
]
