"""
API Serializers

Converts model instances to JSON and vice versa.
"""
from rest_framework import serializers
from game.models import Player, Room, Exit, Item, NPC, Quest, Zone


class PlayerSerializer(serializers.ModelSerializer):
    """Serializer for Player model"""
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Player
        fields = [
            'id', 'username', 'character_name', 'description',
            'level', 'experience', 'health', 'max_health',
            'mana', 'max_mana', 'position', 'is_online',
            'created_at', 'last_login'
        ]
        read_only_fields = fields


class ExitSerializer(serializers.ModelSerializer):
    """Serializer for Exit model"""
    destination_name = serializers.CharField(source='destination.name', read_only=True)

    class Meta:
        model = Exit
        fields = [
            'direction', 'destination', 'destination_name',
            'is_locked', 'is_hidden', 'custom_name'
        ]


class RoomSerializer(serializers.ModelSerializer):
    """Serializer for Room model"""
    zone_name = serializers.CharField(source='zone.name', read_only=True)
    exits = ExitSerializer(many=True, source='exits_out', read_only=True)
    player_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Room
        fields = [
            'id', 'key', 'name', 'description', 'zone', 'zone_name',
            'is_dark', 'is_safe', 'is_private', 'exits', 'player_count'
        ]


class ItemSerializer(serializers.ModelSerializer):
    """Serializer for Item model"""

    class Meta:
        model = Item
        fields = [
            'id', 'key', 'name', 'description', 'item_type',
            'weight', 'value', 'is_equipped', 'equipment_slot',
            'stat_modifiers', 'uses_remaining', 'effect'
        ]


class NPCSerializer(serializers.ModelSerializer):
    """Serializer for NPC model"""
    location_name = serializers.CharField(source='location.name', read_only=True)

    class Meta:
        model = NPC
        fields = [
            'id', 'key', 'name', 'description', 'ai_type',
            'level', 'health', 'max_health', 'location', 'location_name',
            'is_alive', 'sells_items', 'buys_items', 'greeting_message'
        ]


class QuestSerializer(serializers.ModelSerializer):
    """Serializer for Quest model"""
    quest_giver_name = serializers.CharField(source='quest_giver.name', read_only=True)

    class Meta:
        model = Quest
        fields = [
            'id', 'key', 'title', 'description', 'quest_giver',
            'quest_giver_name', 'required_level', 'objectives',
            'experience_reward', 'currency_reward', 'is_repeatable'
        ]


class ZoneSerializer(serializers.ModelSerializer):
    """Serializer for Zone model"""
    room_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Zone
        fields = [
            'id', 'key', 'name', 'description', 'level_min', 'level_max',
            'climate', 'is_safe', 'is_pvp', 'room_count'
        ]
