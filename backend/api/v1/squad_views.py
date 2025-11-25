"""
Squad Management API Views

Endpoints for managing and customizing squads.
"""
import random
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from game.models import Squad, SquadMember
from .serializers import SquadSerializer, SquadMemberSerializer


# Sample names for squad member generation
FIRST_NAMES = [
    'James', 'Michael', 'Robert', 'John', 'David', 'William', 'Richard', 'Joseph',
    'Thomas', 'Christopher', 'Daniel', 'Matthew', 'Anthony', 'Mark', 'Donald', 'Steven',
    'Andrew', 'Joshua', 'Kenneth', 'Kevin', 'Brian', 'Timothy', 'Ronald', 'Jason',
    'Paul', 'Ryan', 'Eric', 'Jacob', 'Gary', 'Nicholas', 'Jonathan', 'Larry'
]

LAST_NAMES = [
    'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
    'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson',
    'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Thompson', 'White',
    'Harris', 'Clark', 'Lewis', 'Robinson', 'Walker', 'Young', 'Hall', 'Allen'
]

CALLSIGNS = [
    'Havoc', 'Reaper', 'Viper', 'Phantom', 'Nomad', 'Hunter', 'Raven',
    'Ghost', 'Shadow', 'Thunder', 'Talon', 'Wolf', 'Eagle', 'Cobra'
]


