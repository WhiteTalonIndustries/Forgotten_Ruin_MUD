"""
API v1 Views

REST API endpoints for game data.
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from game.models import Player, Room, Item, NPC, Quest, Zone
from .serializers import (
    PlayerSerializer, RoomSerializer, ItemSerializer,
    NPCSerializer, QuestSerializer, ZoneSerializer
)


class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for player data

    list: Get all online players
    retrieve: Get specific player details
    """
    serializer_class = PlayerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return only online players"""
        return Player.objects.filter(is_online=True)

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current player's data"""
        try:
            player = request.user.player
            serializer = self.get_serializer(player)
            return Response(serializer.data)
        except Player.DoesNotExist:
            return Response(
                {'error': 'Player not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'])
    def inventory(self, request):
        """Get current player's inventory"""
        try:
            player = request.user.player
            items = player.items.all()
            serializer = ItemSerializer(items, many=True)
            return Response(serializer.data)
        except Player.DoesNotExist:
            return Response(
                {'error': 'Player not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class RoomViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for room data

    list: Get all rooms (paginated)
    retrieve: Get specific room details
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def players(self, request, pk=None):
        """Get players in a specific room"""
        room = self.get_object()
        players = room.get_players()
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)


class ItemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for item data
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]


class NPCViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for NPC data
    """
    queryset = NPC.objects.filter(is_alive=True)
    serializer_class = NPCSerializer
    permission_classes = [permissions.IsAuthenticated]


class QuestViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for quest data
    """
    queryset = Quest.objects.all()
    serializer_class = QuestSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get quests available to current player"""
        try:
            player = request.user.player
            # Filter quests by level requirement
            available_quests = Quest.objects.filter(
                required_level__lte=player.level
            )
            serializer = self.get_serializer(available_quests, many=True)
            return Response(serializer.data)
        except Player.DoesNotExist:
            return Response(
                {'error': 'Player not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class PlayerStatsView(APIView):
    """Get current player statistics"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            player = request.user.player
            stats = {
                'character_name': player.character_name,
                'level': player.level,
                'experience': player.experience,
                'health': player.health,
                'max_health': player.max_health,
                'mana': player.mana,
                'max_mana': player.max_mana,
                'strength': player.strength,
                'dexterity': player.dexterity,
                'intelligence': player.intelligence,
                'constitution': player.constitution,
                'currency': player.currency,
                'inventory_count': player.inventory_count,
                'inventory_size': player.inventory_size,
            }
            return Response(stats)
        except Player.DoesNotExist:
            return Response(
                {'error': 'Player not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class ZoneListView(APIView):
    """Get all zones"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        zones = Zone.objects.all()
        serializer = ZoneSerializer(zones, many=True)
        return Response(serializer.data)
