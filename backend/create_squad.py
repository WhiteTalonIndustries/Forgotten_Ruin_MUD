#!/usr/bin/env python
"""
Create a Ranger Squad for a player

This script creates a 9-person US Army Ranger squad based on the Forgotten Ruin lore.
"""
import os
import django
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from game.models import Player, Squad, SquadMember


# Sample names for squad members
FIRST_NAMES = [
    'James', 'Michael', 'Robert', 'John', 'David', 'William', 'Richard', 'Joseph',
    'Thomas', 'Christopher', 'Daniel', 'Matthew', 'Anthony', 'Mark', 'Donald', 'Steven',
    'Andrew', 'Joshua', 'Kenneth', 'Kevin', 'Brian', 'Timothy', 'Ronald', 'Jason',
]

LAST_NAMES = [
    'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
    'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson',
    'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Thompson', 'White',
    'Harris', 'Clark', 'Lewis', 'Robinson', 'Walker', 'Young', 'Hall',
]


def generate_name():
    """Generate a random name"""
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def create_squad_for_player(player, squad_name=None, callsign=None):
    """
    Create a full 9-person Ranger squad for a player

    Args:
        player: Player object
        squad_name: Optional custom squad name
        callsign: Optional radio callsign
    """
    # Check if player already has a squad
    if hasattr(player, 'squad'):
        print(f"Player {player.character_name} already has a squad!")
        return player.squad

    # Create squad
    if not squad_name:
        squad_name = f"Ranger Squad {random.choice(['Alpha', 'Bravo', 'Charlie', 'Delta'])}"
    if not callsign:
        callsigns = ['Havoc', 'Reaper', 'Viper', 'Phantom', 'Nomad', 'Hunter', 'Raven']
        callsign = random.choice(callsigns)

    squad = Squad.objects.create(
        player=player,
        squad_name=squad_name,
        callsign=callsign,
    )
    print(f"Created squad: {squad.squad_name} (Callsign: {squad.callsign})")

    # Squad Leader (HQ) - Player's primary character
    squad_leader_name = player.character_name  # Use player's character name
    leader = SquadMember.objects.create(
        squad=squad,
        name=f"SSG {squad_leader_name}",
        rank='staff_sergeant',
        fire_team='hq',
        role='squad_leader',
        primary_weapon='m4a1',
        secondary_duty='',  # Squad Leader usually doesn't have secondary duty
        # Slightly better stats for the leader
        strength=12,
        dexterity=12,
        constitution=12,
        intelligence=14,
        marksmanship=60,
        tactics=60,
    )
    print(f"  Created: {leader.name} - Squad Leader (HQ)")

    # Alpha Team
    alpha_members = [
        {
            'name': f"SGT {generate_name()}",
            'rank': 'sergeant',
            'role': 'team_leader',
            'weapon': 'm4a1',
            'secondary': '',
            'fire_team': 'alpha',
        },
        {
            'name': f"SPC {generate_name()}",
            'rank': 'specialist',
            'role': 'automatic_rifleman',
            'weapon': 'm249',
            'secondary': '',
            'fire_team': 'alpha',
        },
        {
            'name': f"SPC {generate_name()}",
            'rank': 'specialist',
            'role': 'grenadier',
            'weapon': 'm4a1_m320',
            'secondary': '',
            'fire_team': 'alpha',
        },
        {
            'name': f"PFC {generate_name()}",
            'rank': 'private_first_class',
            'role': 'rifleman',
            'weapon': 'm4a1',
            'secondary': 'medic',  # Alpha Team medic
            'fire_team': 'alpha',
        },
    ]

    # Bravo Team
    bravo_members = [
        {
            'name': f"SGT {generate_name()}",
            'rank': 'sergeant',
            'role': 'team_leader',
            'weapon': 'm4a1',
            'secondary': 'talker',  # Bravo Team Leader is the Talker
            'fire_team': 'bravo',
        },
        {
            'name': f"SPC {generate_name()}",
            'rank': 'specialist',
            'role': 'automatic_rifleman',
            'weapon': 'm249',
            'secondary': '',
            'fire_team': 'bravo',
        },
        {
            'name': f"SPC {generate_name()}",
            'rank': 'specialist',
            'role': 'grenadier',
            'weapon': 'm4a1_m320',
            'secondary': 'engineer',  # Grenadier doubles as Engineer
            'fire_team': 'bravo',
        },
        {
            'name': f"PFC {generate_name()}",
            'rank': 'private_first_class',
            'role': 'rifleman',
            'weapon': 'm4a1',
            'secondary': 'medic',  # Bravo Team medic
            'fire_team': 'bravo',
        },
    ]

    # Create all squad members
    for member_data in alpha_members + bravo_members:
        # Randomize stats a bit
        strength = random.randint(8, 12)
        dexterity = random.randint(8, 12)
        constitution = random.randint(8, 12)
        intelligence = random.randint(8, 12)

        # Skill levels based on role
        marksmanship = random.randint(45, 55)
        melee = random.randint(25, 35)
        explosives = random.randint(15, 25)
        medical = random.randint(5, 15)
        engineering = random.randint(5, 15)
        tactics = random.randint(25, 35)

        # Boost skills based on secondary duty
        if member_data['secondary'] == 'medic':
            medical = random.randint(50, 60)
        elif member_data['secondary'] == 'engineer':
            engineering = random.randint(50, 60)
            explosives = random.randint(40, 50)
        elif member_data['secondary'] == 'talker':
            intelligence = random.randint(12, 15)
            tactics = random.randint(40, 50)

        # Boost skills for automatic rifleman
        if member_data['role'] == 'automatic_rifleman':
            strength = random.randint(10, 14)  # Need strength for LMG

        # Boost skills for team leaders
        if member_data['role'] == 'team_leader':
            intelligence = random.randint(11, 14)
            tactics = random.randint(45, 55)

        member = SquadMember.objects.create(
            squad=squad,
            name=member_data['name'],
            rank=member_data['rank'],
            fire_team=member_data['fire_team'],
            role=member_data['role'],
            primary_weapon=member_data['weapon'],
            secondary_duty=member_data['secondary'],
            strength=strength,
            dexterity=dexterity,
            constitution=constitution,
            intelligence=intelligence,
            marksmanship=marksmanship,
            melee_combat=melee,
            explosives=explosives,
            medical=medical,
            engineering=engineering,
            tactics=tactics,
        )

        team_label = member_data['fire_team'].capitalize()
        secondary_label = f" ({member.get_secondary_duty_display()})" if member.secondary_duty else ""
        print(f"  Created: {member.name} - {member.get_role_display()} ({team_label}){secondary_label}")

    print(f"\n{squad.squad_name} is ready for deployment!")
    print(f"Total members: {squad.members.count()}")
    print(f"  Squad HQ: {squad.members.filter(fire_team='hq').count()}")
    print(f"  Alpha Team: {squad.members.filter(fire_team='alpha').count()}")
    print(f"  Bravo Team: {squad.members.filter(fire_team='bravo').count()}")

    return squad


if __name__ == '__main__':
    # Create squads for all players without one
    players = Player.objects.all()

    if not players.exists():
        print("No players found! Create a player first.")
    else:
        for player in players:
            if not hasattr(player, 'squad'):
                print(f"\nCreating squad for player: {player.character_name}")
                create_squad_for_player(player)
            else:
                print(f"\nPlayer {player.character_name} already has squad: {player.squad.squad_name}")

    print("\n✓ Squad creation complete!")