class SquadCustomizationView(APIView):
    """
    API endpoint for customizing player's squad
    """
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        """
        Update squad name and callsign

        Request body:
        {
            "squad_name": "New Squad Name",
            "callsign": "NewCallsign"
        }
        """
        try:
            player = request.user.player
            squad = player.squad
        except:
            return Response(
                {'error': 'Player or squad not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Update squad name if provided
        if 'squad_name' in request.data:
            squad_name = request.data['squad_name'].strip()
            if len(squad_name) > 0 and len(squad_name) <= 100:
                squad.squad_name = squad_name
            else:
                return Response(
                    {'error': 'Squad name must be 1-100 characters'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Update callsign if provided
        if 'callsign' in request.data:
            callsign = request.data['callsign'].strip()
            if len(callsign) > 0 and len(callsign) <= 50:
                squad.callsign = callsign
            else:
                return Response(
                    {'error': 'Callsign must be 1-50 characters'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        squad.save()
        serializer = SquadSerializer(squad)
        return Response(serializer.data)


class SquadMemberCustomizationView(APIView):
    """
    API endpoint for customizing individual squad members
    """
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, member_id):
        """
        Update squad member details

        Request body:
        {
            "name": "New Name",
            "secondary_duty": "medic|engineer|talker|"
        }
        """
        try:
            player = request.user.player
            squad = player.squad
            member = squad.members.get(id=member_id)
        except:
            return Response(
                {'error': 'Squad member not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Update name if provided
        if 'name' in request.data:
            name = request.data['name'].strip()
            if len(name) > 0 and len(name) <= 100:
                member.name = name
            else:
                return Response(
                    {'error': 'Name must be 1-100 characters'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Update secondary duty if provided
        if 'secondary_duty' in request.data:
            duty = request.data['secondary_duty'].strip()

            # Validate secondary duty
            valid_duties = ['', 'medic', 'engineer', 'talker']
            if duty not in valid_duties:
                return Response(
                    {'error': f'Invalid secondary duty. Must be one of: {", ".join(valid_duties)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check if duty is already assigned in this fire team
            if duty and duty != '':
                existing = squad.members.filter(
                    fire_team=member.fire_team,
                    secondary_duty=duty
                ).exclude(id=member.id)

                if existing.exists():
                    return Response(
                        {'error': f'Another member in {member.get_fire_team_display()} already has {duty} duty'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            member.secondary_duty = duty

        member.save()
        serializer = SquadMemberSerializer(member)
        return Response(serializer.data)


class SquadMemberSwapView(APIView):
    """
    API endpoint for swapping squad members between fire teams
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Swap two squad members between fire teams

        Request body:
        {
            "member1_id": 1,
            "member2_id": 2
        }
        """
        try:
            player = request.user.player
            squad = player.squad

            member1_id = request.data.get('member1_id')
            member2_id = request.data.get('member2_id')

            if not member1_id or not member2_id:
                return Response(
                    {'error': 'Both member1_id and member2_id are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            member1 = squad.members.get(id=member1_id)
            member2 = squad.members.get(id=member2_id)

        except SquadMember.DoesNotExist:
            return Response(
                {'error': 'One or both squad members not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except:
            return Response(
                {'error': 'Squad not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Can't swap Squad Leader
        if member1.role == 'squad_leader' or member2.role == 'squad_leader':
            return Response(
                {'error': 'Cannot swap the Squad Leader'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Can't swap members in the same fire team
        if member1.fire_team == member2.fire_team:
            return Response(
                {'error': 'Cannot swap members in the same fire team'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Must have same role to swap
        if member1.role != member2.role:
            return Response(
                {'error': 'Can only swap members with the same role'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Swap fire teams
        member1_team = member1.fire_team
        member1.fire_team = member2.fire_team
        member2.fire_team = member1_team

        member1.save()
        member2.save()

        # Return updated squad
        serializer = SquadSerializer(squad)
        return Response(serializer.data)


class SquadGenerationView(APIView):
    """
    API endpoint for generating a new squad for the player
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Generate a new 9-person Ranger squad for the player

        This will DELETE the existing squad and create a brand new one.

        Request body (all optional):
        {
            "squad_name": "Custom Squad Name",
            "callsign": "CustomCallsign"
        }
        """
        try:
            player = request.user.player
        except:
            return Response(
                {'error': 'Player not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Delete existing squad if it exists
        if hasattr(player, 'squad') and player.squad:
            old_squad_name = player.squad.squad_name
            player.squad.delete()
            print(f"Deleted old squad: {old_squad_name}")

        # Get custom names or use defaults
        squad_name = request.data.get('squad_name', '').strip()
        if not squad_name:
            squad_name = f"Ranger Squad {random.choice(['Alpha', 'Bravo', 'Charlie', 'Delta', 'Echo'])}"

        callsign = request.data.get('callsign', '').strip()
        if not callsign:
            callsign = random.choice(CALLSIGNS)

        # Create new squad
        squad = Squad.objects.create(
            player=player,
            squad_name=squad_name,
            callsign=callsign,
        )

        # Generate squad leader (uses player's character name)
        squad_leader_name = player.character_name
        SquadMember.objects.create(
            squad=squad,
            name=f"SSG {squad_leader_name}",
            rank='staff_sergeant',
            fire_team='hq',
            role='squad_leader',
            primary_weapon='m4a1',
            secondary_duty='',
            strength=random.randint(11, 13),
            dexterity=random.randint(11, 13),
            constitution=random.randint(11, 13),
            intelligence=random.randint(13, 15),
            marksmanship=random.randint(55, 65),
            melee_combat=random.randint(30, 40),
            explosives=random.randint(20, 30),
            medical=random.randint(10, 20),
            engineering=random.randint(10, 20),
            tactics=random.randint(55, 65),
        )

        # Define squad composition based on Forgotten Ruin lore
        squad_composition = [
            # Alpha Team
            {
                'rank': 'sergeant',
                'role': 'team_leader',
                'weapon': 'm4a1',
                'secondary': '',
                'fire_team': 'alpha',
            },
            {
                'rank': 'specialist',
                'role': 'automatic_rifleman',
                'weapon': 'm249',
                'secondary': '',
                'fire_team': 'alpha',
            },
            {
                'rank': 'specialist',
                'role': 'grenadier',
                'weapon': 'm4a1_m320',
                'secondary': '',
                'fire_team': 'alpha',
            },
            {
                'rank': 'private_first_class',
                'role': 'rifleman',
                'weapon': 'm4a1',
                'secondary': 'medic',
                'fire_team': 'alpha',
            },
            # Bravo Team
            {
                'rank': 'sergeant',
                'role': 'team_leader',
                'weapon': 'm4a1',
                'secondary': 'talker',
                'fire_team': 'bravo',
            },
            {
                'rank': 'specialist',
                'role': 'automatic_rifleman',
                'weapon': 'm249',
                'secondary': '',
                'fire_team': 'bravo',
            },
            {
                'rank': 'specialist',
                'role': 'grenadier',
                'weapon': 'm4a1_m320',
                'secondary': 'engineer',
                'fire_team': 'bravo',
            },
            {
                'rank': 'private_first_class',
                'role': 'rifleman',
                'weapon': 'm4a1',
                'secondary': 'medic',
                'fire_team': 'bravo',
            },
        ]

        # Generate all squad members
        for member_data in squad_composition:
            # Generate random name
            first_name = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)

            # Add rank prefix
            rank_prefix = {
                'sergeant': 'SGT',
                'specialist': 'SPC',
                'private_first_class': 'PFC',
            }[member_data['rank']]

            name = f"{rank_prefix} {first_name} {last_name}"

            # Generate base attributes (1-20 range)
            strength = random.randint(8, 12)
            dexterity = random.randint(8, 12)
            constitution = random.randint(8, 12)
            intelligence = random.randint(8, 12)

            # Generate base skills (0-100 range)
            marksmanship = random.randint(45, 55)
            melee = random.randint(25, 35)
            explosives = random.randint(15, 25)
            medical = random.randint(5, 15)
            engineering = random.randint(5, 15)
            tactics = random.randint(25, 35)

            # Role-based bonuses
            if member_data['role'] == 'automatic_rifleman':
                strength = random.randint(10, 14)  # Need strength for LMG
                constitution = random.randint(10, 13)  # Endurance to carry ammo

            if member_data['role'] == 'team_leader':
                intelligence = random.randint(11, 14)
                tactics = random.randint(45, 55)
                marksmanship = random.randint(50, 60)

            # Secondary duty bonuses
            if member_data['secondary'] == 'medic':
                medical = random.randint(50, 65)
                intelligence = random.randint(10, 13)
            elif member_data['secondary'] == 'engineer':
                engineering = random.randint(50, 65)
                explosives = random.randint(40, 55)
                intelligence = random.randint(10, 13)
            elif member_data['secondary'] == 'talker':
                intelligence = random.randint(12, 15)
                tactics = random.randint(40, 55)

            # Create the squad member
            SquadMember.objects.create(
                squad=squad,
                name=name,
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

        # Return the newly created squad
        serializer = SquadSerializer(squad)
        return Response({
            'message': f'{squad.squad_name} generated successfully!',
            'squad': serializer.data
        }, status=status.HTTP_201_CREATED)
