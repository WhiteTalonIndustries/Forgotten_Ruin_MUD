"""
Game Commands Package

Contains all player command implementations.
"""

from .base import Command, CommandHandler
from .general import HelpCommand
from .movement import MoveCommand, LookCommand
from .inventory import TakeCommand, DropCommand, InventoryCommand
from .social import SayCommand, EmoteCommand, WhisperCommand, ShoutCommand, GlobalCommand
from .combat import AttackCommand

# Command registry
COMMAND_REGISTRY = {
    # General
    'help': HelpCommand,
    '?': HelpCommand,
    'commands': HelpCommand,

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
    "'": SayCommand,
    'emote': EmoteCommand,
    'me': EmoteCommand,
    'em': EmoteCommand,
    'whisper': WhisperCommand,
    'tell': WhisperCommand,
    'w': WhisperCommand,
    'shout': ShoutCommand,
    'yell': ShoutCommand,
    'global': GlobalCommand,
    'g': GlobalCommand,
    'chat': GlobalCommand,

    # Combat
    'attack': AttackCommand,
    'kill': AttackCommand,
}

__all__ = [
    'Command',
    'CommandHandler',
    'COMMAND_REGISTRY',
]
