#!/usr/bin/env python
"""
Create Example Missions

Creates example public and private missions demonstrating the mission system
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
    END = '\033[0m'

def print_success(msg):
    print(f"{Color.GREEN}✓ {msg}{Color.END}")

def print_section(msg):
    print(f"\n{Color.YELLOW}{'='*70}\n{msg}\n{'='*70}{Color.END}")

# Get NPCs
try:
    captain_reynolds = NPC.objects.get(key='captain_reynolds')
    doc_martinez = NPC.objects.get(key='doc_martinez')
except NPC.DoesNotExist:
    print("Error: Required NPCs not found. Run setup_outpost_interactive.py first.")
    exit(1)

print_section("Creating Example Missions")

# ============================================================================
# Mission 1: Recon Patrol (Public Mission)
# ============================================================================
print_section("Mission 1: Northern Recon Patrol")

recon_mission, created = Mission.objects.update_or_create(
    key='mission_recon_north',
    defaults={
        'name': 'Northern Recon Patrol',
        'mission_type': 'recon',
        'is_public': True,
        'given_by_npc': captain_reynolds,
        'difficulty': 'moderate',
        'required_level': 1,
        'required_squad_size': 2,

        # Hook
        'hook_title': 'Eyes on the Enemy',
        'hook_description': '''Captain Reynolds briefs you in the tactical operations center. Maps cover the walls,
red markers showing enemy positions like a rash spreading across the territory.

"We need intel, Ranger," Reynolds says, tapping a map location north of the outpost.
"Orc forces are massing at grid reference 437-862. We need to know what we're facing."

He slides a mission brief across the table: observe enemy positions, count hostiles,
identify leaders, and report back. Standard reconnaissance operation.

"This is stealth work," Reynolds emphasizes. "Get eyes on target, don't get compromised.
We need intelligence, not a firefight. Can you handle it?"

The northern territories are dangerous. Orc patrols are common. But Rangers are trained
for this. Observe, report, survive.''',

        # Act 1: Insertion and Movement
        'act1_title': 'Act 1: Insertion',
        'act1_description': '''You move north from Ranger Outpost Alpha under cover of pre-dawn darkness.

The terrain transitions from fortified outpost to wilderness quickly. Trees close in,
providing concealment but limiting visibility. This is hostile territory.

Your squad moves tactically: spacing maintained, sectors covered, noise discipline.
Modern Ranger skills applied to a fantasy battlefield.

After two hours of careful movement, you reach the observation position overlooking
the orc encampment. Time to gather intelligence.''',

        'act1_objectives': [
            {
                'key': 'reach_observation_point',
                'description': 'Reach the observation point overlooking enemy positions',
                'required': True
            },
            {
                'key': 'establish_overwatch',
                'description': 'Set up observation post with clear line of sight',
                'required': True
            },
            {
                'key': 'radio_checkin',
                'description': 'Radio check-in with command',
                'required': True
            }
        ],

        # Act 2: Observation and Intelligence Gathering
        'act2_title': 'Act 2: Intelligence Gathering',
        'act2_description': '''From your concealed position, you observe the orc encampment.

It's larger than expected. Crude fortifications surround multiple fire pits. Orcs move
between structures - you count at least 40, possibly more.

Through your rifle optic, you identify key targets:
- An orc chieftain, larger than the others, giving orders
- Dark wizard in black robes, conducting some kind of ritual
- Supply depot with crude weapons and what looks like stolen Ranger equipment

This is critical intel. Command needs this information.

But then complications: an orc patrol approaches your position. They haven't spotted you
yet, but they're getting close. Do you break cover or maintain position?''',

        'act2_objectives': [
            {
                'key': 'count_hostiles',
                'description': 'Count enemy forces (40+ orcs confirmed)',
                'required': True
            },
            {
                'key': 'identify_leaders',
                'description': 'Identify orc chieftain and dark wizard',
                'required': True
            },
            {
                'key': 'locate_supplies',
                'description': 'Locate enemy supply depot',
                'required': True
            },
            {
                'key': 'avoid_patrol',
                'description': 'Evade orc patrol without compromising position',
                'required': True
            }
        ],

        # Act 3: Extraction
        'act3_title': 'Act 3: Exfiltration',
        'act3_description': '''With intelligence gathered, it's time to extract.

You withdraw from the observation point using a different route. The orc patrol is
still searching, but they haven't found your position.

Movement is slow and deliberate. Every sound could give you away. This is where
discipline and training pay off.

As you near Ranger territory, you spot something unexpected: a crashed helicopter,
old but recognizable. Rangers were here before. Recently.

Intel gathered, mission almost complete. Just need to make it back to report.''',

        'act3_objectives': [
            {
                'key': 'withdraw_undetected',
                'description': 'Withdraw from observation point without detection',
                'required': True
            },
            {
                'key': 'investigate_crash_site',
                'description': 'Investigate crashed helicopter (optional)',
                'required': False
            },
            {
                'key': 'return_to_outpost',
                'description': 'Return to Ranger Outpost Alpha',
                'required': True
            },
            {
                'key': 'debrief_command',
                'description': 'Report intelligence to Captain Reynolds',
                'required': True
            }
        ],

        # Conclusions
        'conclusion_success': '''Mission accomplished.

You debrief Captain Reynolds in the tactical operations center. The intelligence you
gathered is critical: 40+ orcs, organized under a chieftain, supported by dark wizard
forces. The supply depot confirms they're planning an extended campaign.

"Excellent work, Ranger," Reynolds says, updating the tactical map with your intel.
"This information gives us options. We can plan countermeasures, disrupt their supply
lines, maybe even preempt their offensive."

He marks the helicopter crash site for investigation. Rangers were there. Maybe recently.
Questions to answer, but that's for another mission.

"You did good work out there," Reynolds concludes. "Stealth discipline, accurate
reporting, clean extraction. That's Ranger-quality reconnaissance."

Your squad returns to the outpost. Mission complete. Intelligence gathered. Rangers
are a little bit safer because of your work.''',

        'conclusion_failure': '''Mission failure.

The orc patrol spotted you. Stealth compromised. You had to fight your way out.

You made it back to the outpost, but the intelligence is incomplete. The orcs know
someone was watching. They'll increase security, maybe relocate.

Captain Reynolds is understanding but disappointed. "You got compromised, Ranger.
That happens. But now they know we're watching. That makes the next mission harder."

Lessons learned. Next time, better concealment. Better noise discipline. Rangers
learn from failures and come back stronger.''',

        'conclusion_partial': '''Partial success.

You gathered some intelligence, but not everything. The orc patrol forced you to extract
early. You got counts and leader identification, but couldn't assess their full
defensive positions or supply situation.

"It's something," Reynolds says, updating what he can on the tactical map. "Not complete,
but it gives us a starting point. Good work getting out when things went sideways."

Partial intel is better than no intel. And you survived. That counts for something.''',

        # Rewards (Public Mission)
        'reward_xp': 500,
        'reward_currency': 100,
        'reward_items': [
            {'item_key': 'tactical_binoculars', 'quantity': 1}
        ],
        'reward_reputation': {
            'rangers': 10
        },

        # Parameters
        'time_limit': 7200,  # 2 hours
        'can_fail': True,
        'can_abandon': True,
        'is_repeatable': True,
        'cooldown_hours': 24,

        # Target location
        'target_location_description': 'Grid reference 437-862, northern orc encampment',
    }
)

print_success(f"Created: {recon_mission.name} (Public)")

# ============================================================================
# Mission 2: Medical Supply Run (Public Mission)
# ============================================================================
print_section("Mission 2: Emergency Medical Supply Run")

medical_mission, created = Mission.objects.update_or_create(
    key='mission_medical_supplies',
    defaults={
        'name': 'Emergency Medical Supply Run',
        'mission_type': 'scavenge',
        'is_public': True,
        'given_by_npc': doc_martinez,
        'difficulty': 'hard',
        'required_level': 3,
        'required_squad_size': 3,

        # Hook
        'hook_title': 'Critical Shortage',
        'hook_description': '''Doc Martinez calls you to the medical bay. The situation is grim.

"We're running critical on antibiotics," he says, showing you the nearly empty supply
cabinet. "In three days, we're out. After that, any infection becomes potentially fatal."

He pulls out a map marked with pre-collapse medical facilities.

"There's an old hospital fifteen klicks east. It's in orc territory, possibly occupied.
But if there are any medical supplies left in this region, they're there."

Martinez looks at you seriously. "I need antibiotics, IV supplies, surgical equipment,
anything medical you can scavenge. Without resupply, Rangers die from simple infections."

This is a critical mission. The outpost's survival depends on medical supplies. Time
to raid an old-world hospital in hostile territory.''',

        # Act 1: Approach and Assessment
        'act1_title': 'Act 1: Hospital Approach',
        'act1_description': '''The hospital looms ahead: a ruined pre-collapse structure.

It's five stories of broken windows and crumbling concrete. Nature has reclaimed parts
of it. But it's intact enough that supplies might have survived.

Your squad scouts the perimeter. Signs of orc presence: crude fortifications at the
entrance, tracks in the dirt, the smell of their cook fires.

They're using the hospital as a forward base. That complicates things.

You have options: stealth approach through a service entrance, frontal assault through
the main entrance, or find an alternate way in through the upper floors.

Decision time. How do you get inside?''',

        'act1_objectives': [
            {
                'key': 'reach_hospital',
                'description': 'Reach the old hospital location',
                'required': True
            },
            {
                'key': 'scout_perimeter',
                'description': 'Scout the perimeter and assess orc presence',
                'required': True
            },
            {
                'key': 'find_entry_point',
                'description': 'Identify entry point into hospital',
                'required': True
            }
        ],

        # Act 2: Interior Operations
        'act2_title': 'Act 2: Supply Scavenging',
        'act2_description': '''Inside the hospital, things get complicated.

The interior is a maze of collapsed hallways and ruined rooms. Medical equipment
is scattered everywhere, looted and discarded by orcs who don't recognize its value.

You find the pharmacy: partially intact. Medication on the shelves, some expired,
some still viable. Doc Martinez will sort through it. You load up.

Surgical supplies in the operating rooms. IV equipment. Antibiotics. Exactly what
you need.

But then: orcs. A patrol inside the hospital. They haven't spotted you yet, but
they're between you and your exit point.

Combat is likely. But if you can avoid it, the extraction will be cleaner.''',

        'act2_objectives': [
            {
                'key': 'locate_pharmacy',
                'description': 'Find the hospital pharmacy',
                'required': True
            },
            {
                'key': 'scavenge_antibiotics',
                'description': 'Scavenge antibiotics and medications',
                'required': True
            },
            {
                'key': 'gather_surgical_supplies',
                'description': 'Collect surgical supplies and IV equipment',
                'required': True
            },
            {
                'key': 'deal_with_orcs',
                'description': 'Deal with orc patrol (stealth or combat)',
                'required': True
            }
        ],

        # Act 3: Extraction Under Fire
        'act3_title': 'Act 3: Fighting Withdrawal',
        'act3_description': '''The orcs know you're here now.

Whether you fought the patrol or they discovered your presence another way, the alarm
is raised. Orcs are converging on your position.

Your squad is loaded down with medical supplies. Movement is slower. But you can't
drop the supplies - that's the whole mission.

Fighting withdrawal: covering fire, controlled retreat, squad discipline. Modern
tactics against fantasy enemies.

The hospital exit is ahead. Orcs are behind and flanking. Your squad lays down
suppressing fire, making every shot count.

This is what Rangers train for: mission accomplishment under fire. Get the supplies
out, no matter what.''',

        'act3_objectives': [
            {
                'key': 'break_contact',
                'description': 'Break contact with orc forces',
                'required': True
            },
            {
                'key': 'protect_supplies',
                'description': 'Protect medical supplies during extraction',
                'required': True
            },
            {
                'key': 'extract_hospital',
                'description': 'Extract from hospital successfully',
                'required': True
            },
            {
                'key': 'return_supplies',
                'description': 'Deliver supplies to Doc Martinez',
                'required': True
            }
        ],

        # Conclusions
        'conclusion_success': '''Mission accomplished. Medical supplies secured.

Doc Martinez meets you at the outpost entrance. Your squad is battered, ammunition low,
but the supplies are intact.

"You got them," Martinez says, relief evident in his voice. He immediately starts
sorting through the supplies: antibiotics, IV equipment, surgical supplies, medications.

"This buys us time. Months of supplies, maybe more. You just saved Ranger lives that
haven't even been wounded yet."

He catalogues everything meticulously. Every piece of equipment, every medication.
The medical bay is restocked.

"Outstanding work," Martinez concludes. "That was a dangerous op. You went into orc
territory, scavenged what we needed, and got out under fire. That's Ranger-quality
mission execution."

The outpost medical situation is stable. Rangers will survive wounds and infections
because of your mission. That's worth celebrating.''',

        'conclusion_failure': '''The supplies were lost.

You made it back to the outpost, but the medical supplies didn't. In the chaos of the
extraction, the packs were abandoned or destroyed.

Doc Martinez tries to hide his disappointment, but it's there. "You tried, Ranger.
Sometimes missions don't work out. We'll make do with what we have."

But you know the truth: without antibiotics, Rangers will die from infections. Simple
wounds will become fatal. The medical situation is critical.

Lessons learned. Next time: better planning, better execution, better protection of
mission-critical supplies.''',

        'conclusion_partial': '''Partial success. Some supplies recovered.

You got out with about half the medical supplies. The rest were lost in the fighting.

Doc Martinez assesses what you brought back. "It's something. Not enough, but better
than nothing. This buys us a few weeks, maybe a month."

Half success is still partial failure. Rangers needed those supplies. But you did
what you could under impossible circumstances.

"You tried," Martinez says. "That counts for something. We'll make another run when
we can."''',

        # Rewards
        'reward_xp': 750,
        'reward_currency': 200,
        'reward_items': [
            {'item_key': 'combat_medic_badge', 'quantity': 1}
        ],
        'reward_reputation': {
            'rangers': 15
        },

        # Parameters
        'time_limit': None,  # No time limit
        'can_fail': True,
        'can_abandon': False,  # Too critical to abandon
        'is_repeatable': True,
        'cooldown_hours': 168,  # 1 week cooldown

        'target_location_description': 'Old hospital, 15km east of outpost',
    }
)

print_success(f"Created: {medical_mission.name} (Public)")

# ============================================================================
# Mission 3: Private Mission Example - Personal Patrol
# ============================================================================
print_section("Mission 3: Personal Patrol (Private Mission Example)")

private_mission, created = Mission.objects.update_or_create(
    key='mission_private_patrol_example',
    defaults={
        'name': 'Personal Patrol: Testing Your Skills',
        'mission_type': 'patrol',
        'is_public': False,  # Private mission - no server impact
        'difficulty': 'easy',
        'required_level': 1,
        'required_squad_size': 1,

        # Hook
        'hook_title': 'Solo Patrol',
        'hook_description': '''You decide to test your skills with a solo patrol.

No formal orders. No mission briefing. Just you, your rifle, and the wilderness around
the outpost. A personal challenge to see if you have what it takes.

The perimeter extends about a klick from the outpost in all directions. Your patrol
route will take you around the northern approach, through the tree line, and back to
base.

It's dangerous out there. But Rangers don't stay safe inside the wire. Time to patrol.''',

        # Act 1
        'act1_title': 'Act 1: Beginning Patrol',
        'act1_description': '''You move beyond the outpost perimeter, alone.

The wilderness is quiet. Too quiet. Every rustle could be an orc patrol. Every shadow
could be a threat. But you move tactically, using your training.

Spacing doesn't matter when you're solo, but sector awareness does. You scan constantly,
rifle ready, senses alert.

This is how you learn: by doing, by patrolling, by putting yourself in situations where
mistakes cost you.''',

        'act1_objectives': [
            {
                'key': 'leave_outpost',
                'description': 'Leave Ranger Outpost Alpha',
                'required': True
            },
            {
                'key': 'reach_first_checkpoint',
                'description': 'Reach first patrol checkpoint',
                'required': True
            }
        ],

        # Act 2
        'act2_title': 'Act 2: Contact',
        'act2_description': '''You encounter orcs.

Two of them, scouts probably. They haven't seen you yet. You're downwind, concealed
in brush, with the advantage.

Decision time: engage or avoid?

Engaging risks noise and attention. Avoiding is safer but lets them continue their patrol.

What would a Ranger do? Mission first. And your mission is personal skill development.

Your call.''',

        'act2_objectives': [
            {
                'key': 'encounter_orcs',
                'description': 'Encounter orc scouts',
                'required': True
            },
            {
                'key': 'make_tactical_decision',
                'description': 'Decide whether to engage or avoid',
                'required': True
            }
        ],

        # Act 3
        'act3_title': 'Act 3: Return',
        'act3_description': '''You complete your patrol and return to base.

Whatever decision you made with the orc scouts, you learned from it. That's the point
of personal patrols: learning, adapting, improving.

The outpost gate comes into view. You made it. Solo patrol completed.

Not an official mission. No XP rewards. But you tested yourself and came back. That's
what matters.''',

        'act3_objectives': [
            {
                'key': 'complete_patrol_route',
                'description': 'Complete patrol route',
                'required': True
            },
            {
                'key': 'return_safely',
                'description': 'Return to Ranger Outpost Alpha',
                'required': True
            }
        ],

        # Conclusions
        'conclusion_success': '''Personal mission accomplished.

You completed your patrol, made tactical decisions, and returned safely. No fanfare,
no official recognition. But you know: you tested yourself and passed.

This is how Rangers improve. Personal challenges. Solo operations. Pushing boundaries.

Ready for the next challenge whenever you want it.''',

        'conclusion_failure': '''Things didn't go as planned.

Maybe you got wounded. Maybe you made bad tactical decisions. Maybe you learned the
hard way that solo patrols are dangerous.

But you're alive. You learned. And personal missions don't have official consequences.
You can try again, apply the lessons learned, and do better next time.

That's the point of private missions: learning without server-wide consequences.''',

        # No rewards (private mission)
        'reward_xp': 0,
        'reward_currency': 0,
        'reward_items': [],

        # Parameters
        'time_limit': None,
        'can_fail': True,
        'can_abandon': True,
        'is_repeatable': True,
        'cooldown_hours': 0,

        'target_location_description': 'Perimeter patrol around Ranger Outpost Alpha',
    }
)

print_success(f"Created: {private_mission.name} (Private - No Server Impact)")

# Summary
print_section("Mission Creation Complete")
print_success(f"Created 3 example missions:")
print(f"  1. {Color.CYAN}{recon_mission.name}{Color.END} (Public, Moderate)")
print(f"  2. {Color.CYAN}{medical_mission.name}{Color.END} (Public, Hard)")
print(f"  3. {Color.CYAN}{private_mission.name}{Color.END} (Private, Easy)")
print()
print(f"{Color.BLUE}Public missions award XP, currency, and items{Color.END}")
print(f"{Color.BLUE}Private missions are personal narratives without server impact{Color.END}")
print()
print(f"{Color.YELLOW}Test missions with:{Color.END}")
print("  GET  /api/v1/missions/")
print("  GET  /api/v1/missions/<key>/")
print("  POST /api/v1/missions/<key>/accept/")
print()
