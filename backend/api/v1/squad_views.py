"""
Squad Management API Views

Endpoints for managing and customizing squads.
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from game.models import Squad, SquadMember
from .serializers import SquadSerializer, SquadMemberSerializer


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
