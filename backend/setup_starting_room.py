#!/usr/bin/env python
"""
Quick script to create a starting room and assign it to players
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from game.models import Room, Zone, Player

# Create or get starter zone
zone, created = Zone.objects.get_or_create(
    key='starter_zone',
    defaults={
        'name': 'Starter Zone',
        'description': 'The beginning area for new adventurers.',
        'level_min': 1,
        'level_max': 10,
        'is_safe': True,
    }
)
print(f"{'Created' if created else 'Found'} zone: {zone.name}")

# Create or get starting room
room, created = Room.objects.get_or_create(
    key='start',
    defaults={
        'name': 'Town Square',
        'description': '''You stand in a bustling town square.

The cobblestone plaza is surrounded by various shops and buildings.
A large fountain stands in the center, its water sparkling in the sunlight.
Citizens hurry about their daily business, and you can hear the sounds of
commerce and conversation all around you.

To the north, you can see the entrance to the Adventurer's Guild.
To the east lies the market district.
To the west, a quiet residential area.
To the south, the main gate leads out of town.''',
        'zone': zone,
        'is_safe': True,
    }
)
print(f"{'Created' if created else 'Found'} room: {room.name}")

# Update all players without a location
players_updated = 0
for player in Player.objects.filter(location__isnull=True):
    player.location = room
    player.home = room
    player.save()
    players_updated += 1
    print(f"  Updated player: {player.character_name}")

print(f"\nTotal players updated: {players_updated}")
print(f"\nStarting room is ready at: {room.name}")
print("All players now have a starting location!")
