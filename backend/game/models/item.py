"""
Item Model

Represents items and equipment in the game world.
"""
from django.db import models
from django.core.validators import MinValueValidator


class Item(models.Model):
    """
    Game item that can be found, equipped, or used

    Items can exist in rooms, player inventories, or NPC inventories.
    """
    # Identification
    key = models.CharField(
        max_length=100,
        db_index=True,
        help_text="Item identifier"
    )

    name = models.CharField(
        max_length=200,
        help_text="Display name"
    )

    description = models.TextField(
        help_text="Detailed description"
    )

    # Item type
    ITEM_TYPES = [
        ('weapon', 'Weapon'),
        ('armor', 'Armor'),
        ('consumable', 'Consumable'),
        ('quest', 'Quest Item'),
        ('currency', 'Currency'),
        ('container', 'Container'),
        ('tool', 'Tool'),
        ('misc', 'Miscellaneous'),
    ]

    item_type = models.CharField(
        max_length=50,
        choices=ITEM_TYPES,
        default='misc',
        help_text="Type of item"
    )

    # Location - can be in room, player inventory, or NPC inventory
    room = models.ForeignKey(
        'Room',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='items_here',
        help_text="Room where item is located"
    )

    owner_player = models.ForeignKey(
        'Player',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='items',
        help_text="Player who owns this item"
    )

    owner_npc = models.ForeignKey(
        'NPC',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='items',
        help_text="NPC who owns this item"
    )

    # Properties
    weight = models.FloatField(
        default=1.0,
        validators=[MinValueValidator(0)],
        help_text="Weight in units"
    )

    value = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Base value in currency"
    )

    # Item flags
    is_takeable = models.BooleanField(
        default=True,
        help_text="Can be picked up"
    )

    is_droppable = models.BooleanField(
        default=True,
        help_text="Can be dropped"
    )

    is_unique = models.BooleanField(
        default=False,
        help_text="Only one can exist per player"
    )

    is_quest_item = models.BooleanField(
        default=False,
        help_text="Required for a quest"
    )

    # Equipment properties
    EQUIPMENT_SLOTS = [
        ('head', 'Head'),
        ('neck', 'Neck'),
        ('chest', 'Chest'),
        ('back', 'Back'),
        ('arms', 'Arms'),
        ('hands', 'Hands'),
        ('waist', 'Waist'),
        ('legs', 'Legs'),
        ('feet', 'Feet'),
        ('finger1', 'Finger 1'),
        ('finger2', 'Finger 2'),
        ('main_hand', 'Main Hand'),
        ('off_hand', 'Off Hand'),
        ('two_hand', 'Two Handed'),
    ]

    equipment_slot = models.CharField(
        max_length=50,
        choices=EQUIPMENT_SLOTS,
        null=True,
        blank=True,
        help_text="Equipment slot if this is wearable"
    )

    is_equipped = models.BooleanField(
        default=False,
        help_text="Currently equipped"
    )

    # Requirements
    required_level = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text="Minimum level to use"
    )

    # Stats and modifiers
    stat_modifiers = models.JSONField(
        default=dict,
        blank=True,
        help_text="Stat bonuses {'strength': 5, 'defense': 10, ...}"
    )

    # Consumable properties
    uses_remaining = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Number of uses left (for consumables)"
    )

    max_uses = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        help_text="Maximum uses"
    )

    effect = models.JSONField(
        null=True,
        blank=True,
        help_text="Effect when used {'type': 'heal', 'amount': 50}"
    )

    # Container properties
    container_capacity = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        help_text="Items it can hold if it's a container"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['key']),
            models.Index(fields=['item_type']),
            models.Index(fields=['owner_player']),
            models.Index(fields=['room']),
        ]
        verbose_name = "Item"
        verbose_name_plural = "Items"

    def __str__(self):
        return f"{self.name} ({self.item_type})"

    @property
    def is_in_world(self):
        """Check if item is in a room (not in inventory)"""
        return self.room is not None

    @property
    def is_usable(self):
        """Check if item can be used"""
        if self.uses_remaining is not None:
            return self.uses_remaining > 0
        return True

    @property
    def is_equippable(self):
        """Check if item can be equipped"""
        return self.equipment_slot is not None

    def use(self, user):
        """
        Use the item

        Args:
            user: Player or NPC using the item

        Returns:
            dict: Result of using the item
        """
        if not self.is_usable:
            return {'success': False, 'message': "This item has no uses remaining."}

        if self.uses_remaining is not None:
            self.uses_remaining -= 1
            if self.uses_remaining == 0:
                # Item consumed
                self.delete()

        return {'success': True, 'message': f"You use {self.name}.", 'effect': self.effect}

    def equip(self, player):
        """Equip this item to a player"""
        if not self.is_equippable:
            return False, "This item cannot be equipped."

        if player.level < self.required_level:
            return False, f"You must be level {self.required_level} to use this."

        # Unequip any item in the same slot
        if self.equipment_slot in ['two_hand']:
            # Two-handed weapons require both hands
            player.items.filter(
                equipment_slot__in=['main_hand', 'off_hand'],
                is_equipped=True
            ).update(is_equipped=False)
        else:
            player.items.filter(
                equipment_slot=self.equipment_slot,
                is_equipped=True
            ).update(is_equipped=False)

        self.is_equipped = True
        self.save(update_fields=['is_equipped'])
        return True, f"You equip {self.name}."

    def unequip(self):
        """Unequip this item"""
        if not self.is_equipped:
            return False, "This item is not equipped."

        self.is_equipped = False
        self.save(update_fields=['is_equipped'])
        return True, f"You unequip {self.name}."
