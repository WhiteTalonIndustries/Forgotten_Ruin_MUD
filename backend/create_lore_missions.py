#!/usr/bin/env python
"""
Create Lore-Based Missions

Creates three compelling public missions based on Forgotten Ruin lore
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from game.models import Mission, MissionEvent, NPC, Room

# Color codes
class Color:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    END = '\033[0m'

def print_success(msg):
    print(f"{Color.GREEN}✓ {msg}{Color.END}")

def print_section(msg):
    print(f"\n{Color.YELLOW}{'='*70}\n{msg}\n{'='*70}{Color.END}")

# Get NPCs
try:
    captain_reynolds = NPC.objects.get(key='captain_reynolds')
    corporal_chen = NPC.objects.get(key='corporal_chen')
    doc_martinez = NPC.objects.get(key='doc_martinez')
except NPC.DoesNotExist:
    print("Error: Required NPCs not found. Run setup_outpost_interactive.py first.")
    exit(1)

print_section("Creating Lore-Based Missions for Forgotten Ruin")

# ============================================================================
# Mission 1: Wraith Rider Ambush (High-Stakes Combat)
# ============================================================================
print_section("Mission 1: Wraith Rider Ambush")

wraith_mission, created = Mission.objects.update_or_create(
    key='mission_wraith_riders',
    defaults={
        'name': 'Wraith Rider Ambush',
        'mission_type': 'defense',
        'is_public': True,
        'given_by_npc': corporal_chen,
        'difficulty': 'very_hard',
        'required_level': 5,
        'required_squad_size': 4,

        # Hook
        'hook_title': 'Ghostly Cavalry',
        'hook_description': '''Corporal Chen intercepts you with urgent intelligence.

"We've got a problem," she says, spreading tactical photos across her workspace. The images
show ghostly riders on spectral mounts - wraith riders, one of the Dark Army's most
dangerous units.

"Intel says a wraith rider patrol is moving through sector seven," Chen explains, marking
the map. "Eight to ten riders. Fast, deadly, and they cause fear in anyone who sees them."

She looks up at you seriously. "They're heading toward a civilian settlement under our
protection. Thirty families, mostly refugees. If those wraiths reach them, it's a
massacre."

The tactical situation is clear but grim: wraith riders are extremely dangerous. They
phase through obstacles, move at incredible speed, and their very presence causes panic.
Standard tactics barely work against them.

"I know this is asking a lot," Chen says. "Wraith riders have killed Rangers before. But
those civilians need us. Can your squad intercept and stop them?"

The Dark Army's elite cavalry versus Rangers. This is the kind of fight that defines who
you are. Rangers don't leave civilians to die.

Time to move out.''',

        # Act 1: Interception
        'act1_title': 'Act 1: Setting the Ambush',
        'act1_description': '''Your squad moves fast to the interception point.

The terrain is in your favor: a narrow valley that the wraith riders must pass through
to reach the settlement. Steep sides, limited maneuver space, good fields of fire.

You have maybe thirty minutes before the wraiths arrive. Time to prepare.

SSG Kim's training kicks in: establish overlapping fields of fire, prepare fallback
positions, load magazines with iron rounds (they work better against undead), check your
blades.

"Remember," one of your team leaders says, "wraiths cause fear. When you see them, your
instincts will scream at you to run. Don't. Hold your position. Rangers don't break."

The valley grows quiet. Then you hear it: the sound of ethereal hoofbeats, growing closer.

Time's up. They're here.''',

        'act1_objectives': [
            {
                'key': 'reach_valley',
                'description': 'Reach the valley interception point',
                'required': True
            },
            {
                'key': 'establish_ambush',
                'description': 'Set up ambush positions with overlapping fire',
                'required': True
            },
            {
                'key': 'load_iron_rounds',
                'description': 'Load iron ammunition (effective against undead)',
                'required': True
            },
            {
                'key': 'prepare_fallback',
                'description': 'Establish fallback positions in case of breakthrough',
                'required': True
            }
        ],

        # Act 2: The Battle
        'act2_title': 'Act 2: Clash with the Dead',
        'act2_description': '''They come like a nightmare made manifest.

Eight wraith riders emerge from the tree line: ghostly figures on spectral mounts, moving
impossibly fast. The air grows cold. Your breath fogs. Every instinct screams danger.

The fear effect hits your squad. It's real, tangible, overwhelming. You see your squad
members fighting the urge to flee. But Rangers don't break. You hold.

"CONTACT!" someone yells. "OPEN FIRE!"

Your squad unleashes controlled fire. Iron rounds punch through ghostly flesh. The wraiths
scream - an inhuman sound that chills your blood. But they don't stop. They charge.

The wraiths phase through your barricades like they're not there. Close combat becomes
inevitable. Blades out. This is what SSG Kim trained you for.

One wraith reaches your position. Your rifle levels. Controlled pair - center mass. The
wraith staggers. Your blade comes up. Iron bites ghostly flesh.

The wraith dissipates with a shriek.

Seven left. The battle is chaos. Gunfire. Blade work. Rangers fighting the dead. This is
impossible. But you're doing it anyway.

Four wraiths down. But they're adapting, trying to flank, using their speed and phase
ability. Your squad needs to adapt faster or this goes bad quickly.''',

        'act2_objectives': [
            {
                'key': 'resist_fear',
                'description': 'Resist the wraith riders\' fear effect and hold position',
                'required': True
            },
            {
                'key': 'first_contact',
                'description': 'Engage wraith riders with ranged fire',
                'required': True
            },
            {
                'key': 'melee_combat',
                'description': 'Engage in close combat with iron blades',
                'required': True
            },
            {
                'key': 'eliminate_four_wraiths',
                'description': 'Eliminate at least four wraith riders',
                'required': True
            },
            {
                'key': 'prevent_flanking',
                'description': 'Prevent wraiths from flanking your position',
                'required': True
            }
        ],

        # Act 3: Final Stand
        'act3_title': 'Act 3: The Last Riders',
        'act3_description': '''Four wraiths remain. They're wounded, desperate, and more dangerous than ever.

Your squad has taken casualties. Not killed, but wounded. Someone took a wraith blade to
the shoulder - necrotic damage, Doc Martinez will need to treat that. Another Ranger has
a broken arm from close combat.

But you're still in the fight. Still holding the line.

The wraiths regroup for a final charge. You can see their strategy: they'll focus on a
single point, try to breakthrough, reach the settlement behind you.

Can't let that happen.

"RELOAD!" you order. "PREPARE FOR FINAL ASSAULT!"

Your squad reloads with practiced efficiency. Iron rounds chambered. Blades ready. Wounded
Rangers providing supporting fire. Everyone fights.

The wraiths charge. A final, desperate attack. Everything happens at once:

Controlled fire - two wraiths drop. Close combat - blade against spectral sword. One
wraith breaks through - but your fallback position catches it. Crossfire eliminates it.

One wraith left. The leader, larger than the others. It sees the battle is lost. It could
flee. But wraith riders don't flee.

It charges directly at you. Personal duel. Wraith leader versus Ranger.

Your M4A1 levels. Controlled pairs. Iron rounds punch through ghostly armor. The wraith
staggers but keeps coming. Twenty meters. Ten meters.

Your blade comes up. The wraith swings its spectral sword. You parry - iron against
ethereal. The impact jars your arm but the blade holds.

Counter-strike. Your iron blade finds the wraith's core. The creature screams and
dissipates into mist.

Silence falls over the valley.

Eight wraith riders came. None leave. The civilian settlement is safe.

Rangers hold the line.''',

        'act3_objectives': [
            {
                'key': 'treat_wounded',
                'description': 'Provide combat first aid to wounded Rangers',
                'required': True
            },
            {
                'key': 'final_defense',
                'description': 'Repel the wraith riders\' final assault',
                'required': True
            },
            {
                'key': 'defeat_wraith_leader',
                'description': 'Defeat the wraith rider leader in combat',
                'required': True
            },
            {
                'key': 'protect_settlement',
                'description': 'Ensure no wraiths reach the civilian settlement',
                'required': True
            },
            {
                'key': 'after_action',
                'description': 'Conduct after-action report with CPL Chen',
                'required': True
            }
        ],

        # Conclusions
        'conclusion_success': '''Mission accomplished. Wraith riders eliminated.

Your squad returns to Ranger Outpost Alpha, battered but victorious. The wounded are
immediately taken to Doc Martinez. Necrotic damage from wraith blades is serious, but
he can treat it.

Captain Reynolds meets you in tactical operations. "I heard the report from Chen. Eight
wraith riders. Some of the Dark Army's best. And you stopped them cold."

He updates the tactical map. "The civilian settlement is safe. Thirty families that would
have been slaughtered are alive because Rangers stood between them and the Dark Army."

Corporal Chen is already analyzing the battle. "Wraith rider tactics, counters that
work, lessons learned. This intel is invaluable. Every Ranger will learn from your fight."

You're exhausted. Combat against wraith riders takes everything you have - physically,
mentally, emotionally. But you won.

"Outstanding work, Ranger," Reynolds says. "Wraith riders kill experienced soldiers. You
not only survived, you defeated them and protected civilians. That's the Ranger standard."

The Dark Army will hear about this. Rangers killed eight wraith riders in a single
engagement. That sends a message: Rangers don't break. Rangers hold the line.

No matter what the Dark Army throws at you, you'll be ready.''',

        'conclusion_failure': '''Mission failed. The settlement was lost.

The wraith riders broke through your positions and reached the civilian settlement. By the
time reinforcements arrived, it was too late. Thirty families dead. The settlement burned.

Your squad made it back to the outpost. Doc Martinez treats your wounded. But the weight
of failure is crushing.

Captain Reynolds doesn't sugarcoat it. "We failed those people. They depended on us and
we couldn't protect them."

But he also doesn't blame you. "Wraith riders are extremely dangerous. This mission was
always near-impossible. You did your best against overwhelming odds."

The tactical map now shows the settlement as lost. A reminder of what's at stake. Every
time Rangers fail, people die.

"Learn from this," Reynolds says. "Analyze what went wrong. Train harder. Be better. We
can't bring those people back. But we can make sure it doesn't happen again."

Rangers remember their failures. And they come back stronger.''',

        'conclusion_partial': '''Partial success. Heavy casualties but settlement saved.

You stopped most of the wraith riders, but two broke through. They reached the settlement
and killed several civilians before a Ranger QRF eliminated them.

The settlement survived, but not unscathed. Eight civilians dead. Families destroyed.

Your squad returns to base with wounded. Doc Martinez is overwhelmed with casualties -
both Rangers and civilians. He works through the night, saving who he can.

Captain Reynolds debriefs you. "You stopped six out of eight. Without your ambush, all
eight would have hit the settlement simultaneously. You saved lives."

But partial success feels like failure. Those eight civilians died because two wraiths
got through. Your ambush should have been perfect.

"Don't let it consume you," Reynolds says. "Learn from it. Adjust. Improve. We're fighting
impossible odds. Partial victories are still victories."

The settlement sends thanks to the Rangers. You saved them. Most of them, anyway.

The weight of command: sometimes your best isn't quite enough. But you keep fighting
anyway. That's what Rangers do.''',

        # Rewards (Public Mission)
        'reward_xp': 1500,
        'reward_currency': 300,
        'reward_items': [
            {'item_key': 'iron_blade_blessed', 'quantity': 1},
            {'item_key': 'wraith_rider_trophy', 'quantity': 1}
        ],
        'reward_reputation': {
            'rangers': 25,
            'civilians': 20
        },

        # Parameters
        'time_limit': 5400,  # 90 minutes - time-sensitive
        'can_fail': True,
        'can_abandon': False,  # Civilians depend on you
        'is_repeatable': True,
        'cooldown_hours': 72,  # 3 days

        'target_location_description': 'Valley approach to civilian settlement, Sector 7',
    }
)

print_success(f"Created: {wraith_mission.name} (Public, Very Hard)")

# Create event for the wraith leader duel
wraith_duel_event = MissionEvent.objects.update_or_create(
    mission=wraith_mission,
    key='wraith_leader_duel',
    defaults={
        'name': 'Duel with Wraith Leader',
        'event_type': 'combat',
        'act': 3,
        'trigger_type': 'objective_complete',
        'trigger_conditions': {'objective_key': 'final_defense'},
        'trigger_chance': 1.0,
        'description': '''The wraith leader challenges you to single combat.

This is personal now. The wraith sees you as the one who killed its riders. It wants
revenge. Rangers and wraith riders - old enemies in a new war.

You can accept the duel or have your squad focus fire. But there's something to be said
for answering a challenge. Rangers don't back down.''',
        'is_repeatable': False,
    }
)

print_success(f"  └─ Created event: Wraith Leader Duel")

# ============================================================================
# Mission 2: The Crashed Ranger Bird (Discovery & Rescue)
# ============================================================================
print_section("Mission 2: The Crashed Ranger Bird")

helicopter_mission, created = Mission.objects.update_or_create(
    key='mission_ranger_helicopter',
    defaults={
        'name': 'The Crashed Ranger Bird',
        'mission_type': 'rescue',
        'is_public': True,
        'given_by_npc': captain_reynolds,
        'difficulty': 'hard',
        'required_level': 4,
        'required_squad_size': 3,

        # Hook
        'hook_title': 'Brothers Lost',
        'hook_description': '''Captain Reynolds calls an emergency briefing.

"Twenty-three days ago, a Ranger patrol went missing," he begins, his voice tight with
controlled emotion. "Hawk-Three-One, a UH-60 Black Hawk with six Rangers on board. Last
radio contact placed them thirty klicks northwest, investigating old-world ruins."

He displays aerial reconnaissance photos: a crashed helicopter in dense forest, rotor
blades sheared off, fuselage partially intact.

"We found them," Reynolds says. "Or what's left of their bird. I need a squad to reach
that crash site, determine what happened, and recover any survivors or remains."

The mission is recovery: find out what happened to Hawk-Three-One, bring Rangers home.

"Those Rangers are brothers," Reynolds says. "We don't leave them out there. Not alive,
not dead. They come home."

The crash site is deep in hostile territory. Orcs control the area. Whatever brought down
that helicopter might still be active. This won't be easy.

But Rangers don't leave Rangers behind.

"Gear up," Reynolds orders. "Bring our people home."''',

        # Act 1: The Journey
        'act1_title': 'Act 1: Into Hostile Territory',
        'act1_description': '''Thirty klicks through enemy territory on foot.

Your squad moves tactically: spacing, sectors, noise discipline. This is orc country.
The terrain is rough - forest, hills, old ruins from the pre-collapse world. Signs of
the Dark Army are everywhere: orc camps, patrols, fortifications.

You avoid contact when possible. This is a recovery mission, not a combat op. Stay quiet,
stay hidden, reach the crash site.

Fifteen klicks in, you find signs of the missing Rangers: boot prints in mud, 5.56mm
brass casings, bloodstains on rock. They came through here. They were in contact.

Twenty-five klicks. The forest thickens. You're getting close. Then you see it through
the trees: the shattered remains of Hawk-Three-One.

The Black Hawk crashed hard. Rotor blades are scattered across fifty meters. The fuselage
rests at an angle against a massive tree. Scorch marks indicate fire.

No sign of the crew. Yet.

Your squad approaches cautiously. This could be an ambush. Orcs use bait traps. But you
have to check. Rangers might still be alive.''',

        'act1_objectives': [
            {
                'key': 'navigate_territory',
                'description': 'Navigate 30km through hostile orc territory',
                'required': True
            },
            {
                'key': 'avoid_orc_patrols',
                'description': 'Avoid or bypass orc patrols without major engagement',
                'required': True
            },
            {
                'key': 'find_ranger_signs',
                'description': 'Locate signs of the missing Ranger patrol',
                'required': True
            },
            {
                'key': 'reach_crash_site',
                'description': 'Reach the helicopter crash site',
                'required': True
            },
            {
                'key': 'secure_perimeter',
                'description': 'Secure perimeter around crash site',
                'required': True
            }
        ],

        # Act 2: Investigation
        'act2_title': 'Act 2: What Happened Here',
        'act2_description': '''You investigate the wreckage.

The Black Hawk took heavy damage. The fuselage is riddled with holes - not from the crash,
from weapons. Large-caliber rounds. Maybe even something magical based on the scorch
patterns.

Inside the crew compartment, you find evidence: blood, abandoned equipment, shell casings.
The Rangers survived the crash. They fought here. Hard.

Your communications specialist finds the Black Hawk's black box. Damaged but maybe
recoverable. If Intel can pull data from it, you'll know what brought them down.

Then you find the trail: boot prints leading away from the crash, heading east. The
Rangers evacuated after the crash. At least some of them made it out of the bird alive.

You follow the trail. Blood droplets in the dirt. Discarded medical packaging - they were
treating wounded. More brass casings - they were fighting a running battle.

Half a klick from the crash, you find a makeshift fighting position: hasty fortification,
lots of expended ammunition, more blood. They made a stand here. Bought time.

The trail continues east. Fresher now. Days old, not weeks.

Someone might still be alive.

Then you hear it: distant gunfire. M4A1 carbines. That's Ranger weapons. Someone's in
contact. RIGHT NOW.''',

        'act2_objectives': [
            {
                'key': 'investigate_wreckage',
                'description': 'Investigate the helicopter wreckage thoroughly',
                'required': True
            },
            {
                'key': 'recover_black_box',
                'description': 'Recover the Black Hawk\'s flight recorder',
                'required': True
            },
            {
                'key': 'find_ranger_trail',
                'description': 'Locate the trail of surviving Rangers',
                'required': True
            },
            {
                'key': 'follow_trail',
                'description': 'Follow the trail east from crash site',
                'required': True
            },
            {
                'key': 'locate_survivors',
                'description': 'Locate the source of Ranger weapons fire',
                'required': True
            }
        ],

        # Act 3: The Rescue
        'act3_title': 'Act 3: No Ranger Left Behind',
        'act3_description': '''You rush toward the gunfire.

Through the trees, you see them: three Rangers, pinned down by an orc warband. Twenty-plus
hostiles, closing in. The Rangers are in a small depression, using it for cover. One is
wounded badly. They're running low on ammunition.

They're Hawk-Three-One's survivors. Twenty-three days evading through hostile territory,
fighting the whole way. They've stayed alive through skill, grit, and Ranger
determination.

But they're at the end. This is their last stand.

Unless you intervene.

"RANGERS COMING IN!" you shout. "HOLD POSITION!"

Your squad hits the orcs from the flank. Surprise works in your favor. Controlled fire
drops six orcs before they realize they're being attacked from a new direction.

The survivors recognize friendly forces. One of them - a sergeant, by his rank - grins
despite the desperate situation. "ABOUT DAMN TIME!" he yells. "WE WERE STARTING TO THINK
YOU FORGOT ABOUT US!"

Rangers don't forget Rangers.

Combined fire breaks the orc assault. Your squad and the survivors work together: covering
fire, tactical movement, disciplined shooting. This is what Rangers train for.

The orcs fall back, then retreat. They didn't expect reinforcements. The battle swings
from orc victory to Ranger victory in minutes.

Three survivors: Sergeant First Class Ramirez (Hawk-Three-One's crew chief), Specialist
Hayes (door gunner), and Private Chen (wounded but alive). The pilot, copilot, and one
other Ranger didn't make it. KIA in the crash or the fighting after.

"We need to get home," Ramirez says. He's exhausted, wounded, but still fighting. "We've
got intel on what brought us down. Command needs to hear this."

Extraction time. You've got three survivors and a black box. Now you have to get
everyone back through thirty klicks of hostile territory.

But that's fine. You came for Rangers. You found them. And now you're all going home.''',

        'act3_objectives': [
            {
                'key': 'assault_orcs',
                'description': 'Launch surprise assault on orc forces',
                'required': True
            },
            {
                'key': 'link_up_survivors',
                'description': 'Link up with Hawk-Three-One survivors',
                'required': True
            },
            {
                'key': 'eliminate_orc_threat',
                'description': 'Eliminate or repel orc warband',
                'required': True
            },
            {
                'key': 'treat_wounded',
                'description': 'Provide medical treatment to survivors',
                'required': True
            },
            {
                'key': 'extract_to_outpost',
                'description': 'Extract all personnel back to Ranger Outpost Alpha',
                'required': True
            }
        ],

        # Conclusions
        'conclusion_success': '''Mission accomplished. Rangers recovered and returned home.

Your combined squad makes it back to Ranger Outpost Alpha. The journey was hard - carrying
wounded through hostile territory - but everyone made it.

Doc Martinez meets you at the gate. He immediately takes the wounded to medical bay.
Private Chen needs surgery. Specialist Hayes has infected wounds. SFC Ramirez is
dehydrated and exhausted. But they'll all survive.

Captain Reynolds debriefs the survivors personally. What they tell him is grim: Hawk-
Three-One was brought down by dark wizard magic. Lightning from the sky, disabling the
electronics. The helicopter crashed. The crew evacuated and fought for twenty-three days.

"Three made it," Reynolds says. "Because Rangers don't quit. And because Rangers don't
leave Rangers behind."

He turns to you. "You brought our people home. Some of them dead, but home. Some of them
alive, against all odds. That's what Rangers do for each other."

The black box data confirms it: the Dark Army has anti-air magic capabilities. That
changes tactical planning. No more helicopter operations without magical countermeasures.

The three survivors will recover, return to duty, and keep fighting. Because Rangers
don't quit.

"Outstanding work," Reynolds concludes. "You gave hope back to everyone in this outpost.
Proof that Rangers take care of their own. No matter what."

No Ranger left behind. Promise kept.''',

        'conclusion_failure': '''Mission failed. The survivors were lost.

You reached the survivors too late. The orc warband overwhelmed them before you could
intervene. By the time you fought through to their position, they were dead.

SFC Ramirez, Specialist Hayes, Private Chen - fought for twenty-three days and died
meters away from rescue.

Your squad recovered their bodies and the black box. The extraction was grim and silent.
Rangers carrying fallen Rangers home.

Captain Reynolds meets you at the outpost. The bodies are taken to the medical bay for
identification and preparation. Doc Martinez handles them with respect.

"They were alive," Reynolds says quietly. "If we'd been faster, better, we could have
saved them. But we weren't."

He looks at you. "This isn't your fault. You did everything you could. Sometimes
everything isn't enough in this world."

The black box data reveals what brought them down: dark wizard magic. That intel will save
future lives. But it doesn't change what happened here.

"We brought them home," Reynolds says. "Dead, but home. That's something. It has to be."

Three more Rangers added to the memorial. Three more names. Three more reminders of what's
at stake.

Rangers remember. And Rangers keep fighting.''',

        'conclusion_partial': '''Partial success. Some survivors recovered, but with losses.

You reached the survivors and drove off the orcs. But not before casualties: SFC Ramirez
was killed in the final assault. Specialist Hayes and Private Chen made it out alive.

Your squad brings everyone home: two alive, four dead, and the black box.

Doc Martinez treats the survivors. They'll recover physically. Emotionally will take
longer. Twenty-three days of evasion, watching friends die, narrowly escaping death.

Captain Reynolds debriefs them. The intel about dark wizard anti-air magic is critical.
Future operations will adapt based on what Hawk-Three-One learned the hard way.

"We got two back alive," Reynolds tells you. "That's a win. Not perfect, but a win. You
saved lives today."

But it doesn't feel like a win. SFC Ramirez fought for twenty-three days and died minutes
before he would have been safe.

"He died a Ranger," Reynolds says. "Fighting to the end, protecting his soldiers, never
quitting. There's honor in that. Remember him that way."

Four Rangers killed. Two Rangers saved. The mission math of an impossible situation.

Rangers take care of their own. You did your best. Sometimes that's all you can do.''',

        # Rewards
        'reward_xp': 1200,
        'reward_currency': 250,
        'reward_items': [
            {'item_key': 'helicopter_black_box', 'quantity': 1},
            {'item_key': 'ranger_dog_tags', 'quantity': 1},
            {'item_key': 'survival_kit_military', 'quantity': 1}
        ],
        'reward_reputation': {
            'rangers': 30
        },

        # Parameters
        'time_limit': None,  # No time limit - survivors waited 23 days
        'can_fail': True,
        'can_abandon': False,  # Never abandon fellow Rangers
        'is_repeatable': False,  # One-time story mission
        'cooldown_hours': 0,

        'target_location_description': 'Crashed UH-60 Black Hawk, 30km northwest of outpost',
    }
)

print_success(f"Created: {helicopter_mission.name} (Public, Hard)")

# Create event for discovering the survivors
survivor_discovery = MissionEvent.objects.update_or_create(
    mission=helicopter_mission,
    key='survivor_discovery',
    defaults={
        'name': 'Discover Survivors',
        'event_type': 'discovery',
        'act': 2,
        'trigger_type': 'objective_complete',
        'trigger_conditions': {'objective_key': 'follow_trail'},
        'trigger_chance': 1.0,
        'description': '''You hear M4A1 gunfire in the distance.

That's Ranger weapons. That means Rangers are alive and fighting. Twenty-three days after
their helicopter crashed, survivors are still out here.

Your squad immediately moves toward the sound. Rangers help Rangers. Always.''',
        'is_repeatable': False,
    }
)

print_success(f"  └─ Created event: Survivor Discovery")

# ============================================================================
# Mission 3: Strike the Dark Wizard Coven (Assassination/Raid)
# ============================================================================
print_section("Mission 3: Strike the Dark Wizard Coven")

wizard_mission, created = Mission.objects.update_or_create(
    key='mission_wizard_coven_strike',
    defaults={
        'name': 'Strike the Dark Wizard Coven',
        'mission_type': 'assassination',
        'is_public': True,
        'given_by_npc': captain_reynolds,
        'difficulty': 'extreme',
        'required_level': 7,
        'required_squad_size': 6,

        # Hook
        'hook_title': 'Kill the Wizards',
        'hook_description': '''Captain Reynolds calls a commanders briefing. This is serious.

"Intel from CPL Chen confirms it," Reynolds begins, his voice hard. "The dark wizard coven
that's been supporting orc operations is conducting a major ritual. Location: old temple
ruins, grid reference 441-865."

He displays reconnaissance photos: six robed figures around a ritual circle, glowing with
malevolent energy. The air around them shimmers with dark magic.

"Chen's analysis says if they complete this ritual, we're in serious trouble. Best case:
they summon reinforcements from the Lich Pharaoh's armies. Worst case: they curse this
entire region. Either way, Rangers die and the outpost is threatened."

Reynolds looks around the room at the assembled Rangers.

"This is an assassination op. Six dark wizards, unknown number of orc guards, in the
middle of hostile territory. We go in hard, kill the wizards before they complete the
ritual, and extract."

He pauses. "This is extremely dangerous. Dark wizards throw lightning, fire, death magic.
They can kill you from range before you close to melee. We've lost Rangers to wizards
before."

But the alternative is worse. If that ritual completes, the strategic situation changes.
The Dark Army gets stronger. Rangers get weaker.

"I need volunteers," Reynolds says. "This is a death-or-glory op. We might not all come
back. But we're Rangers. When the mission is impossible, that's when they call us."

Every Ranger in the room volunteers.

Reynolds selects the best: experienced squad leaders, sharpshooters, combat veterans.
This is an all-star team for a nightmare mission.

"Gear up," Reynolds orders. "We hit them at dawn. Disrupted night vision gives us an edge.
Get in, kill the wizards, get out."

Simple plan. Brutal execution. This is what Rangers do.

Rangers are about to teach the Dark Army a lesson: you can have magic. Rangers have
marksmanship, tactics, and the refusal to quit. Let's see which is stronger.''',

        # Act 1: Infiltration
        'act1_title': 'Act 1: Into the Dark',
        'act1_description': '''Your strike team moves out pre-dawn.

Six Rangers: you as team leader, two expert marksmen, one combat medic, one breacher
with demolitions, one communications specialist. The best of the best.

The approach is through dangerous territory. This is deep in Dark Army control. Orc
patrols are constant. You move like ghosts: silent, invisible, deadly when necessary.

Three hours of movement. Zero contact. Your team is too skilled to be spotted.

As dawn approaches, you reach the temple ruins. Ancient structure, crumbling stone,
overgrown with vegetation. The dark wizards have claimed it for their ritual.

Through your optic, you count targets:
- Six dark wizards in ritual circle (primary targets)
- Twelve orc guards on perimeter (secondary)
- Unknown forces inside the temple structure

Your marksmen select positions: overlapping fields of fire, clear sight lines to the
ritual circle, escape routes planned. Your breacher prepares charges in case you need to
demolish the temple. Combat medic readies trauma supplies.

The wizards begin their ritual. You can see dark energy coalescing around them. Whatever
they're summoning, it's starting to manifest.

Time's up. You have to hit them now.

"All teams, stand by," you whisper into your radio. "Weapons hot. Target the wizards.
Orc guards are secondary. Execute on my mark."

The sun breaks the horizon. Dawn light catches the temple ruins.

"Execute."''',

        'act1_objectives': [
            {
                'key': 'infiltrate_territory',
                'description': 'Infiltrate to temple ruins without detection',
                'required': True
            },
            {
                'key': 'establish_overwatch',
                'description': 'Establish overwatch positions for marksmen',
                'required': True
            },
            {
                'key': 'identify_targets',
                'description': 'Identify and prioritize all six dark wizards',
                'required': True
            },
            {
                'key': 'prepare_breach',
                'description': 'Prepare demolition charges (contingency)',
                'required': True
            },
            {
                'key': 'await_dawn',
                'description': 'Wait for dawn (disrupts wizard night vision)',
                'required': True
            }
        ],

        # Act 2: The Strike
        'act2_title': 'Act 2: Headshots and Lightning',
        'act2_description': '''Six shots fired simultaneously. Six wizards targeted.

Four wizards drop instantly. Headshots. They were focusing on their ritual, vulnerable,
unaware. Precision marksmanship eliminates them before they can react.

Two wizards survive the initial volley. They turn, see the threat, and immediately begin
casting.

"INCOMING!" someone yells.

Lightning arcs across the temple ruins. It hits near your breacher - he's thrown back by
the blast, smoking. Your medic is already moving to him.

Your marksmen re-acquire the surviving wizards. Two more shots. One wizard drops. One
remains, and he's furious.

The orc guards realize they're under attack. They charge your positions. You're combat
veterans - you don't panic. Controlled fire drops the first wave. The second wave is
smarter, using cover.

The surviving dark wizard is casting something big. You can see dark energy building
around him. Whatever it is, you can't let him complete it.

"PRIORITY TARGET!" you order. "TAKE THAT WIZARD DOWN!"

Multiple Rangers engage the wizard. He's shielded somehow - bullets impact magical
barriers and dissipate. He's protected.

But Rangers adapt. Your demolitions expert recovers and launches a 40mm grenade from his
M320. The grenade punches through the magical shield and detonates.

The wizard staggers. His concentration breaks. The spell he was casting backfires in
spectacular fashion - dark energy explodes outward, consuming him.

Six dark wizards. All dead. Mission accomplished.

Except now you have to extract through an entire orc encampment that knows you're here.

"EXFIL NOW!" you order. "FIGHTING WITHDRAWAL!"

The battle is just beginning.''',

        'act2_objectives': [
            {
                'key': 'initial_volley',
                'description': 'Execute simultaneous shots on all six wizards',
                'required': True
            },
            {
                'key': 'kill_four_wizards',
                'description': 'Confirm kills on at least four dark wizards',
                'required': True
            },
            {
                'key': 'survive_lightning',
                'description': 'Survive dark wizard lightning attacks',
                'required': True
            },
            {
                'key': 'eliminate_final_wizards',
                'description': 'Eliminate remaining dark wizards',
                'required': True
            },
            {
                'key': 'disrupt_ritual',
                'description': 'Prevent completion of dark ritual',
                'required': True
            }
        ],

        # Act 3: Extraction Under Fire
        'act3_title': 'Act 3: Run the Gauntlet',
        'act3_description': '''Extracting through a hornet's nest.

Every orc in the area knows there are Rangers at the temple. They're converging on your
position. You count at least fifty hostiles, probably more.

Your team moves fast: bounding overwatch, covering fire, tactical retreat. Modern infantry
tactics against fantasy enemies.

Orcs charge. Your team drops them with controlled fire. But there are always more. The
ammunition situation is becoming critical.

"CONSERVE AMMO!" you order. "MAKE SHOTS COUNT!"

Your marksmen are invaluable: one shot, one kill, each round eliminating a threat. Your
breacher uses his last 40mm grenades to break up orc formations. Your medic is treating
wounded while running.

Two klicks from the temple, you reach a chokepoint: a narrow ravine. Good defensive
position. Your team makes a stand there, laying down suppressing fire while the wounded
move through.

The orcs mass for a final assault. This is it. Hold here or die here.

Your team unleashes everything: rifles, grenades, even old-fashioned grenades scavenged
from the temple. The ravine becomes a kill zone.

The orc assault breaks. Too many casualties. They fall back.

Your team uses the opportunity to extract. Three more klicks of tactical movement, then
you're in Ranger-controlled territory. Safe.

You made it. All six wizards dead. Ritual disrupted. And your team survived against
impossible odds.

Rangers just hit the Dark Army's elite and came out on top.''',

        'act3_objectives': [
            {
                'key': 'begin_extraction',
                'description': 'Begin tactical withdrawal from temple',
                'required': True
            },
            {
                'key': 'fighting_retreat',
                'description': 'Conduct fighting retreat through orc forces',
                'required': True
            },
            {
                'key': 'hold_chokepoint',
                'description': 'Hold defensive position at ravine chokepoint',
                'required': True
            },
            {
                'key': 'break_orc_assault',
                'description': 'Repel final orc assault',
                'required': True
            },
            {
                'key': 'extract_all_personnel',
                'description': 'Extract entire team to Ranger territory',
                'required': True
            }
        ],

        # Conclusions
        'conclusion_success': '''Mission accomplished. Dark wizard coven eliminated.

Your strike team returns to Ranger Outpost Alpha as heroes.

The mission was a complete success: all six dark wizards killed, ritual disrupted, team
extracted with only minor injuries. This is textbook special operations.

Captain Reynolds personally debriefs you. "Six dark wizards. The Dark Army's magical
support for this entire region. And you eliminated them in a single strike."

CPL Chen confirms the strategic impact: "Without those wizards, orc operations lose their
magical support. No more lightning strikes. No more ritual magic. No more cursed weapons.
This changes the tactical balance significantly."

The Dark Army will retaliate. They'll be furious. But for now, Rangers have the advantage.

"You hit their elite forces and came out on top," Reynolds says. "That sends a message:
Rangers can reach anywhere, kill anyone, and extract successfully. The Dark Army thought
their wizards were untouchable. You proved them wrong."

The other Rangers look at your strike team with new respect. You took on an extreme
mission and executed perfectly. That's the Ranger standard.

"Outstanding work," Reynolds concludes. "Some missions are impossible. Rangers do them
anyway. This was one of those missions. And you made it look easy."

The Dark Army just learned: wizards might have magic, but Rangers have marksmanship,
tactics, and the will to do impossible things. Rangers win.''',

        'conclusion_failure': '''Mission failed. The strike team was lost.

The dark wizards were too powerful. The ritual was too close to completion. Your team
fought brilliantly but was overwhelmed by dark magic.

Only two Rangers made it back: your communications specialist and one marksman. The rest
were killed by wizard magic during the assault or the extraction.

Captain Reynolds receives the survivors personally. They're in shock, wounded, barely
alive. Doc Martinez takes them to medical bay.

The debrief is grim: four Rangers KIA, six dark wizards still alive, ritual possibly
completed. Strategic failure.

"We lost good Rangers," Reynolds says, his voice heavy. "Experienced soldiers, people we
depended on. Gone because we underestimated the threat."

CPL Chen's analysis is worse: the ritual may have completed before your strike. If so,
the Dark Army just got significantly stronger.

The memorial wall gets four new names. Four more Rangers who died fighting impossible odds.

"We'll try again," Reynolds says. "Learn from this. Train harder. Be better. We can't
bring them back. But we can make sure their sacrifice means something."

Rangers remember their dead. And Rangers keep fighting.''',

        'conclusion_partial': '''Partial success. Wizards dead but heavy casualties.

You eliminated all six dark wizards and disrupted the ritual. Mission accomplished.

But the cost was high: three Rangers KIA during the extraction. Your breacher, one
marksman, and your communications specialist didn't make it.

The surviving three Rangers return to base: you, one marksman, and your medic. You're
wounded, exhausted, traumatized. But alive.

Captain Reynolds debriefs you in medical bay while Doc Martinez treats your injuries.

"Six wizards dead," Reynolds says. "Ritual disrupted. Strategic success. But we paid
for it."

Three Rangers killed. The outpost memorial wall gets three new names. Rangers who died
completing an impossible mission.

"They died as Rangers," Reynolds says. "Fighting to the end, never quitting, completing
the mission no matter what. There's honor in that."

CPL Chen confirms the strategic impact: the Dark Army lost critical magical support. That
will affect their operations for months. Your team's sacrifice bought time and advantage.

But it doesn't feel like victory when you're carrying dead friends home.

"You did what had to be done," Reynolds says. "Sometimes victory costs more than we want
to pay. But we pay it anyway. That's what Rangers do."

Mission accomplished. At terrible cost. But accomplished.''',

        # Rewards
        'reward_xp': 2000,
        'reward_currency': 500,
        'reward_items': [
            {'item_key': 'dark_wizard_staff', 'quantity': 1},
            {'item_key': 'ritual_tome', 'quantity': 1},
            {'item_key': 'rangers_valor_medal', 'quantity': 1}
        ],
        'reward_reputation': {
            'rangers': 40
        },

        # Failure consequences
        'failure_consequences': {
            'type': 'dark_army_ritual_complete',
            'effects': {
                'dark_army_strength': '+15%',
                'orc_morale': '+10',
                'ranger_casualties_increase': True
            }
        },

        # Parameters
        'time_limit': 10800,  # 3 hours - must hit them during ritual
        'can_fail': True,
        'can_abandon': False,  # Too critical to abandon
        'is_repeatable': False,  # One-time major operation
        'cooldown_hours': 0,

        'target_location_description': 'Ancient temple ruins, grid reference 441-865',
    }
)

print_success(f"Created: {wizard_mission.name} (Public, Extreme)")

# Create choice event for wizard encounter
wizard_choice = MissionEvent.objects.update_or_create(
    mission=wizard_mission,
    key='wizard_surrender_offer',
    defaults={
        'name': 'The Surviving Wizard\'s Offer',
        'event_type': 'choice',
        'act': 2,
        'trigger_type': 'objective_complete',
        'trigger_conditions': {'objective_key': 'kill_four_wizards'},
        'trigger_chance': 0.3,  # 30% chance
        'description': '''One of the surviving dark wizards raises his hands.

"Wait!" he shouts in accented English. "I surrender! I have information! I'll tell you
about the Lich Pharaoh's plans!"

He's wounded, his magic depleted. He's offering intelligence in exchange for his life.

Your marksman has him in the crosshairs. One word and the wizard dies.

Do you take prisoners? Or do you eliminate all threats?''',
        'choices': [
            {
                'text': 'Capture the wizard for interrogation',
                'outcome': 'capture',
                'requirements': {}
            },
            {
                'text': 'Execute the wizard - no prisoners',
                'outcome': 'execute',
                'requirements': {}
            }
        ],
        'outcomes': {
            'capture': {
                'description': '''You order your team to capture the wizard.

"Secure him!" you command. Your team moves in, binds the wizard with zip ties, and
searches him for hidden weapons or components.

The wizard is now a prisoner. Intel will interrogate him. Whatever he knows about the
Lich Pharaoh's plans could save Ranger lives.

But you now have to extract with a prisoner through hostile territory. That complicates
things.''',
                'effects': {
                    'prisoner_captured': True,
                    'intelligence_bonus': True,
                    'extraction_difficulty': '+1'
                }
            },
            'execute': {
                'description': '''You give the order with a simple gesture.

Your marksman fires. The wizard drops. No prisoners today.

The mission is cleaner without a prisoner to protect during extraction. And you eliminated
a threat permanently.

Whatever intelligence the wizard had dies with him. But you completed the primary mission:
all six dark wizards dead.''',
                'effects': {
                    'all_wizards_dead': True,
                    'extraction_difficulty': 'normal'
                }
            }
        },
        'is_repeatable': False,
    }
)

print_success(f"  └─ Created event: Wizard Surrender Offer")

# Summary
print_section("Mission Creation Complete!")
print()
print_success(f"Created 3 lore-based missions:")
print()
print(f"{Color.CYAN}1. Wraith Rider Ambush{Color.END}")
print(f"   Type: Defense | Difficulty: Very Hard | Level: 5+ | Squad: 4+")
print(f"   {Color.MAGENTA}Defend a civilian settlement from elite Dark Army cavalry{Color.END}")
print(f"   Rewards: 1500 XP, Iron Blessed Blade, Wraith Trophy")
print()
print(f"{Color.CYAN}2. The Crashed Ranger Bird{Color.END}")
print(f"   Type: Rescue | Difficulty: Hard | Level: 4+ | Squad: 3+")
print(f"   {Color.MAGENTA}Recover a lost Ranger helicopter crew from hostile territory{Color.END}")
print(f"   Rewards: 1200 XP, Black Box, Dog Tags, Survival Kit")
print()
print(f"{Color.CYAN}3. Strike the Dark Wizard Coven{Color.END}")
print(f"   Type: Assassination | Difficulty: Extreme | Level: 7+ | Squad: 6+")
print(f"   {Color.MAGENTA}Eliminate six dark wizards before they complete a dark ritual{Color.END}")
print(f"   Rewards: 2000 XP, Wizard Staff, Ritual Tome, Valor Medal")
print()
print(f"{Color.YELLOW}Features:{Color.END}")
print("  ✓ Rich narrative based on Forgotten Ruin lore")
print("  ✓ Three-act cinematic structure")
print("  ✓ Multiple difficulty levels (Hard, Very Hard, Extreme)")
print("  ✓ Optional events with player choices")
print("  ✓ Success/Failure/Partial outcomes")
print("  ✓ Strategic consequences for server state")
print()
print(f"{Color.BLUE}Test with:{Color.END}")
print("  python manage.py makemigrations")
print("  python manage.py migrate")
print("  python create_lore_missions.py")
print()
