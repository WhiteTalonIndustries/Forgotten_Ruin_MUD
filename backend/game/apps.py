"""
Game application configuration
"""
from django.apps import AppConfig


class GameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'game'
    verbose_name = 'Game Logic'

    def ready(self):
        """
        Initialize game systems when Django starts
        """
        # Import signal handlers
        import game.signals
