"""
Ability Models
"""
from django.db import models

class Skill(models.Model):
    """
    Represents a skill that a player can learn.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class Spell(models.Model):
    """
    Represents a spell that a player can cast.
    """
    name = models.CharField(max_length=100, unique=True)
    power_cost = models.IntegerField(default=3)
    range = models.CharField(max_length=20, blank=True)
    targets = models.CharField(max_length=100, blank=True)
    resist = models.CharField(max_length=20, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class Transformation(models.Model):
    """
    Represents a transformation that a player can undergo.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    upgrades = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.name
