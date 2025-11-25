#!/usr/bin/env python
"""
Setup Interactive Elements for Ranger Outpost Alpha

Creates NPCs, interactive objects, and tactical elements for the Forgotten Ruin
themed military outpost.
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from game.models import Room, NPC, Item

# Color codes for output
class Color:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    END = '\033[0m'

def print_success(msg):
    print(f"{Color.GREEN}✓ {msg}{Color.END}")

def print_info(msg):
    print(f"{Color.BLUE}→ {msg}{Color.END}")

def print_section(msg):
    print(f"\n{Color.YELLOW}{'='*60}\n{msg}\n{'='*60}{Color.END}")

# Get rooms
print_section("Loading Rooms")
rooms = {}
room_keys = [
    'start',           # Command Center
    'ranger_hq',       # Tactical Operations
    'war_room',        # Strategic Planning
    'quartermaster',   # Quartermaster's Office
    'market_district', # Supply Depot
    'blacksmith',      # Armorer Station
    'training_grounds',# Combat Training
    'medical_ward',    # Medical Bay
    'armory',          # Armory
]

for key in room_keys:
    try:
        room = Room.objects.get(key=key)
        rooms[key] = room
        print_info(f"Loaded: {room.name}")
    except Room.DoesNotExist:
        print(f"⚠ Warning: Room '{key}' not found")

# Create NPCs
print_section("Creating NPCs")

npcs_data = [
    {
        'key': 'captain_reynolds',
        'name': 'Captain Marcus Reynolds',
        'description': '''A battle-hardened Ranger captain with piercing gray eyes and a tactical mind.

Captain Reynolds commands Ranger Outpost Alpha. His multicam fatigues are worn and
patched, bearing the scars of countless engagements. An M4A1 carbine is always within
reach. His left forearm bears a jagged scar - a trophy from close combat with an orc
chieftain.

He's adapted better than most to this nightmare world. Where some Rangers struggle with
the reality of magic, Reynolds treats it like any other threat to be analyzed, countered,
and defeated. He carries both magazines and a combat knife that glows faintly with
enchantment.

His command philosophy is simple: "Rangers don't quit. We adapt, we fight, and we win."''',
        'location_key': 'ranger_hq',
        'ai_type': 'quest_giver',
        'greeting_message': 'Ranger. The situation out there is FUBAR, but we hold the line. What do you need?',
        'level': 25,
        'dialogue_tree': {
            'greeting': 'Ranger. The situation out there is FUBAR, but we hold the line. What do you need?',
            'topics': {
                'situation': 'Ten thousand years after we left, and Earth is a fantasy hellscape. Orcs, magic, dragons - the works. But we\'re US Army Rangers. We don\'t surrender, we adapt.',
                'orders': 'Right now we need intel. Patrol the perimeter, engage any orc scouts, and report back. Every piece of information keeps us alive another day.',
                'enemy': 'The Dark Army is massing to the north. Orcs mostly, but we\'ve confirmed dark wizard activity and wraith rider cavalry. They want this outpost eliminated.',
                'magic': 'Yeah, magic is real. Took me a month to accept that. Now I treat it like any other weapon system. Learn it, counter it, use it if we can.'
            }
        },
        'is_attackable': False,
    },
    {
        'key': 'sergeant_kim',
        'name': 'SSG Sarah Kim',
        'description': '''The outpost's senior NCO and training instructor. Battle-tested and no-nonsense.

Staff Sergeant Kim runs the training programs with an iron fist. She was a combatives
instructor before the Rangers got stranded here, and she's adapted those skills to
include defense against creatures that shouldn't exist.

Her fatigues are immaculate despite the circumstances. An M4A1 with an M320 grenade
launcher is slung across her back. On her hip hangs a sword - an honest-to-god sword -
that she wields with disturbing proficiency.

"Rangers train to survive," she says. "In this world, that means learning to shoot orcs
at 300 meters and then being ready to gut them with a blade if they get close."''',
        'location_key': 'training_grounds',
        'ai_type': 'trainer',
        'greeting_message': 'You here to train or to waste my time? This isn\'t a game - what you learn here keeps you breathing.',
        'level': 20,
        'dialogue_tree': {
            'greeting': 'You here to train or to waste my time? This isn\'t a game - what you learn here keeps you breathing.',
            'topics': {
                'training': 'We drill modern tactics and melee combat. You need both out there. Orcs don\'t go down from one round, and they love close combat. Be ready.',
                'combat': 'Modern doctrine still applies: fire discipline, cover, maneuver. But add in defending against magical attacks and fighting with blades. It\'s brutal.',
                'survival': 'First rule: Don\'t go solo. Second rule: Conserve ammunition. Third rule: Always have a blade ready. Magic can disable your rifle, but a sword doesn\'t jam.'
            }
        },
        'is_attackable': False,
    },
    {
        'key': 'doc_martinez',
        'name': 'SFC Diego Martinez',
        'description': '''The outpost's senior medic - part combat lifesaver, part wizard.

Sergeant First Class Martinez was a Special Forces medic before the Rangers got
stranded. Now he's something more. His medical bay combines field hospital equipment
with healing potions, herbs, and actual divine magic.

He wears medic insignia on his plate carrier and carries an M4A1, but also has vials
of glowing liquid on his belt and wears an amulet that pulses with soft light. His hands
have saved more lives than his carbine has taken.

"I learned the hard way that healing magic is real," he explains. "Prayer works here.
So does medicine. I use both. Whatever keeps my Rangers alive."''',
        'location_key': 'medical_ward',
        'ai_type': 'merchant',
        'greeting_message': 'Need patching up? I can handle anything from bullet wounds to curse removal. Welcome to 21st century medicine meets fantasy.',
        'level': 18,
        'sells_items': True,
        'buys_items': False,
        'price_modifier': 0.8,  # Discounted healing for Rangers
        'dialogue_tree': {
            'greeting': 'Need patching up? I can handle anything from bullet wounds to curse removal.',
            'topics': {
                'healing': 'I can treat conventional injuries and magical ones. Healing potions work - I\'ve tested them. Divine magic is real too. I use everything I can.',
                'supplies': 'Medical supplies are limited. We scavenge what we can and trade for healing herbs. The locals brew potions that actually work.',
                'magic': 'Magic changed everything I knew about medicine. Curses are real. Poison from monster bites needs special treatment. But I adapt - that\'s what medics do.'
            }
        },
        'is_attackable': False,
    },
    {
        'key': 'specialist_jackson',
        'name': 'SPC Marcus Jackson',
        'description': '''The outpost's armorer and gunsmith, keeping the Rangers' weapons operational.

Specialist Jackson was a small arms repairer before this deployment became permanent.
Now he maintains M4A1s, M249s, and improvises repairs with whatever materials he can
scavenge from this ruined world.

His workspace is part modern armory, part medieval forge. He's learned to work metal
the old-fashioned way when replacement parts aren't available. The smell of gun oil
mixes with coal smoke from his forge.

"Keeping our weapons running is my mission," he states flatly. "When parts run out, I
forge new ones. Rangers need their rifles, and I make sure they have them."''',
        'location_key': 'blacksmith',
        'ai_type': 'merchant',
        'greeting_message': 'Need weapons maintenance? Modifications? I keep Ranger equipment combat-ready. What do you need?',
        'level': 15,
        'sells_items': True,
        'buys_items': True,
        'price_modifier': 0.9,
        'dialogue_tree': {
            'greeting': 'Need weapons maintenance? Modifications? I keep Ranger equipment combat-ready.',
            'topics': {
                'repairs': 'I can repair any weapon or armor. Modern stuff is easy if I have parts. Old-world scavenged gear I can usually figure out.',
                'modifications': 'I add bayonet lugs to carbines, reinforce armor with scavenged plates, even try to enchant equipment. Gotta use every advantage.',
                'forge': 'Yeah, I learned blacksmithing. When you can\'t order parts from supply, you make them. I forge blades too - Rangers need backup weapons.'
            }
        },
        'is_attackable': False,
    },
    {
        'key': 'sergeant_walsh',
        'name': 'SGT Michael Walsh',
        'description': '''The quartermaster, managing the outpost's precious supplies and equipment.

Sergeant Walsh runs the supply depot with meticulous attention to detail. Every round
of ammunition is counted. Every MRE is tracked. Every piece of salvaged equipment is
catalogued. In a world where resupply isn't coming, logistics is life or death.

His desk is covered in inventory sheets and requisition forms. An M4A1 leans against
the wall next to crates of ammunition and supplies. He treats supplies like gold because
out here, they are.

"Supply discipline keeps us alive," he insists. "We can't waste ammunition or equipment.
Everything gets tracked, everything gets accounted for."''',
        'location_key': 'market_district',
        'ai_type': 'merchant',
        'greeting_message': 'Quartermaster. Here for supplies? Everything is rationed and tracked. What do you need?',
        'level': 12,
        'sells_items': True,
        'buys_items': True,
        'price_modifier': 1.0,
        'dialogue_tree': {
            'greeting': 'Quartermaster. Here for supplies? Everything is rationed and tracked.',
            'topics': {
                'supplies': 'We have 5.56mm ammunition, MREs, medical supplies, and scavenged equipment. Everything is rationed - take only what you need for your mission.',
                'salvage': 'Bring me salvage from the ruins and I\'ll trade for it. Old-world tech, monster parts, anything useful. We need resources.',
                'trade': 'I buy and sell at fair rates. Rangers get first priority. Civilians can trade after Ranger needs are met.'
            }
        },
        'is_attackable': False,
    },
    {
        'key': 'corporal_chen',
        'name': 'CPL Lisa Chen',
        'description': '''An intelligence specialist analyzing enemy movements and tactical data.

Corporal Chen is the outpost's intelligence analyst. Maps, reports, and tactical data
cover her work area. She correlates patrol reports, interrogation data, and information
from local informants to build a picture of enemy capabilities.

She's younger than most Rangers here but brilliant. Her workspace has laptops running
on solar-charged batteries, paper maps marked with enemy positions, and even sketches
of magical runes she's trying to understand.

"Knowledge is our edge," she explains. "We're outnumbered and outgunned by magic. The
only way we survive is by knowing our enemy better than they know themselves."''',
        'location_key': 'war_room',
        'ai_type': 'friendly',
        'greeting_message': 'Intel shop. I track enemy movements and capabilities. What do you need to know?',
        'level': 14,
        'dialogue_tree': {
            'greeting': 'Intel shop. I track enemy movements and capabilities. What do you need to know?',
            'topics': {
                'enemy': 'Dark Army forces are massing north. We\'ve identified orc warbands, dark wizard covens, and wraith rider cavalry. They\'re organized - that makes them dangerous.',
                'intel': 'Every patrol reports back. Every encounter gets analyzed. I build the big picture from the pieces. That\'s how we stay ahead.',
                'magic': 'I study magical threats like I would any other weapon system. Document capabilities, identify counters, develop tactics. Magic isn\'t mystical - it\'s just another tool to understand.'
            }
        },
        'is_attackable': False,
    },
    {
        'key': 'pfc_rodriguez',
        'name': 'PFC Carlos Rodriguez',
        'description': '''A young Ranger standing guard, alert and ready.

Private First Class Rodriguez is one of the outpost's sentries. Young but already
experienced in ways no Ranger should have to be. He's seen orcs charge Ranger positions.
He's watched dark wizards throw lightning. He's kept fighting.

His M4A1 is held at the ready, magazines within easy reach. He scans constantly, eyes
alert for threats. On his belt next to spare magazines is a combat knife - mundane but
reliable.

"I never thought I'd be fighting orcs and wizards," he admits. "But Rangers adapt. We
fight what's in front of us, and we don't quit."''',
        'location_key': 'start',
        'ai_type': 'guard',
        'greeting_message': 'Ranger. Perimeter is quiet for now, but stay alert. Things can go sideways fast out here.',
        'level': 10,
        'dialogue_tree': {
            'greeting': 'Ranger. Perimeter is quiet for now, but stay alert.',
            'topics': {
                'guard': 'I pull watch rotation. We keep eyes on the perimeter 24/7. Orcs love night attacks, and wraith riders move fast. Can\'t let our guard down.',
                'threat': 'Biggest threat is complacency. You start thinking you\'re safe, that\'s when the orcs hit. Stay alert, stay alive.',
                'rangers': 'Rangers are the best infantry in the world. This situation is FUBAR, but we don\'t quit. We adapt and we fight.'
            }
        },
        'is_attackable': False,
    },
]

npcs_created = 0
for npc_data in npcs_data:
    location_key = npc_data.pop('location_key')
    location = rooms.get(location_key)

    if not location:
        print(f"⚠ Warning: Location '{location_key}' not found for NPC '{npc_data['key']}'")
        continue

    # Check if NPC already exists
    existing_npc = NPC.objects.filter(key=npc_data['key']).first()
    if existing_npc:
        # Update existing NPC
        for field, value in npc_data.items():
            setattr(existing_npc, field, value)
        existing_npc.location = location
        existing_npc.home_location = location
        existing_npc.max_health = npc_data['level'] * 20
        existing_npc.health = npc_data['level'] * 20
        existing_npc.save()
        print_info(f"Updated NPC: {existing_npc.name}")
    else:
        # Create new NPC
        npc = NPC.objects.create(
            location=location,
            home_location=location,
            max_health=npc_data['level'] * 20,
            health=npc_data['level'] * 20,
            **npc_data
        )
        npcs_created += 1
        print_success(f"Created NPC: {npc.name}")

# Create Interactive Objects
print_section("Creating Interactive Objects")

objects_data = [
    {
        'key': 'tactical_map',
        'name': 'Tactical Map',
        'description': '''A large tactical map covering the wall, marked with enemy positions and Ranger intelligence.

The map shows the region around Ranger Outpost Alpha in brutal detail:

RED MARKERS (Enemy Territory):
  - North: Multiple orc encampments, estimated 500+ hostiles
  - Northwest: Dark wizard activity, ritual sites identified
  - Northeast: Wraith rider cavalry sightings
  - West: Territory of the Lich Pharaoh - EXTREME DANGER
  - East: Dragon lair confirmed - AVOID

GREEN MARKERS (Friendly):
  - Center: Ranger Outpost Alpha (your location)
  - Scattered: Small civilian settlements under Ranger protection
  - Routes: Patrol paths and supply lines

YELLOW MARKERS (Unknown/Contested):
  - Various ruins from the old world
  - Areas requiring reconnaissance

The map is updated daily as patrols report back. Red markers seem to multiply faster
than green ones. The Rangers are holding a thin line against a massive threat.''',
        'location_key': 'ranger_hq',
        'item_type': 'misc',
        'is_takeable': False,
        'is_droppable': False,
        'examine_message': 'The tactical situation is grim. The Rangers are outnumbered at least 20 to 1, possibly worse. But they hold the line.',
    },
    {
        'key': 'weapons_rack',
        'name': 'Weapons Rack',
        'description': '''A military weapons rack holding the primary armament of the Rangers.

The rack is organized with military precision:

TOP RACK - M4A1 Carbines:
  - 15 rifles, cleaned and ready
  - 30-round magazines stacked nearby
  - Weapons show wear but are well-maintained

MIDDLE RACK - M4A1 with M320 Grenade Launchers:
  - 4 rifles with attached grenade launchers
  - 40mm grenades in a locked container
  - For designated grenadiers only

BOTTOM RACK - M249 Light Machine Guns:
  - 3 LMGs with bipods deployed
  - Belt-fed ammunition boxes stacked
  - Heavy firepower for suppression

SIDE RACK - Blades:
  - Combat knives, standard issue
  - Several swords - scavenged and forged
  - Backup weapons when firearms fail

The smell of gun oil and steel is strong. These weapons are the thin line between the
Rangers and the darkness outside.''',
        'location_key': 'armory',
        'item_type': 'misc',
        'is_takeable': False,
        'is_droppable': False,
        'examine_message': 'Standard Ranger armament: M4A1 carbines, M249 LMGs, and blade weapons for close combat.',
    },
    {
        'key': 'ammo_crate',
        'name': 'Ammunition Crate',
        'description': '''A military ammunition crate stenciled with "5.56mm NATO".

The crate is partially full - a concerning sight. Inside:
  - Green-tipped 5.56mm rounds in stripper clips
  - Loose rounds waiting to be loaded into magazines
  - A few belts of linked ammunition for M249s

A tally sheet on top tracks ammunition expenditure. The numbers tell a story: the Rangers
are shooting more than they're scavenging. Eventually, they'll run out.

Handwritten notes in the margins: "Conserve ammo. Controlled pairs. Make every shot count."

This is why Rangers are learning blade combat. Bullets are finite in this world.''',
        'location_key': 'market_district',
        'item_type': 'container',
        'is_takeable': False,
        'is_droppable': False,
        'examine_message': 'Ammunition supplies are limited. Every round counts.',
    },
    {
        'key': 'combat_dummy',
        'name': 'Training Dummy',
        'description': '''A training dummy that's seen extensive use.

The dummy is human-sized but modified. Someone has added:
  - Tusks and green paint (simulating orcs)
  - Height extensions (simulating trolls)
  - Dark robes (simulating dark wizards)

It's riddled with holes from live fire training and slashed from blade practice. Rangers
train against realistic representations of their enemies.

A sign reads: "KNOW YOUR ENEMY. Orcs charge aggressively. Wizards hang back and cast.
Wraiths are fast. Train for all threats."

Blood, sweat, and cordite residue mark this training equipment. Rangers learn here so
they survive out there.''',
        'location_key': 'training_grounds',
        'item_type': 'misc',
        'is_takeable': False,
        'is_droppable': False,
        'examine_message': 'Modified to simulate enemy threats: orcs, trolls, and dark wizards.',
    },
    {
        'key': 'medical_station',
        'name': 'Medical Station',
        'description': '''A field medical station combining modern medicine with magical healing.

LEFT SIDE (Modern):
  - IV bags and trauma supplies
  - Surgical instruments sterilized and ready
  - Bandages, tourniquets, hemostatic agents
  - A combat lifesaver manual, well-thumbed

RIGHT SIDE (Magical):
  - Healing potions in labeled bottles (tested and verified)
  - Herbs with genuine restorative properties
  - An amulet that glows softly (divine healing focus)
  - Antidotes for monster poison

The two worlds meet here. Modern military medicine and fantasy healing, both saving
Ranger lives. The medics use whatever works.

A note on the wall: "Prayer works here. Magic is real. Use every tool. - Doc Martinez"''',
        'location_key': 'medical_ward',
        'item_type': 'misc',
        'is_takeable': False,
        'is_droppable': False,
        'examine_message': 'Modern medicine meets magical healing. The medics use both to save lives.',
    },
    {
        'key': 'radio_equipment',
        'name': 'Radio Equipment',
        'description': '''Military radio communications equipment, solar-powered and still operational.

The radio station is the outpost's lifeline:
  - PRC-152 tactical radios for patrol communications
  - Long-range antenna for extended communications
  - Solar panels providing power
  - Encryption systems (still functional, thank god)

A patrol is checking in now:
  "Alpha-Two-Six, this is Havoc-One-Three. Grid reference 437-862. Orc patrol,
   estimated eight hostiles. We have eyes on. Request permission to engage."

Response: "Havoc-One-Three, Alpha-Two-Six. Permission granted. Controlled fire,
          conserve ammo. Break contact if they swarm. Over."

The crackle of radios is constant. Rangers reporting in, calling for support, sharing
intel. It's the sound of modern soldiers fighting a fantasy war.''',
        'location_key': 'start',
        'item_type': 'misc',
        'is_takeable': False,
        'is_droppable': False,
        'examine_message': 'Solar-powered tactical radios keep patrols connected to command.',
    },
    {
        'key': 'intel_board',
        'name': 'Intelligence Board',
        'description': '''A board covered with intelligence reports, photos, and enemy analysis.

The board is organized by threat type:

ORCS:
  - Photos (surveillance): Green-skinned, tusked, 6-7 feet tall
  - Behavior: Aggressive, prefer melee, charge under fire
  - Tactics: Swarm attacks, limited coordination
  - Counter: Controlled fire, maintain distance, target leaders

DARK WIZARDS:
  - Description: Robed figures, carry staffs
  - Abilities: Cast lightning, fire, death magic
  - Tactics: Hang back behind melee troops
  - Counter: Prioritize targets, headshots, interrupt casting

WRAITH RIDERS:
  - Identification: Ghostly cavalry, fast moving
  - Threat Level: EXTREME
  - Tactics: Fast flanking attacks, cause fear
  - Counter: Controlled fire, iron weapons, hold formation

LICH PHARAOH (Distant Threat):
  - Status: Confirmed real
  - Capabilities: Unknown, presumed EXTREME
  - Location: Western territories
  - Orders: AVOID CONTACT

Intel saves lives. Know your enemy.''',
        'location_key': 'war_room',
        'item_type': 'misc',
        'is_takeable': False,
        'is_droppable': False,
        'examine_message': 'Detailed intelligence on enemy forces: orcs, dark wizards, wraith riders, and the Lich Pharaoh.',
    },
]

objects_created = 0
for obj_data in objects_data:
    location_key = obj_data.pop('location_key')
    location = rooms.get(location_key)

    if not location:
        print(f"⚠ Warning: Location '{location_key}' not found for object '{obj_data['key']}'")
        continue

    examine_message = obj_data.pop('examine_message', '')

    # Check if object already exists
    existing_obj = Item.objects.filter(key=obj_data['key'], room=location).first()
    if existing_obj:
        # Update existing object
        for field, value in obj_data.items():
            setattr(existing_obj, field, value)
        if examine_message:
            existing_obj.effect = {'examine_message': examine_message}
        existing_obj.save()
        print_info(f"Updated object: {existing_obj.name}")
    else:
        # Create new object
        obj = Item.objects.create(
            room=location,
            effect={'examine_message': examine_message} if examine_message else None,
            weight=0,
            value=0,
            **obj_data
        )
        objects_created += 1
        print_success(f"Created object: {obj.name}")

# Print summary
print_section("Setup Complete!")
print_success(f"NPCs created/updated: {npcs_created + (len(npcs_data) - npcs_created)}")
print_success(f"Interactive objects created/updated: {objects_created + (len(objects_data) - objects_created)}")

print(f"\n{Color.GREEN}Ranger Outpost Alpha is now fully populated with NPCs and interactive elements!{Color.END}")
print(f"{Color.BLUE}Rangers can now interact with command staff, trainers, medics, and examine tactical equipment.{Color.END}")
print(f"{Color.YELLOW}Use 'talk <npc>' to speak with NPCs and 'examine <object>' to inspect items.{Color.END}\n")
