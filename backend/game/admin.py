"""
Django Admin Configuration for Game Models
"""
from django.contrib import admin
from .models import Player, Room, Exit, Zone, Item, NPC, Quest, PlayerQuest


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['character_name', 'user', 'level', 'health', 'location', 'is_online']
    list_filter = ['is_online', 'level', 'position']
    search_fields = ['character_name', 'user__username']
    readonly_fields = ['created_at', 'last_login', 'total_playtime']
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'character_name', 'description')
        }),
        ('Location', {
            'fields': ('location', 'home')
        }),
        ('Stats', {
            'fields': ('level', 'experience', 'health', 'max_health', 'mana', 'max_mana')
        }),
        ('Attributes', {
            'fields': ('strength', 'dexterity', 'intelligence', 'constitution')
        }),
        ('State', {
            'fields': ('position', 'is_online')
        }),
        ('Inventory', {
            'fields': ('inventory_size', 'currency')
        }),
        ('Metadata', {
            'fields': ('created_at', 'last_login', 'total_playtime', 'attributes')
        }),
    )


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ['name', 'key', 'level_min', 'level_max', 'room_count', 'is_safe']
    list_filter = ['is_safe', 'is_pvp', 'climate']
    search_fields = ['name', 'key', 'description']
    readonly_fields = ['created_at', 'updated_at', 'room_count']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'key', 'zone', 'player_count', 'is_safe', 'is_dark']
    list_filter = ['zone', 'is_safe', 'is_dark', 'is_private']
    search_fields = ['name', 'key', 'description']
    readonly_fields = ['created_at', 'updated_at', 'player_count']
    fieldsets = (
        ('Basic Info', {
            'fields': ('key', 'name', 'description', 'zone')
        }),
        ('Properties', {
            'fields': ('is_dark', 'is_safe', 'is_private', 'is_indoors', 'max_capacity')
        }),
        ('Position', {
            'fields': ('coordinates',)
        }),
        ('State', {
            'fields': ('state',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Exit)
class ExitAdmin(admin.ModelAdmin):
    list_display = ['source', 'direction', 'destination', 'is_locked', 'is_hidden']
    list_filter = ['direction', 'is_locked', 'is_hidden', 'is_one_way']
    search_fields = ['source__name', 'destination__name']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'item_type', 'weight', 'value', 'owner_player', 'room']
    list_filter = ['item_type', 'is_takeable', 'is_unique', 'equipment_slot']
    search_fields = ['name', 'key', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(NPC)
class NPCAdmin(admin.ModelAdmin):
    list_display = ['name', 'ai_type', 'level', 'location', 'is_alive', 'is_merchant']
    list_filter = ['ai_type', 'is_alive', 'sells_items', 'buys_items']
    search_fields = ['name', 'key', 'description']
    readonly_fields = ['created_at', 'updated_at', 'is_merchant']
    fieldsets = (
        ('Basic Info', {
            'fields': ('key', 'name', 'description')
        }),
        ('Location', {
            'fields': ('location', 'home_location')
        }),
        ('AI', {
            'fields': ('ai_type', 'dialogue_tree', 'greeting_message')
        }),
        ('Movement', {
            'fields': ('patrol_route', 'wanders')
        }),
        ('Combat', {
            'fields': ('level', 'health', 'max_health', 'damage', 'defense')
        }),
        ('Loot', {
            'fields': ('loot_table', 'currency_drop', 'experience_reward')
        }),
        ('Merchant', {
            'fields': ('sells_items', 'buys_items', 'price_modifier')
        }),
        ('Respawn', {
            'fields': ('respawn_time', 'is_alive', 'death_time')
        }),
        ('Flags', {
            'fields': ('is_unique', 'is_attackable', 'attributes')
        }),
    )


@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    list_display = ['title', 'key', 'required_level', 'quest_giver', 'is_repeatable']
    list_filter = ['required_level', 'is_repeatable']
    search_fields = ['title', 'key', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(PlayerQuest)
class PlayerQuestAdmin(admin.ModelAdmin):
    list_display = ['player', 'quest', 'status', 'accepted_at', 'completed_at']
    list_filter = ['status']
    search_fields = ['player__character_name', 'quest__title']
    readonly_fields = ['accepted_at', 'completed_at', 'is_complete']
