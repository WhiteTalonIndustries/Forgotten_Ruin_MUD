"""
NPC (Non-Player Character) Model

Represents AI-controlled characters in the game world.
"""
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class NPC(models.Model):
    """
    Non-Player Character

    AI-controlled entities that can interact with players.
    """
    # Identification
    key = models.CharField(
        max_length=100,
        db_index=True,
        help_text="NPC identifier"
    )

    name = models.CharField(
        max_length=200,
        help_text="NPC name"
    )

    description = models.TextField(
        help_text="NPC description"
    )

    # Location
    location = models.ForeignKey(
        'Room',
        on_delete=models.CASCADE,
        related_name='npcs_here',
        help_text="Current room"
    )

    home_location = models.ForeignKey(
        'Room',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='npcs_home',
        help_text="Home/spawn location"
    )

    # AI Behavior
    AI_TYPES = [
        ('passive', 'Passive'),
        ('friendly', 'Friendly'),
        ('neutral', 'Neutral'),
        ('aggressive', 'Aggressive'),
        ('merchant', 'Merchant'),
        ('quest_giver', 'Quest Giver'),
        ('guard', 'Guard'),
        ('trainer', 'Trainer'),
    ]

    ai_type = models.CharField(
        max_length=50,
        choices=AI_TYPES,
        default='passive',
        help_text="AI behavior type"
    )

    # Dialogue
    dialogue_tree = models.JSONField(
        null=True,
        blank=True,
        help_text="Conversation options and responses"
    )

    greeting_message = models.CharField(
        max_length=500,
        blank=True,
        help_text="Message when player first approaches"
    )

    # Movement
    patrol_route = models.JSONField(
        null=True,
        blank=True,
        help_text="List of room keys to patrol"
    )

    wanders = models.BooleanField(
        default=False,
        help_text="Whether NPC wanders randomly"
    )

    # Combat Stats
    level = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text="NPC level"
    )

    health = models.IntegerField(
        default=100,
        validators=[MinValueValidator(0)],
        help_text="Current health"
    )

    max_health = models.IntegerField(
        default=100,
        validators=[MinValueValidator(1)],
        help_text="Maximum health"
    )

    damage = models.IntegerField(
        default=10,
        validators=[MinValueValidator(0)],
        help_text="Base damage"
    )

    defense = models.IntegerField(
        default=5,
        validators=[MinValueValidator(0)],
        help_text="Defense rating"
    )

    # Loot
    loot_table = models.JSONField(
        default=list,
        blank=True,
        help_text="Items that can drop [{'item_key': 'sword', 'chance': 0.5}, ...]"
    )

    currency_drop = models.JSONField(
        default=dict,
        blank=True,
        help_text="Currency drop range {'min': 10, 'max': 50}"
    )

    experience_reward = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Experience given when defeated"
    )

    # Merchant properties
    sells_items = models.BooleanField(
        default=False,
        help_text="Whether this NPC sells items"
    )

    buys_items = models.BooleanField(
        default=False,
        help_text="Whether this NPC buys items"
    )

    price_modifier = models.FloatField(
        default=1.0,
        validators=[MinValueValidator(0.1)],
        help_text="Price multiplier for buying/selling"
    )

    # Respawn
    respawn_time = models.IntegerField(
        default=300,
        validators=[MinValueValidator(0)],
        help_text="Respawn time in seconds"
    )

    is_alive = models.BooleanField(
        default=True,
        help_text="Whether NPC is alive"
    )

    death_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When NPC died"
    )

    # Flags
    is_unique = models.BooleanField(
        default=False,
        help_text="Only one instance exists"
    )

    is_attackable = models.BooleanField(
        default=True,
        help_text="Can be attacked by players"
    )

    # Custom attributes
    attributes = models.JSONField(
        default=dict,
        blank=True,
        help_text="Custom attributes and flags"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['location', 'name']
        indexes = [
            models.Index(fields=['key']),
            models.Index(fields=['location']),
            models.Index(fields=['is_alive']),
            models.Index(fields=['ai_type']),
        ]
        verbose_name = "NPC"
        verbose_name_plural = "NPCs"

    def __str__(self):
        return f"{self.name} ({self.ai_type})"

    @property
    def health_percentage(self):
        """Get health as percentage"""
        if self.max_health == 0:
            return 0
        return (self.health / self.max_health) * 100

    @property
    def is_merchant(self):
        """Check if NPC is a merchant"""
        return self.sells_items or self.buys_items

    @property
    def should_respawn(self):
        """Check if NPC should respawn"""
        if self.is_alive or not self.death_time:
            return False

        elapsed = (timezone.now() - self.death_time).total_seconds()
        return elapsed >= self.respawn_time

    def take_damage(self, amount):
        """Apply damage to NPC"""
        self.health = max(0, self.health - amount)
        if self.health == 0:
            self.die()
        else:
            self.save(update_fields=['health'])

    def heal(self, amount):
        """Heal the NPC"""
        self.health = min(self.health + amount, self.max_health)
        self.save(update_fields=['health'])

    def die(self):
        """Handle NPC death"""
        self.is_alive = False
        self.health = 0
        self.death_time = timezone.now()
        self.save(update_fields=['is_alive', 'health', 'death_time'])

        # Drop loot
        self.drop_loot()

    def respawn(self):
        """Respawn the NPC"""
        self.is_alive = True
        self.health = self.max_health
        self.death_time = None

        if self.home_location:
            self.location = self.home_location

        self.save(update_fields=['is_alive', 'health', 'death_time', 'location'])

    def drop_loot(self):
        """Drop items from loot table"""
        import random
        from .item import Item

        for loot_entry in self.loot_table:
            if random.random() < loot_entry.get('chance', 0.5):
                # Create item in the room
                # TODO: Implement item creation from loot table
                pass

    def ai_tick(self):
        """
        AI update called periodically

        Handles AI behavior like wandering, attacking, etc.
        """
        if not self.is_alive:
            if self.should_respawn:
                self.respawn()
            return

        # AI behavior based on type
        if self.ai_type == 'aggressive':
            self.check_for_targets()
        elif self.wanders:
            self.maybe_wander()

    def check_for_targets(self):
        """Check for players to attack (aggressive AI)"""
        # TODO: Implement aggressive AI behavior
        pass

    def maybe_wander(self):
        """Randomly move to adjacent room"""
        # TODO: Implement wandering behavior
        pass
