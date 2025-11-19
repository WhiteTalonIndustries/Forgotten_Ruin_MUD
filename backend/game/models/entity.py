"""
Base Entity Model

All game objects inherit from this base entity class.
"""
from django.db import models
from django.utils import timezone


class Entity(models.Model):
    """
    Base class for all game entities (players, NPCs, items, rooms)

    Provides common fields and methods shared by all game objects.
    """
    # Basic identification
    key = models.CharField(
        max_length=100,
        db_index=True,
        help_text="Unique identifier/name for this entity"
    )

    name = models.CharField(
        max_length=200,
        help_text="Display name for this entity"
    )

    description = models.TextField(
        blank=True,
        help_text="Detailed description of the entity"
    )

    # Entity type for querying
    entity_type = models.CharField(
        max_length=50,
        db_index=True,
        help_text="Type of entity (player, npc, item, room)"
    )

    # Flexible attribute storage
    attributes = models.JSONField(
        default=dict,
        blank=True,
        help_text="Flexible JSON storage for custom attributes"
    )

    # Metadata
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When this entity was created"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last time this entity was updated"
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Whether this entity is active in the game world"
    )

    class Meta:
        abstract = True
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['key']),
            models.Index(fields=['entity_type']),
        ]

    def __str__(self):
        return f"{self.name} ({self.entity_type})"

    def get_attribute(self, key, default=None):
        """Get a custom attribute value"""
        return self.attributes.get(key, default)

    def set_attribute(self, key, value):
        """Set a custom attribute value"""
        self.attributes[key] = value
        self.save(update_fields=['attributes', 'updated_at'])

    def delete_attribute(self, key):
        """Delete a custom attribute"""
        if key in self.attributes:
            del self.attributes[key]
            self.save(update_fields=['attributes', 'updated_at'])
