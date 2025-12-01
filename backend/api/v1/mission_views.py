"""
Mission API Views

Provides REST API endpoints for mission management
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone

from game.models import Mission, PlayerMission, Player, NPC


class MissionListView(APIView):
    """
    GET /api/v1/missions/
    List all available missions for the player
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        player = get_object_or_404(Player, user=request.user)

        # Get all active missions
        all_missions = Mission.objects.filter(is_active=True)

        # Categorize missions
        available = []
        active = []
        completed = []

        for mission in all_missions:
            # Check player's relationship with this mission
            player_mission = PlayerMission.objects.filter(
                player=player,
                mission=mission
            ).first()

            mission_data = {
                'id': str(mission.id),
                'key': mission.key,
                'name': mission.name,
                'type': mission.mission_type,
                'difficulty': mission.difficulty,
                'required_level': mission.required_level,
                'is_public': mission.is_public,
                'hook_title': mission.hook_title,
                'given_by': mission.given_by_npc.name if mission.given_by_npc else None,
                'time_limit': mission.time_limit,
                'is_repeatable': mission.is_repeatable,
            }

            if player_mission:
                if player_mission.status in ['active', 'in_progress']:
                    mission_data['player_mission_id'] = str(player_mission.id)
                    mission_data['status'] = player_mission.status
                    mission_data['progress'] = player_mission.get_progress_summary()
                    active.append(mission_data)
                elif player_mission.status == 'completed':
                    mission_data['completed_at'] = player_mission.completed_at
                    mission_data['success_level'] = player_mission.success_level
                    completed.append(mission_data)
                else:
                    # Check if available
                    can_start, message = mission.can_player_start(player)
                    if can_start:
                        mission_data['can_start'] = True
                        available.append(mission_data)
                    else:
                        mission_data['can_start'] = False
                        mission_data['requirement_message'] = message
            else:
                # New mission - check if available
                can_start, message = mission.can_player_start(player)
                mission_data['can_start'] = can_start
                mission_data['requirement_message'] = message if not can_start else None
                if can_start:
                    available.append(mission_data)

        return Response({
            'available': available,
            'active': active,
            'completed': completed,
        })


