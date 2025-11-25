#!/usr/bin/env python
"""
Update the starter zone to Forgotten Ruin theme

Converts the zone from generic fantasy to military sci-fi meets fantasy theme.
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from game.models import Zone, Room

print("Updating zone to Forgotten Ruin theme...")

# Update the zone
zone = Zone.objects.get(key='starter_zone')
zone.name = 'Ranger Outpost Alpha'
zone.description = '''A fortified military outpost in the world of Ruin - 10,000 years after civilization fell.

This is where the stranded US Army Rangers have made their stand against the
darkness. The outpost is a blend of modern military technology and necessity-driven
adaptation to a world where magic has returned and mythical creatures roam.

The Rangers fight with M4A1 carbines and tactical training against orcs, trolls,
dark wizards, and worse. This outpost is humanity's last line of defense in a
world that has become a nightmare of fantasy and horror.'''
zone.save()
print(f"✓ Updated zone: {zone.name}")

# Update Town Square (start room)
room = Room.objects.get(key='start')
room.name = 'Ranger Outpost - Command Center'
room.description = '''You stand in the fortified command center of Ranger Outpost Alpha.

The walls are reinforced with salvaged pre-Ruin materials and newly-hewn timber,
creating a blend of old-world technology and new-world necessity. Sandbags line
the windows, and weapon racks hold a mix of M4A1 carbines and scavenged melee weapons.

A tactical map of the surrounding Ruin dominates one wall, marked with hostile
positions - orc encampments, dark wizard sightings, and the distant threat of
the Lich Pharaoh's legions. The air carries the smell of gun oil, leather, and
the faint metallic tang of magic.

Rangers in worn fatigues move between their posts, checking ammunition and
sharpening blades for close combat. Through the windows, you can see the harsh
landscape of this world 10,000 years after civilization fell.

This is a military operation in a fantasy nightmare. Rangers don't just carry
rifles anymore - they've learned to fight with swords and defend against magic.

To the north lies the armory and equipment depot.
To the east, the training grounds where Rangers practice both marksmanship and melee.
To the west, the medical bay and barracks.
To the south, the main gate leads into the dangerous world of Ruin.'''
room.save()
print(f"✓ Updated: {room.name}")

# Update other key rooms
rooms_to_update = {
    'ranger_hq': {
        'name': 'Ranger Outpost - Tactical Operations',
        'description': '''The tactical operations center of the outpost.

Maps cover every wall - topographical charts of the Ruin, threat assessments,
patrol routes, and intel on enemy movements. Red pins mark confirmed orc camps.
Black pins indicate dark wizard activity. Purple marks the last reported position
of a dragon.

Rangers in combat fatigues study reports and plan operations. Radio equipment
crackles with patrol check-ins. A weapons rack holds M4A1s and M249s alongside
captured orc weapons and enchanted blades.

This is where modern military doctrine meets fantasy warfare. The Rangers adapt
or they die.

The command center lies south. North leads to the armory.'''
    },
    'war_room': {
        'name': 'Ranger Outpost - Strategic Planning',
        'description': '''A secured room where senior Rangers plan long-term operations.

The large map table shows the entire region in brutal detail. Ranger outposts
are marked in green - small islands of humanity in a sea of red enemy territory.
The Lich Pharaoh's domain sprawls to the west. Orc lands stretch endlessly
north. Dragon sightings cluster in the eastern mountains.

Battle plans lie scattered: "Operation Nightfall" - a raid on an orc stronghold.
"Phantom Protocol" - infiltrating dark wizard territory. "Last Stand Contingency" -
what to do if the outpost is overrun.

Weapon racks line the walls with emergency armaments. This room represents the
harsh reality: the Rangers are outnumbered, outgunned by magic, and running
out of time.

Tactical ops lies to the south.'''
    },
    'market_district': {
        'name': 'Ranger Outpost - Supply Depot',
        'description': '''The supply and trade area of the outpost.

This is where Rangers trade salvaged equipment, scavenged tech from the old
world, and items taken from defeated enemies. Crates are stacked high: 5.56mm
ammunition, MREs, medical supplies, and mysterious artifacts pulled from ruins.

Civilian traders who've allied with the Rangers set up stalls. They offer
services: weapon repair, armor modification, intelligence on enemy movements.
Some sell strange items - healing potions that actually work, enchanted blades,
spell components.

The smell mixes: gun oil, leather, and something otherworldly. This is the
economy of survival in a world where bullets and magic coexist.

The command center lies west. East leads to the armory. South you can see
the general store and trading posts.'''
    },
    'blacksmith': {
        'name': 'Ranger Outpost - Armorer Station',
        'description': '''A workshop combining modern armoring with ancient smithing.

The armorer, a Ranger who was once a machinist, works here with both modern
tools and traditional forge equipment. She repairs plate carriers and body
armor, modifies weapons to accept bayonets for the inevitable close combat,
and even attempts to enchant equipment using techniques learned from locals.

Weapon racks display the hybrid arsenal: M4A1 carbines with attached combat
knives, modified M249s with reinforced barrels, plate armor with ballistic
inserts, and swords forged from salvaged steel.

The workbench holds both gunsmithing tools and blacksmithing hammers. This is
where American military technology adapts to a fantasy world's demands.

The supply depot lies west.'''
    },
    'training_grounds': {
        'name': 'Ranger Outpost - Combat Training Area',
        'description': '''An open training area where Rangers drill for hybrid warfare.

One section has firing ranges where Rangers practice marksmanship with their
M4A1s and M249s. Targets are painted to look like orcs and trolls. A
qualification board tracks scores.

Another area has melee combat circles where Rangers spar with blades and
practice hand-to-hand combat. Modern combatives mixed with sword techniques.

A third section features tactical scenarios: "What to do when a dark wizard
casts at your position." "Counter-ambush against wraith riders." "Room clearing
when the enemy uses magic."

**SAFE ZONE**: All training is non-lethal. Weapons are set to practice mode.

This is where Rangers learn to survive in a world where their military training
must combine with fantasy combat skills. Adapt or die.

The command center lies north. Additional training facilities extend east and west.'''
    },
    'medical_ward': {
        'name': 'Ranger Outpost - Medical Bay',
        'description': '''The medical facility - a blend of field hospital and magical healing ward.

One side looks like a standard military medical bay: cots with wounded Rangers,
IVs, surgical equipment, trauma supplies. Medics with combat lifesaver training
work efficiently.

The other side is stranger: healing potions in labeled bottles, herbs with
genuine restorative properties, a civilian healer who channels actual divine
magic to close wounds. The Rangers have learned that in this world, prayer
sometimes works better than surgery.

The air smells of antiseptic and incense. Modern medicine meets magical healing.
Both save lives.

**HEALING SERVICES AVAILABLE**: Minor injuries treated free. Major trauma requires
resources. Curse removal and poison treatment available.

The command center lies northwest.'''
    },
}

for room_key, room_data in rooms_to_update.items():
    try:
        room = Room.objects.get(key=room_key)
        room.name = room_data['name']
        room.description = room_data['description']
        room.save()
        print(f"✓ Updated: {room.name}")
    except Room.DoesNotExist:
        print(f"⚠ Room not found: {room_key}")

print("\n✓ Zone successfully updated to Forgotten Ruin theme!")
print("The outpost now reflects the military sci-fi meets fantasy setting.")
