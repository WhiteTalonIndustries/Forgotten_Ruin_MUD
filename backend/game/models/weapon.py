"""
Weapon Model
"""
from django.db import models

class Weapon(models.Model):
    """
    Represents a weapon in the game.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    WEAPON_TYPES = [
        ('military', 'Military'),
        ('medieval', 'Medieval'),
    ]
    weapon_type = models.CharField(max_length=20, choices=WEAPON_TYPES, default='military')

    range = models.CharField(max_length=20, blank=True, help_text="e.g., '24\" / 36\"' or '12\"'")
    shots = models.CharField(max_length=20, default='1', help_text="e.g., '1', '4', or 'Explosive (2\" radius)'")
    damage = models.CharField(max_length=20, default='+0')

    properties = models.JSONField(default=dict, blank=True, help_text="e.g., {'heavy_weapon': True, 'piercing': True}")

    def __str__(self):
        return self.name
