"""
Zone Model

Represents a zone/area in the game world that groups related rooms.
"""
from django.db import models


class Zone(models.Model):
    """
    A zone or area in the game world

    Zones group related rooms together for organization and management.
    """
    # Identification
    key = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="Unique zone identifier (e.g., 'newbie_town')"
    )

    name = models.CharField(
        max_length=200,
        help_text="Display name of the zone"
    )

    description = models.TextField(
        blank=True,
        help_text="Zone description and lore"
    )

    # Zone properties
    level_min = models.IntegerField(
        default=1,
        help_text="Recommended minimum level"
    )

    level_max = models.IntegerField(
        default=100,
        help_text="Recommended maximum level"
    )

    # Flags
    is_safe = models.BooleanField(
        default=False,
        help_text="No combat allowed in entire zone"
    )

    is_pvp = models.BooleanField(
        default=False,
        help_text="Player vs Player combat allowed"
    )

    is_hidden = models.BooleanField(
        default=False,
        help_text="Hidden from zone lists"
    )

    is_instanced = models.BooleanField(
        default=False,
        help_text="Each party gets their own copy"
    )

    # Theme/Environment
    climate = models.CharField(
        max_length=50,
        blank=True,
        choices=[
            ('temperate', 'Temperate'),
            ('tropical', 'Tropical'),
            ('arctic', 'Arctic'),
            ('desert', 'Desert'),
            ('underground', 'Underground'),
            ('magical', 'Magical'),
        ],
        help_text="Zone climate/environment"
    )

    # Custom attributes
    attributes = models.JSONField(
        default=dict,
        blank=True,
        help_text="Custom zone attributes"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Builder info
    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='zones_created',
        help_text="User who created this zone"
    )

    class Meta:
        ordering = ['level_min', 'name']
        indexes = [
            models.Index(fields=['key']),
            models.Index(fields=['level_min', 'level_max']),
        ]
        verbose_name = "Zone"
        verbose_name_plural = "Zones"

    def __str__(self):
        return f"{self.name} (Levels {self.level_min}-{self.level_max})"

    @property
    def room_count(self):
        """Count rooms in this zone"""
        return self.rooms.count()

    @property
    def player_count(self):
        """Count players currently in this zone"""
        return sum(room.player_count for room in self.rooms.all())
