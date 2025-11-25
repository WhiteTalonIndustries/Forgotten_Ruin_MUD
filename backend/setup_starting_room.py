#!/usr/bin/env python
"""
Quick script to create a starting room and assign it to players
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from game.models import Room, Zone, Player, Exit

# Create or get starter zone
zone, created = Zone.objects.get_or_create(
    key='starter_zone',
    defaults={
        'name': 'Ranger Outpost Alpha',
        'description': 'A fortified outpost built by the stranded Rangers in the world of Ruin.',
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
        'name': 'Ranger Outpost - Command Center',
        'description': '''You stand in the fortified command center of Ranger Outpost Alpha.

The walls are reinforced with salvaged pre-Ruin materials and newly-hewn timber,
creating a blend of old-world technology and new-world necessity. Sandbags line
the windows, and weapon racks hold a mix of M4A1 carbines and scavenged melee weapons.

A tactical map of the surrounding Ruin dominates one wall, marked with hostile
positions - orc encampments, dark wizard sightings, and the distant threat of
the Lich Pharaoh's legions. The air carries the smell of gun oil, leather, and
the faint metallic tang of magic.

Rangers move with purpose between their posts, their modern fatigues worn and
patched. Some check their ammunition, others sharpen blades for close combat.
Through the windows, you can see the harsh landscape of this world 10,000 years
after civilization fell.

To the north lies the armory and equipment depot.
To the east, the training grounds where Rangers practice both marksmanship and melee.
To the west, the medical bay and barracks.
To the south, the main gate leads into the dangerous world of Ruin.''',
        'zone': zone,
        'is_safe': True,
        'is_indoors': True,
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

# Create additional rooms
armory, created = Room.objects.get_or_create(
    key='armory',
    defaults={
        'name': 'Ranger Outpost - Armory',
        'description': '''The armory is a heavily secured room lined with weapon racks and ammunition crates.

M4A1 carbines are mounted in orderly rows alongside M249 light machine guns. Grenade
launchers, fragmentation grenades, and magazines of 5.56mm ammunition fill the shelves.
But that's not all - scavenged swords, spears, and even a few enchanted weapons taken
from fallen enemies rest in specially marked sections.

A grizzled Ranger armorer stands behind a reinforced counter, maintaining the equipment.
The smell of gun oil and steel fills the air. On the wall, a hand-painted sign reads:
"Take care of your gear, and it'll take care of you. - Sergeant Major"

The exit south leads back to the command center.''',
        'zone': zone,
        'is_safe': True,
        'is_indoors': True,
    }
)
print(f"{'Created' if created else 'Found'} room: {armory.name}")

training_grounds, created = Room.objects.get_or_create(
    key='training_grounds',
    defaults={
        'name': 'Ranger Outpost - Training Grounds',
        'description': '''An open courtyard within the fortified walls serves as the training grounds.

Rangers practice both marksmanship and melee combat here. Shooting ranges with makeshift
targets stand alongside sparring circles drawn in the dirt. The crack of rifle fire
mixes with the clash of steel as Rangers drill in the hybrid combat tactics necessary
to survive in this world.

Some practice firing bursts from their M4s while others work on sword techniques taught
by locals who've adapted to this harsh reality. A few Rangers even practice dodging
and countering magical attacks, using captured spell components for training.

Drill sergeants bark orders, pushing their squads to be ready for anything the Ruin
can throw at them. Sweat, determination, and the will to survive permeate this place.

The exit west leads back to the command center.''',
        'zone': zone,
        'is_safe': True,
        'is_indoors': False,
    }
)
print(f"{'Created' if created else 'Found'} room: {training_grounds.name}")

medical_bay, created = Room.objects.get_or_create(
    key='medical_bay',
    defaults={
        'name': 'Ranger Outpost - Medical Bay and Barracks',
        'description': '''This dual-purpose area serves as both medical facility and living quarters.

On one side, medical cots are arranged with precision, stocked with both modern first-aid
supplies and mysterious healing potions acquired through trade or scavenged from the Ruin.
A Ranger medic with field surgery training tends to wounded soldiers, while also learning
the arcane properties of magical healing herbs.

On the other side, rows of bunks provide sparse but functional sleeping arrangements.
Personal gear is stowed in footlockers, each Ranger keeping their kit ready for immediate
deployment. Photos of families 10,000 years gone sit on makeshift nightstands - reminders
of what was lost and what's worth fighting for.

The air smells of antiseptic, canvas, and the faint aroma of cooking from the mess area.

The exit east leads back to the command center.''',
        'zone': zone,
        'is_safe': True,
        'is_indoors': True,
    }
)
print(f"{'Created' if created else 'Found'} room: {medical_bay.name}")

main_gate, created = Room.objects.get_or_create(
    key='main_gate',
    defaults={
        'name': 'Ranger Outpost - Main Gate',
        'description': '''You stand at the fortified main gate of Ranger Outpost Alpha.

Massive wooden beams reinforced with salvaged metal plate create a defensible choke point.
Sandbag emplacements flank the entrance, with M249 machine guns positioned to cover
the approaches. Rangers stand watch on elevated positions, scanning the horizon for
threats - orc warbands, dark riders, or worse.

Beyond the gate, the world of Ruin stretches out before you. Ancient ruins of the old
world poke through twisted forests and corrupted wastelands. In the distance, you can
see smoke rising from what might be an orc encampment. The sky has an unnatural tint,
a reminder that magic has reclaimed this world.

This is the last safe place. Beyond lies danger, death, and perhaps glory.

To the north lies the relative safety of the command center.
To the south... the Ruin awaits.''',
        'zone': zone,
        'is_safe': True,
        'is_indoors': False,
    }
)
print(f"{'Created' if created else 'Found'} room: {main_gate.name}")

# Create exits
print("\nCreating exits...")

# Command Center exits
Exit.objects.get_or_create(
    source=room,
    direction='north',
    defaults={'destination': armory, 'is_active': True}
)
Exit.objects.get_or_create(
    source=room,
    direction='east',
    defaults={'destination': training_grounds, 'is_active': True}
)
Exit.objects.get_or_create(
    source=room,
    direction='west',
    defaults={'destination': medical_bay, 'is_active': True}
)
Exit.objects.get_or_create(
    source=room,
    direction='south',
    defaults={'destination': main_gate, 'is_active': True}
)

# Return exits
Exit.objects.get_or_create(
    source=armory,
    direction='south',
    defaults={'destination': room, 'is_active': True}
)
Exit.objects.get_or_create(
    source=training_grounds,
    direction='west',
    defaults={'destination': room, 'is_active': True}
)
Exit.objects.get_or_create(
    source=medical_bay,
    direction='east',
    defaults={'destination': room, 'is_active': True}
)
Exit.objects.get_or_create(
    source=main_gate,
    direction='north',
    defaults={'destination': room, 'is_active': True}
)

print("All exits created!")

print(f"\nStarting room is ready at: {room.name}")
print("All players now have a starting location!")
print("\nRanger Outpost Alpha is operational!")
