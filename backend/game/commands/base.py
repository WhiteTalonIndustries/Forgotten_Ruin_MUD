"""
Base Command System

Provides the foundation for all player commands.
"""
from typing import Tuple, Optional


class Command:
    """
    Base class for all commands

    Subclasses should override execute() to implement command logic.
    """
    key = ""  # Command name
    aliases = []  # Alternative command names
    help_text = ""  # Help documentation
    category = "General"  # Command category

    def __init__(self):
        """Initialize command"""
        pass

    def parse(self, raw_input: str) -> dict:
        """
        Parse command arguments from raw input

        Args:
            raw_input: Raw command string from player

        Returns:
            dict: Parsed arguments
        """
        parts = raw_input.strip().split(maxsplit=1)
        return {
            'command': parts[0] if parts else '',
            'args': parts[1] if len(parts) > 1 else '',
        }

    def check_permissions(self, player) -> Tuple[bool, str]:
        """
        Check if player has permission to execute command

        Args:
            player: Player attempting to execute command

        Returns:
            tuple: (has_permission, error_message)
        """
        return True, ""

    def execute(self, player, **kwargs) -> str:
        """
        Execute the command

        Args:
            player: Player executing command
            **kwargs: Command arguments

        Returns:
            str: Result message to send to player
        """
        raise NotImplementedError("Command must implement execute()")


class CommandHandler:
    """
    Handles parsing and executing player commands
    """

    @staticmethod
    def handle_command(player, raw_input: str, command_registry: dict) -> str:
        """
        Parse and execute a player command

        Args:
            player: Player executing command
            raw_input: Raw command string
            command_registry: Dictionary of available commands

        Returns:
            str: Result message
        """
        if not raw_input or not raw_input.strip():
            return ""

        # Parse command name and arguments
        parts = raw_input.strip().split(maxsplit=1)
        cmd_name = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ''

        # Find command in registry
        command_class = None
        for key, cmd_cls in command_registry.items():
            if cmd_name == key or cmd_name in getattr(cmd_cls, 'aliases', []):
                command_class = cmd_cls
                break

        if not command_class:
            return f"Unknown command: {cmd_name}. Type 'help' for available commands."

        # Instantiate command
        try:
            command = command_class()

            # Check permissions
            has_permission, error_msg = command.check_permissions(player)
            if not has_permission:
                return error_msg

            # Execute command
            result = command.execute(player, args=args)
            return result

        except Exception as e:
            # Log error
            import logging
            logging.error(f"Error executing command '{cmd_name}': {e}", exc_info=True)
            return "An error occurred while executing that command."

    @staticmethod
    def get_help(command_registry: dict, command_name: Optional[str] = None) -> str:
        """
        Get help text for commands

        Args:
            command_registry: Dictionary of available commands
            command_name: Specific command to get help for (optional)

        Returns:
            str: Help text
        """
        if command_name:
            # Get help for specific command
            command_class = command_registry.get(command_name.lower())
            if not command_class:
                return f"No help available for '{command_name}'."

            return f"{command_class.key}: {command_class.help_text}"
        else:
            # List all commands by category
            categories = {}
            for cmd_cls in set(command_registry.values()):
                category = getattr(cmd_cls, 'category', 'General')
                if category not in categories:
                    categories[category] = []
                categories[category].append(cmd_cls)

            help_text = "Available Commands:\n\n"
            for category, commands in sorted(categories.items()):
                help_text += f"{category}:\n"
                for cmd_cls in sorted(commands, key=lambda c: c.key):
                    aliases = f" ({', '.join(cmd_cls.aliases)})" if cmd_cls.aliases else ""
                    help_text += f"  {cmd_cls.key}{aliases}: {cmd_cls.help_text}\n"
                help_text += "\n"

            return help_text
