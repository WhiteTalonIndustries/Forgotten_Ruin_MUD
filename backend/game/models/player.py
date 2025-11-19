"""
Player Model

Represents a player character in the game world.
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Player(models.Model):
    """
    Player character model

    Linked to a User account for authentication.
    Contains all character stats, inventory, and game state.
    """
    # Link to authentication user
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='player',
        help_text="User account for this player"
    )

    # Character identity
    character_name = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="In-game character name"
    )

    description = models.TextField(
        blank=True,
        default="A mysterious adventurer.",
        help_text="Character description"
    )

    # Location
    location = models.ForeignKey(
        'Room',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='players_here',
        help_text="Current room location"
    )

    home = models.ForeignKey(
        'Room',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='players_home',
        help_text="Home/respawn location"
    )

    # Core Stats
    level = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Character level"
    )

    experience = models.BigIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Experience points"
    )

    # Health/Mana
    health = models.IntegerField(
        default=100,
        validators=[MinValueValidator(0)],
        help_text="Current health points"
    )

    max_health = models.IntegerField(
        default=100,
        validators=[MinValueValidator(1)],
        help_text="Maximum health points"
    )

    mana = models.IntegerField(
        default=100,
        validators=[MinValueValidator(0)],
        help_text="Current mana points"
    )

    max_mana = models.IntegerField(
        default=100,
        validators=[MinValueValidator(1)],
        help_text="Maximum mana points"
    )

    # Attributes
    strength = models.IntegerField(
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Physical power"
    )

    dexterity = models.IntegerField(
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Agility and reflexes"
    )

    intelligence = models.IntegerField(
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Mental acuity and magical power"
    )

    constitution = models.IntegerField(
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Endurance and vitality"
    )

    # State
    position = models.CharField(
        max_length=20,
        default='standing',
        choices=[
            ('standing', 'Standing'),
            ('sitting', 'Sitting'),
            ('lying', 'Lying Down'),
            ('sleeping', 'Sleeping'),
            ('dead', 'Dead'),
        ],
        help_text="Character position/posture"
    )

    is_online = models.BooleanField(
        default=False,
        help_text="Whether player is currently connected"
    )

    # Inventory
    inventory_size = models.IntegerField(
        default=20,
        validators=[MinValueValidator(1)],
        help_text="Maximum inventory capacity"
    )

    currency = models.BigIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="In-game currency"
    )

    # Metadata
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When character was created"
    )

    last_login = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Last login time"
    )

    last_action = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Last action/command time"
    )

    total_playtime = models.DurationField(
        default=timezone.timedelta,
        help_text="Total time played"
    )

    # Flexible attributes
    attributes = models.JSONField(
        default=dict,
        blank=True,
        help_text="Custom attributes and flags"
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['character_name']),
            models.Index(fields=['is_online']),
            models.Index(fields=['level']),
        ]
        verbose_name = "Player"
        verbose_name_plural = "Players"

    def __str__(self):
        return f"{self.character_name} (Level {self.level})"

    @property
    def is_alive(self):
        """Check if player is alive"""
        return self.health > 0 and self.position != 'dead'

    @property
    def inventory_count(self):
        """Count items in inventory"""
        return self.items.count()

    @property
    def is_inventory_full(self):
        """Check if inventory is full"""
        return self.inventory_count >= self.inventory_size

    def heal(self, amount):
        """Heal the player"""
        self.health = min(self.health + amount, self.max_health)
        self.save(update_fields=['health'])

    def take_damage(self, amount):
        """Apply damage to player"""
        self.health = max(0, self.health - amount)
        if self.health == 0:
            self.position = 'dead'
        self.save(update_fields=['health', 'position'])

    def restore_mana(self, amount):
        """Restore mana"""
        self.mana = min(self.mana + amount, self.max_mana)
        self.save(update_fields=['mana'])

    def spend_mana(self, amount):
        """Spend mana"""
        if self.mana >= amount:
            self.mana -= amount
            self.save(update_fields=['mana'])
            return True
        return False

    def gain_experience(self, amount):
        """Add experience points"""
        self.experience += amount
        # TODO: Check for level up
        self.save(update_fields=['experience'])

    def move_to(self, room):
        """Move player to a new room"""
        self.location = room
        self.save(update_fields=['location'])
