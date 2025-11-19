"""
Room and Exit Models

Represents locations in the game world and connections between them.
"""
from django.db import models
from django.core.validators import MinValueValidator


class Room(models.Model):
    """
    A location in the game world

    Rooms are discrete locations where players, NPCs, and items can exist.
    """
    # Identification
    key = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="Unique room identifier (e.g., 'town_square')"
    )

    name = models.CharField(
        max_length=200,
        help_text="Display name of the room"
    )

    description = models.TextField(
        help_text="Detailed description of the room"
    )

    # Zone/Area
    zone = models.ForeignKey(
        'Zone',
        on_delete=models.CASCADE,
        related_name='rooms',
        help_text="Zone this room belongs to"
    )

    # Optional coordinates for mapping
    coordinates = models.JSONField(
        null=True,
        blank=True,
        help_text="3D coordinates {'x': 0, 'y': 0, 'z': 0}"
    )

    # Room properties
    is_dark = models.BooleanField(
        default=False,
        help_text="Whether room is dark (requires light source)"
    )

    is_safe = models.BooleanField(
        default=False,
        help_text="No combat allowed in this room"
    )

    is_private = models.BooleanField(
        default=False,
        help_text="Limited access room"
    )

    is_indoors = models.BooleanField(
        default=False,
        help_text="Indoor vs outdoor room"
    )

    # Capacity
    max_capacity = models.IntegerField(
        default=50,
        validators=[MinValueValidator(1)],
        help_text="Maximum number of players allowed"
    )

    # Dynamic state
    state = models.JSONField(
        default=dict,
        blank=True,
        help_text="Dynamic room state (puzzle states, flags, etc.)"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['zone', 'key']
        indexes = [
            models.Index(fields=['key']),
            models.Index(fields=['zone']),
        ]
        verbose_name = "Room"
        verbose_name_plural = "Rooms"

    def __str__(self):
        return f"{self.name} ({self.key})"

    @property
    def player_count(self):
        """Count players in this room"""
        return self.players_here.filter(is_online=True).count()

    @property
    def is_full(self):
        """Check if room is at capacity"""
        return self.player_count >= self.max_capacity

    def get_exits(self):
        """Get all exits from this room"""
        return self.exits_out.filter(is_active=True)

    def get_contents(self):
        """Get all items in this room"""
        return self.items_here.all()

    def get_npcs(self):
        """Get all NPCs in this room"""
        return self.npcs_here.filter(is_alive=True)

    def get_players(self):
        """Get all players in this room"""
        return self.players_here.filter(is_online=True)

    def broadcast(self, message, exclude=None):
        """
        Send a message to all players in the room

        Args:
            message: Message to send
            exclude: Player to exclude from broadcast (optional)
        """
        players = self.get_players()
        if exclude:
            players = players.exclude(id=exclude.id)

        # TODO: Implement actual message sending via WebSocket
        return players


class Exit(models.Model):
    """
    Connection between two rooms

    Represents a directional path from one room to another.
    """
    # Rooms
    source = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='exits_out',
        help_text="Room this exit leads from"
    )

    destination = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='exits_in',
        help_text="Room this exit leads to"
    )

    # Direction
    direction = models.CharField(
        max_length=20,
        choices=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
            ('northeast', 'Northeast'),
            ('northwest', 'Northwest'),
            ('southeast', 'Southeast'),
            ('southwest', 'Southwest'),
            ('up', 'Up'),
            ('down', 'Down'),
            ('in', 'In'),
            ('out', 'Out'),
        ],
        help_text="Direction of the exit"
    )

    # Optional custom name
    custom_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Custom exit name (e.g., 'door', 'portal')"
    )

    # Exit properties
    is_locked = models.BooleanField(
        default=False,
        help_text="Whether exit is locked"
    )

    required_key = models.ForeignKey(
        'Item',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='unlocks_exits',
        help_text="Item required to unlock this exit"
    )

    is_hidden = models.BooleanField(
        default=False,
        help_text="Hidden exit (requires discovery)"
    )

    is_one_way = models.BooleanField(
        default=False,
        help_text="Exit only works in one direction"
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Whether exit is currently usable"
    )

    # Messages
    message_enter = models.CharField(
        max_length=200,
        blank=True,
        help_text="Message shown when entering (e.g., 'You walk north.')"
    )

    message_leave = models.CharField(
        max_length=200,
        blank=True,
        help_text="Message shown to others when leaving"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['source', 'direction']
        unique_together = ['source', 'direction']
        indexes = [
            models.Index(fields=['source', 'direction']),
        ]
        verbose_name = "Exit"
        verbose_name_plural = "Exits"

    def __str__(self):
        return f"{self.source.key} -> {self.direction} -> {self.destination.key}"

    @property
    def display_name(self):
        """Get display name for exit"""
        return self.custom_name if self.custom_name else self.direction

    def can_traverse(self, player):
        """
        Check if a player can use this exit

        Args:
            player: Player attempting to use exit

        Returns:
            tuple: (can_use, message)
        """
        if not self.is_active:
            return False, "That way is blocked."

        if self.is_locked:
            if not self.required_key:
                return False, "That exit is locked."

            # Check if player has the required key
            has_key = player.items.filter(id=self.required_key.id).exists()
            if not has_key:
                return False, f"You need {self.required_key.name} to unlock that exit."

        if self.destination.is_full:
            return False, "That area is too crowded right now."

        return True, ""
