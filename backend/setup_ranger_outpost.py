#!/usr/bin/env python
"""
Setup Ranger Outpost Tutorial Zone

Creates a complete tutorial area themed as a ranger outpost with:
- Central town square
- Combat training grounds (safe, no XP)
- Market district (NPC vendors & player auction house)
- Medical ward (healing services)
- Schoolhouse (skill training)
- Ranger headquarters
- Residential areas
- And more!
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from game.models import Room, Zone, Exit, NPC

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

# Get or create the zone
print_section("Creating Ranger Outpost Zone")
zone, created = Zone.objects.get_or_create(
    key='starter_zone',
    defaults={
        'name': 'Whispering Pines Outpost',
        'description': '''A fortified ranger outpost on the edge of the wilderness.

This settlement serves as humanity's bulwark against the encroaching
darkness of the Forgotten Ruins. Rangers patrol the surrounding forests,
protecting the civilian population that has gathered here seeking safety.

The outpost is a hub of activity, with training grounds for new recruits,
markets for trade, and facilities to support both rangers and civilians.''',
        'level_min': 1,
        'level_max': 10,
        'is_safe': True,
        'climate': 'temperate',
    }
)
if created:
    print_success(f"Created zone: {zone.name}")
else:
    zone.name = 'Whispering Pines Outpost'
    zone.description = zone.defaults['description'] if hasattr(zone, 'defaults') else zone.description
    zone.save()
    print_info(f"Updated zone: {zone.name}")

# Room data structure
rooms_data = {
    'town_square': {
        'name': 'Town Square',
        'description': '''You stand in the heart of Whispering Pines Outpost.

The cobblestone plaza is surrounded by sturdy wooden buildings, their
walls reinforced with iron bands. A large fountain carved from granite
stands at the center, depicting a ranger with a bow drawn, forever
vigilant. The water flows clear and cool, fed by an underground spring.

Around you, citizens go about their daily business. Rangers in forest-green
cloaks mingle with merchants, craftsmen, and families who have found
refuge here. The air carries the scent of pine and woodsmoke.

The Ranger Headquarters stands prominently to the north, its banner
bearing the crossed arrows of the Order. East leads to the bustling
Market District, while west takes you to the quieter Residential Quarter.
South, you can see the Training Grounds where new recruits practice.
A medical tent with a white flag stands to the southeast.''',
        'key': 'start',
    },

    # NORTH: Ranger Headquarters & School
    'ranger_hq': {
        'name': 'Ranger Headquarters',
        'description': '''The headquarters of the Whispering Pines Rangers.

This sturdy oak building serves as the command center for ranger
operations. Maps of the surrounding wilderness cover the walls,
marked with scouting reports and danger zones. A large table
dominates the center, scattered with reports and tactical plans.

The Rangers' Banner hangs above the doorway - two crossed arrows
over a green field, symbolizing their eternal watch over these lands.
Senior rangers discuss patrol routes in hushed tones.

A hallway to the north leads to the War Room. The Quartermaster's
office is to the west, and the town square lies south.''',
        'key': 'ranger_hq',
    },

    'war_room': {
        'name': 'War Room',
        'description': '''The strategic planning center of the outpost.

This secured chamber is where the ranger captains plan their
operations against the threats from the Forgotten Ruins. A massive
map table dominates the room, showing the entire region in miniature.
Small wooden markers indicate ranger patrols, known monster lairs,
and unexplored territories.

Weapons racks line the walls, holding emergency armaments. A
window overlooks the northern wilderness, providing a clear view
of any approaching threats.

Only the headquarters lies to the south.''',
        'key': 'war_room',
    },

    'quartermaster': {
        'name': 'Quartermaster\'s Office',
        'description': '''A cramped office filled with supplies and equipment.

Shelves line every wall, stocked with ranger gear: coils of rope,
climbing spikes, waterskins, trail rations, and more. The Quartermaster
keeps meticulous inventory lists, ensuring every ranger is properly
equipped before heading into the wilderness.

A workbench in the corner holds tools for repairing gear. The smell
of leather oil and metal polish fills the air.

The headquarters lies east. A door north leads to the Schoolhouse.''',
        'key': 'quartermaster',
    },

    'schoolhouse': {
        'name': 'Schoolhouse of Skills',
        'description': '''A warm, well-lit building dedicated to learning.

This is where outpost residents - both rangers and civilians - come
to learn new skills and improve existing ones. Bookshelves line the
walls, filled with manuals on everything from wilderness survival
to advanced combat techniques.

Several training stations are set up around the room:
- A crafting bench for learning trades
- Target practice for archery
- First aid dummies for medical training
- Herbalism tables with preserved plants
- Lock picking practice kits

Instructors rotate through, offering lessons to anyone willing to learn.

The Quartermaster's office is south, and a path northeast leads to
the Herbalist's Garden.''',
        'key': 'schoolhouse',
    },

    'herbalist_garden': {
        'name': 'Herbalist\'s Garden',
        'description': '''A peaceful garden filled with medicinal plants.

Protected by a wooden fence, this garden grows the herbs and plants
used by the outpost's healers. Neatly organized beds contain
goldenseal, echinacea, comfrey, and dozens of other medicinal flora.

A small greenhouse at the back cultivates rare plants that require
special care. The head herbalist tends the garden with devoted
attention, teaching apprentices the art of identifying and
preparing healing remedies.

The schoolhouse lies southwest. A gate east leads back toward the
Medical Ward.''',
        'key': 'herbalist_garden',
    },

    # EAST: Market District
    'market_district': {
        'name': 'Market District',
        'description': '''A bustling marketplace filled with activity.

Merchants have set up stalls and shops along both sides of this
wide street. The air fills with the calls of vendors hawking their
wares, the ring of the blacksmith's hammer, and the rich aroma of
fresh bread from the bakery.

Rangers returning from patrols sell their salvage here, while
craftsmen offer their services. Civilians trade goods, creating a
vibrant economy within the safety of the outpost walls.

The Auction House stands prominently to the north, while the
General Store is south. East leads to the Blacksmith's Forge, and
west returns to the Town Square. Northeast, you can see the
Merchant's Guild Hall.''',
        'key': 'market_district',
    },

    'auction_house': {
        'name': 'Auction House',
        'description': '''A large building dedicated to player trading.

This is where adventurers come to buy and sell items with each other.
Large boards on the walls display current auctions, with items ranging
from common supplies to rare artifacts recovered from the ruins.

Secure trading booths line the sides, allowing safe exchanges. An
auctioneer stands at the front, calling out bids for featured items.
The atmosphere crackles with the energy of commerce.

A notice board lists current auctions and completed sales. Private
trading rooms are available in the back for high-value exchanges.

The market district lies south.''',
        'key': 'auction_house',
    },

    'general_store': {
        'name': 'General Store',
        'description': '''A well-stocked shop selling everyday necessities.

Shelves groan under the weight of supplies: rope, torches, waterskins,
bedrolls, rations, and basic tools. The shopkeeper, a retired ranger,
knows the value of good equipment and stocks only reliable goods.

Basic weapons and armor hang on the walls - nothing fancy, but solid
gear for those just starting out. A counter displays potions, herbs,
and other consumables.

Signs indicate fair prices for buying and selling. The market district
is north.''',
        'key': 'general_store',
    },

    'blacksmith': {
        'name': 'Blacksmith\'s Forge',
        'description': '''A sweltering workshop filled with fire and steel.

The forge roars with heat, its flames reflected off the soot-stained
walls. The blacksmith, a massive woman with arms like tree trunks,
hammers away at a glowing sword blade. Sparks fly with each strike.

Weapon racks display her work: swords, axes, spears, and daggers of
various designs. Armor pieces hang nearby - chainmail, plate, leather.
The quality is excellent; many rangers trust their lives to her craft.

A grinding wheel spins in the corner for sharpening. The smell of hot
metal and coal fills your lungs.

West returns to the market, and north leads to the Armory.''',
        'key': 'blacksmith',
    },

    'armory': {
        'name': 'Ranger Armory',
        'description': '''A secure building storing the outpost's weapons.

This reinforced structure serves as both an armory and a showcase of
ranger martial tradition. Weapons line the walls in organized racks,
each maintained in perfect condition. The collection includes bows,
crossbows, swords, spears, and various specialized ranger equipment.

A master armorer inspects and repairs equipment here. Rangers can
requisition gear for missions, while experienced adventurers can
purchase higher-quality arms.

Display cases show historical weapons used by legendary rangers of
the past. Their stories serve as inspiration.

The blacksmith's forge is south, and the Merchant's Guild lies west.''',
        'key': 'armory',
    },

    'merchant_guild': {
        'name': 'Merchant\'s Guild Hall',
        'description': '''The headquarters of the merchants' organization.

This elegant building serves as the meeting place for the merchant
guild that operates throughout the region. Plush chairs circle a
large table where merchants discuss trade routes, prices, and
economic opportunities.

The guild provides various services: currency exchange, letters of
credit, caravan scheduling, and trade agreements. A notice board
displays trade opportunities and merchant quests.

Guild members receive preferential pricing and access to exclusive
contracts. The guildmaster's office occupies the upper floor.

Southwest leads to the market, and east connects to the armory.''',
        'key': 'merchant_guild',
    },

    # SOUTH: Training Grounds
    'training_grounds': {
        'name': 'Training Grounds',
        'description': '''An open field dedicated to combat training.

This packed-earth arena is where rangers hone their skills and new
recruits learn the fundamentals of combat. Training dummies stand at
various distances, some showing the wear of countless strikes.

Multiple practice areas are set up:
- Melee combat rings with padded weapons
- Archery ranges with target butts
- Obstacle courses for agility training
- Tactical scenario areas

**SAFE ZONE**: Combat here is non-lethal. No experience is gained,
and no real damage is inflicted. This is purely for learning and
practice.

Instructors walk among the trainees, offering advice and correction.
The clash of wooden weapons and shouts of exertion fill the air.

The town square is north. A path east leads to the Dueling Grounds,
while west takes you to the Archery Range.''',
        'key': 'training_grounds',
    },

    'dueling_grounds': {
        'name': 'Dueling Grounds',
        'description': '''A formal combat arena for one-on-one matches.

This circular ring is marked by white stones, creating a clear
boundary for duels. Wooden benches surround the area, allowing
spectators to watch matches. A scoreboard tracks recent bouts.

**SAFE ZONE**: All duels here are sanctioned and non-lethal. Magical
wards prevent actual harm - when a combatant would be struck down,
they are instead teleported to the sidelines, defeated but unharmed.

This is where rangers settle disputes honorably, where students test
their progress, and where warriors prove their skill. A duel master
oversees all matches, ensuring fair play.

The training grounds lie west. South leads to the Advanced Training
Hall.''',
        'key': 'dueling_grounds',
    },

    'archery_range': {
        'name': 'Archery Range',
        'description': '''A long range dedicated to bow and crossbow training.

Targets are set up at various distances - 50, 100, and 150 yards.
Some targets are stationary, others mounted on springs to simulate
movement. A few are even enchanted to move on their own, providing
a significant challenge.

Racks of practice bows and crossbows line the equipment shed.
Barrels full of practice arrows (blunted and marked with paint)
stand ready. Range masters supervise, ensuring safety protocols
are followed.

**SAFE ZONE**: Practice weapons only. Perfect for improving aim
without wasting expensive ammunition.

The training grounds are east. A path south leads to the Tactics
Classroom.''',
        'key': 'archery_range',
    },

    'advanced_training': {
        'name': 'Advanced Training Hall',
        'description': '''An indoor facility for advanced combat techniques.

This large hall is where experienced rangers teach specialized combat
styles to those ready to advance beyond basics. The floor is padded
with thick mats. Weapons racks hold practice versions of exotic arms.

Advanced techniques taught here include:
- Dual-wielding combat
- Shield mastery
- Disarming and grappling
- Fighting multiple opponents
- Mounted combat basics
- Special weapon techniques

**SAFE ZONE**: All training is supervised and non-lethal.

Only the most dedicated students make it to this level. The
instructors are veteran rangers with decades of experience.

The dueling grounds are north. East leads to the Tactics Classroom.''',
        'key': 'advanced_training',
    },

    'tactics_classroom': {
        'name': 'Tactics Classroom',
        'description': '''A strategic planning and theory room.

While physical training is important, a ranger must also train the
mind. This classroom teaches combat tactics, wilderness survival
strategy, monster behavior patterns, and group coordination.

A large sandbox occupies the center, used to simulate battlefield
scenarios with small figurines. Students learn to plan ambushes,
coordinate with allies, exploit terrain, and adapt to unexpected
situations.

Maps of the surrounding ruins are studied in detail. Knowledge of
your enemy and your environment can mean the difference between
victory and death.

West is the archery range, and north returns to advanced training.''',
        'key': 'tactics_classroom',
    },

    # SOUTHEAST: Medical Ward
    'medical_ward': {
        'name': 'Medical Ward',
        'description': '''A clean, well-organized healing facility.

This large tent (soon to be a permanent structure) serves as the
outpost's medical center. Rows of cots line both sides, most currently
empty - a testament to the relative safety of the outpost. The air
smells of healing herbs and clean linen.

Healers in white robes move efficiently between stations. Medical
supplies are neatly organized on shelves: bandages, poultices,
healing potions, surgical tools, and various herbs.

**HEALING SERVICES AVAILABLE**:
- Minor wounds: Free for outpost residents
- Major injuries: Subsidized rates
- Poison treatment and curse removal
- Disease curing
- Resurrection services (expensive)

A shrine to the healing goddess occupies one corner, where clerics
pray for the recovery of the injured.

The town square is northwest. North leads to the Herbalist's Garden,
and east takes you to the Recovery Rooms.''',
        'key': 'medical_ward',
    },

    'recovery_rooms': {
        'name': 'Recovery Rooms',
        'description': '''Private rooms for patients requiring extended care.

These quieter chambers allow patients to rest and recover in peace.
Each room contains a comfortable bed, a chair for visitors, and a
small table. Healing runes are carved into the walls, accelerating
natural recovery.

Healers check on patients regularly, adjusting treatment as needed.
The atmosphere is calm and conducive to healing. Soft music drifts
from somewhere, a gentle melody known to soothe pain and promote rest.

Those recovering from serious injuries, curses, or diseases stay here
until fully healed.

The medical ward is west. A door south leads to the Alchemist's Lab.''',
        'key': 'recovery_rooms',
    },

    'alchemist_lab': {
        'name': 'Alchemist\'s Laboratory',
        'description': '''A workshop filled with bubbling potions and reagents.

This is where the outpost's alchemists create healing potions, antidotes,
and other useful concoctions. Glass alembics bubble over carefully
controlled flames. Shelves hold hundreds of bottles, vials, and jars
containing ingredients both mundane and exotic.

The head alchemist, a gnome with singed eyebrows and an intense focus,
works at the main bench. She occasionally mutters formulas to herself.

**SERVICES OFFERED**:
- Potion brewing (bring ingredients)
- Poison identification
- Alchemical supplies for sale
- Crafting lessons for aspiring alchemists

A faint smell of sulfur and strange herbs permeates everything.

North returns to the recovery rooms.''',
        'key': 'alchemist_lab',
    },

    # WEST: Residential Quarter
    'residential_quarter': {
        'name': 'Residential Quarter',
        'description': '''A peaceful neighborhood of homes and families.

This quieter section of the outpost is where civilians and off-duty
rangers live. Small cottages line neat streets. Children play in the
yards, their laughter a welcome sound of normalcy in these dangerous
times.

Laundry hangs on lines between buildings. Neighbors chat over fences.
Gardens grow vegetables and flowers. The atmosphere is one of
community and mutual support - everyone here knows they depend on
each other for survival.

A small park with benches provides a gathering place. The town
square lies east. North leads to the Ranger Barracks, while south
takes you to the Commons Hall.''',
        'key': 'residential_quarter',
    },

    'ranger_barracks': {
        'name': 'Ranger Barracks',
        'description': '''Living quarters for active-duty rangers.

This long, sturdy building houses rangers between missions. Rows of
bunks line the walls, each with a footlocker for personal belongings.
The space is kept clean and orderly - ranger discipline extends to
all aspects of life.

Rangers rest, maintain their equipment, or socialize quietly. A
weapons rack near the door allows quick access in case of emergency.
Maps and mission briefings are pinned to a central board.

This is not a place for civilians - only rangers and authorized
personnel are allowed.

The residential quarter is south. A door east leads back toward the
Quartermaster's office.''',
        'key': 'ranger_barracks',
    },

    'commons_hall': {
        'name': 'Commons Hall',
        'description': '''A community gathering place and tavern.

This warm, welcoming hall serves as the social heart of the
residential quarter. Long tables fill the main room, where residents
gather for meals, celebrations, and meetings. A large fireplace
crackles cheerfully.

The tavern section serves food and drink at reasonable prices. The
barkeep, a jovial dwarf, knows everyone's name and most of their
stories. This is where you come to hear the latest news, rumors of
adventure, and tales of the ruins.

A quest board hangs near the entrance, where rangers post notices
seeking assistance with various tasks. Musicians sometimes play in
the evening, and the hall rings with song.

The residential quarter lies north, and a door east leads to the
Training Grounds.''',
        'key': 'commons_hall',
    },
}

# Create all rooms
print_section("Creating Rooms")
rooms = {}
for room_key, room_data in rooms_data.items():
    room, created = Room.objects.get_or_create(
        key=room_data['key'],
        defaults={
            'name': room_data['name'],
            'description': room_data['description'],
            'zone': zone,
            'is_safe': True,
        }
    )
    if not created:
        room.name = room_data['name']
        room.description = room_data['description']
        room.zone = zone
        room.is_safe = True
        room.save()
        print_info(f"Updated: {room.name}")
    else:
        print_success(f"Created: {room.name}")
    rooms[room_key] = room

# Create exits (connections between rooms)
print_section("Creating Exits")
exits_data = [
    # Town Square connections
    ('town_square', 'ranger_hq', 'north', 'south'),
    ('town_square', 'market_district', 'east', 'west'),
    ('town_square', 'residential_quarter', 'west', 'east'),
    ('town_square', 'training_grounds', 'south', 'north'),
    ('town_square', 'medical_ward', 'southeast', 'northwest'),

    # Ranger HQ area
    ('ranger_hq', 'war_room', 'north', 'south'),
    ('ranger_hq', 'quartermaster', 'west', 'east'),
    ('quartermaster', 'schoolhouse', 'north', 'south'),
    ('quartermaster', 'ranger_barracks', 'west', 'east'),
    ('schoolhouse', 'herbalist_garden', 'northeast', 'southwest'),
    ('herbalist_garden', 'medical_ward', 'east', 'north'),

    # Market District
    ('market_district', 'auction_house', 'north', 'south'),
    ('market_district', 'general_store', 'south', 'north'),
    ('market_district', 'blacksmith', 'east', 'west'),
    ('market_district', 'merchant_guild', 'northeast', 'southwest'),
    ('blacksmith', 'armory', 'north', 'south'),
    ('armory', 'merchant_guild', 'west', 'east'),

    # Training Grounds area
    ('training_grounds', 'dueling_grounds', 'east', 'west'),
    ('training_grounds', 'archery_range', 'west', 'east'),
    ('training_grounds', 'commons_hall', 'west', 'east'),
    ('dueling_grounds', 'advanced_training', 'south', 'north'),
    ('archery_range', 'tactics_classroom', 'south', 'north'),
    ('advanced_training', 'tactics_classroom', 'east', 'west'),

    # Medical Ward area
    ('medical_ward', 'recovery_rooms', 'east', 'west'),
    ('recovery_rooms', 'alchemist_lab', 'south', 'north'),

    # Residential Quarter
    ('residential_quarter', 'ranger_barracks', 'north', 'south'),
    ('residential_quarter', 'commons_hall', 'south', 'north'),
]

exits_created = 0
for from_key, to_key, direction, reverse_dir in exits_data:
    from_room = rooms[from_key]
    to_room = rooms[to_key]

    # Create exit from -> to
    exit_obj, created = Exit.objects.get_or_create(
        source=from_room,
        direction=direction,
        defaults={'destination': to_room}
    )
    if created:
        exits_created += 1

    # Create reverse exit to -> from
    reverse_exit, created = Exit.objects.get_or_create(
        source=to_room,
        direction=reverse_dir,
        defaults={'destination': from_room}
    )
    if created:
        exits_created += 1

print_success(f"Created/verified {exits_created} exits")

# Create NPCs
print_section("Creating NPCs")
npcs_data = [
    {
        'key': 'captain_aldric',
        'name': 'Captain Aldric Thornwood',
        'description': '''A grizzled ranger captain with steel-gray hair and sharp eyes.

Captain Thornwood commands the rangers of Whispering Pines. His weathered
face bears the scars of countless battles against the creatures from the
ruins. Despite his stern demeanor, he cares deeply for both his rangers
and the civilians under his protection.''',
        'location': 'ranger_hq',
        'greeting_message': 'Welcome to Whispering Pines, recruit. We stand between civilization and the darkness.',
        'level': 20,
    },
    {
        'key': 'healer_miriam',
        'name': 'Healer Miriam Lightbringer',
        'description': '''A compassionate cleric with gentle hands and a warm smile.

Miriam leads the medical ward, using both divine magic and herbal medicine
to heal the injured. She believes all life is precious and will heal anyone
in need, regardless of their ability to pay.''',
        'location': 'medical_ward',
        'greeting_message': 'May the light bless you. Do you require healing?',
        'level': 15,
    },
    {
        'key': 'blacksmith_greta',
        'name': 'Master Smith Greta Ironheart',
        'description': '''A powerfully built woman with muscular arms and a no-nonsense attitude.

Greta is the finest blacksmith in the region. Her weapons are sought after
by rangers throughout the land. She takes pride in her craft and won't sell
inferior goods. If it bears her mark, you can trust your life to it.''',
        'location': 'blacksmith',
        'greeting_message': 'You want quality? You came to the right place. I don\'t make junk.',
        'level': 18,
    },
    {
        'key': 'merchant_tobias',
        'name': 'Merchant Tobias Goldleaf',
        'description': '''A portly merchant with a quick smile and shrewd eyes.

Tobias runs the general store and knows the value of everything. He's fair
in his dealings and maintains a well-stocked shop. He's always interested
in buying salvage from the ruins.''',
        'location': 'general_store',
        'greeting_message': 'Welcome, welcome! Looking to buy or sell? I\'ve got the best prices around!',
        'level': 10,
    },
    {
        'key': 'instructor_kael',
        'name': 'Combat Instructor Kael Swiftblade',
        'description': '''A lithe elf with lightning-fast reflexes and decades of experience.

Kael trains new rangers in combat arts. His teaching methods are demanding
but effective. Many of the outpost's finest warriors credit their skills
to his instruction.''',
        'location': 'training_grounds',
        'greeting_message': 'Ready to train? Remember: in real combat, there are no second chances.',
        'level': 25,
    },
    {
        'key': 'teacher_elara',
        'name': 'Teacher Elara Wisewood',
        'description': '''An elderly woman with kind eyes and vast knowledge.

Elara runs the schoolhouse, teaching both children and adults various skills.
Her library of manuals and textbooks is extensive, covering everything from
herbalism to advanced tactics.''',
        'location': 'schoolhouse',
        'greeting_message': 'Knowledge is a weapon sharper than any blade. What would you like to learn?',
        'level': 12,
    },
    {
        'key': 'alchemist_zixil',
        'name': 'Alchemist Zixil Sparklebrew',
        'description': '''A gnome alchemist with perpetually singed hair and enthusiastic energy.

Zixil is brilliant but occasionally chaotic in her methods. Her potions are
effective, even if the process of making them sometimes results in small
explosions. She's always seeking rare ingredients.''',
        'location': 'alchemist_lab',
        'greeting_message': 'Oh! A customer! Careful where you step - that puddle is still acidic.',
        'level': 16,
    },
    {
        'key': 'auctioneer_marcus',
        'name': 'Auctioneer Marcus Swifthand',
        'description': '''A charismatic human with a booming voice and quick wit.

Marcus runs the auction house, facilitating trades between adventurers.
His rapid-fire auctioneering style and honest dealing have made him trusted
by the community.''',
        'location': 'auction_house',
        'greeting_message': 'Step right up! Best deals in the outpost, guaranteed!',
        'level': 8,
    },
    {
        'key': 'barkeep_durin',
        'name': 'Barkeep Durin Alekeeper',
        'description': '''A jovial dwarf with a magnificent braided beard and booming laugh.

Durin runs the Commons Hall tavern. He knows everyone's stories and serves
the best ale for miles around. His establishment is the social hub of the
outpost. He's also an excellent source of rumors and quest leads.''',
        'location': 'commons_hall',
        'greeting_message': 'Aye! Welcome, friend! First drink is on the house for newcomers!',
        'level': 14,
    },
    {
        'key': 'herbalist_sylvie',
        'name': 'Herbalist Sylvie Greenleaf',
        'description': '''A half-elf with earth-stained hands and deep connection to nature.

Sylvie maintains the herbalist's garden and teaches others about medicinal
plants. She can identify any herb and knows dozens of remedies passed down
through generations of healers.''',
        'location': 'herbalist_garden',
        'greeting_message': 'The plants speak to those who listen. Would you like to learn their secrets?',
        'level': 13,
    },
]

npcs_created = 0
for npc_data in npcs_data:
    location = rooms[npc_data['location']]
    npc, created = NPC.objects.get_or_create(
        key=npc_data['key'],
        defaults={
            'name': npc_data['name'],
            'description': npc_data['description'],
            'location': location,
            'greeting_message': npc_data['greeting_message'],
            'level': npc_data['level'],
            'max_health': npc_data['level'] * 10,
            'health': npc_data['level'] * 10,
            'ai_type': 'friendly',
            'sells_items': npc_data['location'] in ['blacksmith', 'general_store', 'alchemist_lab'],
            'buys_items': npc_data['location'] in ['general_store'],
        }
    )
    if created:
        npcs_created += 1
        print_success(f"Created NPC: {npc.name}")
    else:
        print_info(f"Found NPC: {npc.name}")

# Update all existing players to start in town square
print_section("Updating Player Locations")
from game.models import Player
players_updated = 0
for player in Player.objects.all():
    if not player.location or player.location.key != 'start':
        player.location = rooms['town_square']
        player.home = rooms['town_square']
        player.save()
        players_updated += 1
        print_success(f"Updated player: {player.character_name}")

# Print summary
print_section("Setup Complete!")
print_success(f"Zone: {zone.name}")
print_success(f"Rooms created/updated: {len(rooms)}")
print_success(f"Exits created/verified: {exits_created}")
print_success(f"NPCs created: {npcs_created}")
print_success(f"Players updated: {players_updated}")

print(f"\n{Color.GREEN}The Whispering Pines Ranger Outpost is ready!{Color.END}")
print(f"{Color.BLUE}Players will start in the Town Square.{Color.END}")
print(f"{Color.YELLOW}Explore with: look, north, south, east, west, etc.{Color.END}\n")
