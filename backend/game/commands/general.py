"""
General Commands

Basic utility commands for all players.
"""
from .base import Command, CommandHandler


class HelpCommand(Command):
    """Show available commands and help text"""
    key = "help"
    aliases = ["?", "commands"]
    help_text = "Show available commands and help information"
    category = "General"

    def execute(self, player, **kwargs):
        """Execute help command"""
        from game.commands import COMMAND_REGISTRY

        args = kwargs.get('args', '').strip()

        if args:
            # Get help for specific command
            return CommandHandler.get_help(COMMAND_REGISTRY, args)
        else:
            # Show all commands
            return CommandHandler.get_help(COMMAND_REGISTRY)
