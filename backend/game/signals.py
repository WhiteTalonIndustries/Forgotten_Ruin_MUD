"""
Django Signals for Game Events

Handles automatic actions triggered by model events.
"""
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Player

User = get_user_model()


@receiver(post_save, sender=User)
def create_player_for_user(sender, instance, created, **kwargs):
    """
    Automatically create a Player when a new User is created
    """
    if created:
        # Only create if player doesn't exist
        if not hasattr(instance, 'player'):
            Player.objects.create(
                user=instance,
                character_name=f"{instance.username}_character"
            )


@receiver(pre_delete, sender=Player)
def cleanup_player_items(sender, instance, **kwargs):
    """
    Clean up player items when player is deleted
    """
    # Delete all items owned by player
    instance.items.all().delete()
