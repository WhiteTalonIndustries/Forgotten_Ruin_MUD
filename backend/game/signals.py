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

    Note: This signal is bypassed during user registration via the API,
    as the registration view handles player creation with custom character names.
    """
    if created:
        # Skip if this is being called from a signal (check if raw flag is set)
        # or if player creation should be handled elsewhere (like registration)
        if kwargs.get('raw', False):
            return

        # Only create if player doesn't exist
        if not hasattr(instance, 'player'):
            from .models import Room
            # Try to get starting room
            starting_room = Room.objects.filter(key='start').first()

            # This will be skipped if player is created by registration view
            try:
                Player.objects.create(
                    user=instance,
                    character_name=instance.username,
                    location=starting_room,
                    home=starting_room
                )
            except:
                # Player might have been created by another process (e.g., registration view)
                pass


@receiver(pre_delete, sender=Player)
def cleanup_player_items(sender, instance, **kwargs):
    """
    Clean up player items when player is deleted
    """
    # Delete all items owned by player
    instance.items.all().delete()