class MissionDetailView(APIView):
    """
    GET /api/v1/missions/<key>/
    Get detailed information about a specific mission
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, mission_key):
        player = get_object_or_404(Player, user=request.user)
        mission = get_object_or_404(Mission, key=mission_key, is_active=True)

        # Get player's instance of this mission if it exists
        player_mission = PlayerMission.objects.filter(
            player=player,
            mission=mission
        ).first()

        # Check if player can start
        can_start, requirement_message = mission.can_player_start(player)

        mission_data = {
            'id': str(mission.id),
            'key': mission.key,
            'name': mission.name,
            'type': mission.mission_type,
            'difficulty': mission.difficulty,
            'required_level': mission.required_level,
            'required_squad_size': mission.required_squad_size,
            'is_public': mission.is_public,
            'can_start': can_start,
            'requirement_message': requirement_message if not can_start else None,

            # Narrative structure
            'hook_title': mission.hook_title,
            'hook_description': mission.hook_description,

            # Only show acts if mission is active
            'acts': None,

            # Mission parameters
            'time_limit': mission.time_limit,
            'can_fail': mission.can_fail,
            'can_abandon': mission.can_abandon,
            'is_repeatable': mission.is_repeatable,

            # Rewards (if public)
            'rewards': None,

            # Given by
            'given_by': {
                'name': mission.given_by_npc.name,
                'key': mission.given_by_npc.key,
            } if mission.given_by_npc else None,

            # Player progress
            'player_progress': None,
        }

        # If mission is public, show rewards
        if mission.is_public:
            mission_data['rewards'] = {
                'xp': mission.reward_xp,
                'currency': mission.reward_currency,
                'items': mission.reward_items,
                'reputation': mission.reward_reputation,
            }

        # If player has this mission active, show progress and current act
        if player_mission and player_mission.status in ['active', 'in_progress']:
            mission_data['player_progress'] = player_mission.get_progress_summary()

            # Show current act structure
            current_act = player_mission.current_act
            acts = []

            if current_act >= 1:
                acts.append({
                    'act': 1,
                    'title': mission.act1_title,
                    'description': mission.act1_description,
                    'objectives': self._get_objectives_with_status(
                        mission.act1_objectives,
                        player_mission.objectives_completed
                    ),
                })

            if current_act >= 2:
                acts.append({
                    'act': 2,
                    'title': mission.act2_title,
                    'description': mission.act2_description,
                    'objectives': self._get_objectives_with_status(
                        mission.act2_objectives,
                        player_mission.objectives_completed
                    ),
                })

            if current_act >= 3:
                acts.append({
                    'act': 3,
                    'title': mission.act3_title,
                    'description': mission.act3_description,
                    'objectives': self._get_objectives_with_status(
                        mission.act3_objectives,
                        player_mission.objectives_completed
                    ),
                })

            mission_data['acts'] = acts

        # If completed, show conclusion
        if player_mission and player_mission.status == 'completed':
            if player_mission.success_level == 'full':
                mission_data['conclusion'] = mission.conclusion_success
            elif player_mission.success_level == 'partial':
                mission_data['conclusion'] = mission.conclusion_partial
            else:
                mission_data['conclusion'] = mission.conclusion_failure

            mission_data['player_progress'] = player_mission.get_progress_summary()

        return Response(mission_data)

    def _get_objectives_with_status(self, objectives, completed_dict):
        """Add completion status to objectives"""
        return [
            {
                **obj,
                'completed': completed_dict.get(obj['key'], False)
            }
            for obj in objectives
        ]


class MissionAcceptView(APIView):
    """
    POST /api/v1/missions/<key>/accept/
    Accept a mission
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, mission_key):
        player = get_object_or_404(Player, user=request.user)
        mission = get_object_or_404(Mission, key=mission_key, is_active=True)

        # Check if player already has this mission
        existing = PlayerMission.objects.filter(
            player=player,
            mission=mission,
            status__in=['active', 'in_progress']
        ).first()

        if existing:
            return Response(
                {'error': 'Mission already in progress'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if player can start
        can_start, message = mission.can_player_start(player)
        if not can_start:
            return Response(
                {'error': message},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create player mission instance
        player_mission = PlayerMission.objects.create(
            player=player,
            mission=mission,
            status='available'
        )

        # Accept the mission
        success, message = player_mission.accept()

        if success:
            return Response({
                'message': message,
                'player_mission_id': str(player_mission.id),
                'hook': {
                    'title': mission.hook_title,
                    'description': mission.hook_description,
                },
                'act1': {
                    'title': mission.act1_title,
                    'description': mission.act1_description,
                    'objectives': mission.act1_objectives,
                }
            })
        else:
            player_mission.delete()
            return Response(
                {'error': message},
                status=status.HTTP_400_BAD_REQUEST
            )


class MissionObjectiveCompleteView(APIView):
    """
    POST /api/v1/player-missions/<id>/objectives/<objective_key>/complete/
    Complete a mission objective
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, player_mission_id, objective_key):
        player = get_object_or_404(Player, user=request.user)
        player_mission = get_object_or_404(
            PlayerMission,
            id=player_mission_id,
            player=player
        )

        # Check time limit
        player_mission.check_time_limit()

        if player_mission.status not in ['active', 'in_progress']:
            return Response(
                {'error': 'Mission is not active'},
                status=status.HTTP_400_BAD_REQUEST
            )

        success, message = player_mission.complete_objective(objective_key)

        if success:
            response_data = {
                'message': message,
                'progress': player_mission.get_progress_summary(),
            }

            # If mission completed, include conclusion
            if player_mission.status == 'completed':
                mission = player_mission.mission
                if player_mission.success_level == 'full':
                    response_data['conclusion'] = mission.conclusion_success
                elif player_mission.success_level == 'partial':
                    response_data['conclusion'] = mission.conclusion_partial

                # Include rewards if public mission
                if mission.is_public:
                    response_data['rewards'] = {
                        'xp': player_mission.xp_awarded,
                        'currency': player_mission.currency_awarded,
                        'items': player_mission.items_awarded,
                    }

            return Response(response_data)
        else:
            return Response(
                {'error': message},
                status=status.HTTP_400_BAD_REQUEST
            )


class MissionAbandonView(APIView):
    """
    POST /api/v1/player-missions/<id>/abandon/
    Abandon a mission
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, player_mission_id):
        player = get_object_or_404(Player, user=request.user)
        player_mission = get_object_or_404(
            PlayerMission,
            id=player_mission_id,
            player=player
        )

        success, message = player_mission.abandon_mission()

        if success:
            return Response({'message': message})
        else:
            return Response(
                {'error': message},
                status=status.HTTP_400_BAD_REQUEST
            )


class MissionEventTriggerView(APIView):
    """
    POST /api/v1/player-missions/<id>/events/<event_key>/trigger/
    Trigger a mission event
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, player_mission_id, event_key):
        player = get_object_or_404(Player, user=request.user)
        player_mission = get_object_or_404(
            PlayerMission,
            id=player_mission_id,
            player=player
        )

        # Get the event
        from game.models import MissionEvent
        event = get_object_or_404(
            MissionEvent,
            mission=player_mission.mission,
            key=event_key
        )

        # Check if already triggered
        if not event.is_repeatable and event_key in player_mission.events_triggered:
            return Response(
                {'error': 'Event already triggered'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Trigger the event
        success, message = player_mission.trigger_event(event_key)

        if success:
            return Response({
                'message': message,
                'event': {
                    'name': event.name,
                    'type': event.event_type,
                    'description': event.description,
                    'choices': event.choices if event.event_type == 'choice' else None,
                }
            })
        else:
            return Response(
                {'error': message},
                status=status.HTTP_400_BAD_REQUEST
            )


class MissionChoiceView(APIView):
    """
    POST /api/v1/player-missions/<id>/events/<event_key>/choice/
    Make a choice in a mission event
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, player_mission_id, event_key):
        player = get_object_or_404(Player, user=request.user)
        player_mission = get_object_or_404(
            PlayerMission,
            id=player_mission_id,
            player=player
        )

        # Get choice from request
        choice_text = request.data.get('choice')
        if not choice_text:
            return Response(
                {'error': 'Choice not provided'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get the event
        from game.models import MissionEvent
        event = get_object_or_404(
            MissionEvent,
            mission=player_mission.mission,
            key=event_key
        )

        # Find the choice and its outcome
        choice_data = None
        for choice in event.choices:
            if choice['text'] == choice_text:
                choice_data = choice
                break

        if not choice_data:
            return Response(
                {'error': 'Invalid choice'},
                status=status.HTTP_400_BAD_REQUEST
            )

        outcome_key = choice_data.get('outcome')
        outcome = event.outcomes.get(outcome_key, {})

        # Record the choice
        player_mission.make_choice(event_key, choice_text, outcome_key)

        return Response({
            'message': 'Choice recorded',
            'outcome': {
                'description': outcome.get('description', ''),
                'effects': outcome.get('effects', {}),
            }
        })


class MissionCreatePrivateView(APIView):
    """
    POST /api/v1/missions/create-private/
    Create a private mission for the player
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        player = get_object_or_404(Player, user=request.user)

        # Extract mission data from request
        data = request.data

        try:
            # Create the mission
            mission = Mission.objects.create(
                key=f"private_{player.id}_{timezone.now().timestamp()}",
                name=data.get('name'),
                mission_type=data.get('mission_type', 'custom'),
                is_public=False,  # Private mission
                difficulty=data.get('difficulty', 'moderate'),
                required_level=player.level,  # Set to player's current level

                # Hook
                hook_title=data.get('hook_title'),
                hook_description=data.get('hook_description'),

                # Act 1
                act1_title=data.get('act1_title', 'Setup'),
                act1_description=data.get('act1_description'),
                act1_objectives=data.get('act1_objectives', []),

                # Act 2
                act2_title=data.get('act2_title', 'Confrontation'),
                act2_description=data.get('act2_description'),
                act2_objectives=data.get('act2_objectives', []),

                # Act 3
                act3_title=data.get('act3_title', 'Climax'),
                act3_description=data.get('act3_description'),
                act3_objectives=data.get('act3_objectives', []),

                # Conclusion
                conclusion_success=data.get('conclusion_success'),
                conclusion_failure=data.get('conclusion_failure', ''),
                conclusion_partial=data.get('conclusion_partial', ''),

                # No rewards for private missions
                reward_xp=0,
                reward_currency=0,
                reward_items=[],

                # Parameters
                time_limit=data.get('time_limit'),
                can_fail=data.get('can_fail', True),
                can_abandon=data.get('can_abandon', True),
                is_repeatable=False,
            )

            return Response({
                'message': 'Private mission created',
                'mission': {
                    'id': str(mission.id),
                    'key': mission.key,
                    'name': mission.name,
                }
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
