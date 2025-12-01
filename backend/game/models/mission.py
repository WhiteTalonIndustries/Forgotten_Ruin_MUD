"""
Mission System Models

Supports both public missions (server-impacting, award XP/assets) and private missions
(personal narratives without server impact).

Missions follow a cinematic three-act structure:
- Hook: Introduction and motivation
- Act 1: Setup and rising action
- Act 2: Confrontation and complications
- Act 3: Climax and resolution
- Conclusion: Satisfying wrap-up and rewards
"""
from django.db import models
from django.utils import timezone
import uuid


class Mission(models.Model):
    """
    Base mission definition - can be instantiated for players
    """
    MISSION_TYPES = [
        ('recon', 'Reconnaissance'),
        ('raid', 'Raid'),
        ('rescue', 'Rescue'),
        ('escort', 'Escort'),
        ('assassination', 'Assassination'),
        ('defense', 'Defense'),
        ('patrol', 'Patrol'),
        ('investigation', 'Investigation'),
        ('diplomatic', 'Diplomatic'),
        ('scavenge', 'Scavenging'),
        ('custom', 'Custom'),
    ]

    DIFFICULTY_LEVELS = [
        ('trivial', 'Trivial'),
        ('easy', 'Easy'),
        ('moderate', 'Moderate'),
        ('hard', 'Hard'),
        ('very_hard', 'Very Hard'),
        ('extreme', 'Extreme'),
        ('impossible', 'Impossible'),
    ]

    # Identity
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(max_length=100, unique=True, db_index=True)
    name = models.CharField(max_length=200)
    mission_type = models.CharField(max_length=20, choices=MISSION_TYPES, default='custom')

    # Public vs Private
    is_public = models.BooleanField(
        default=True,
        help_text="Public missions affect server state and award XP/assets. Private missions are personal narratives."
    )

    # Mission giver
    given_by_npc = models.ForeignKey(
        'game.NPC',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='missions_given'
    )

    # Difficulty and requirements
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, default='moderate')
    required_level = models.IntegerField(default=1)
    required_squad_size = models.IntegerField(default=1, help_text="Minimum squad members required")

    # Location
    start_location = models.ForeignKey(
        'game.Room',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='missions_starting_here'
    )
    target_location_description = models.TextField(
        blank=True,
        help_text="Description of where the mission takes place (e.g., 'Grid reference 437-862')"
    )

    # Narrative Structure - Hook
    hook_title = models.CharField(max_length=200, help_text="Compelling hook title")
    hook_description = models.TextField(help_text="Opening scene that hooks the player")

    # Narrative Structure - Act 1 (Setup)
    act1_title = models.CharField(max_length=200, default="Setup")
    act1_description = models.TextField(help_text="Setup and rising action")
    act1_objectives = models.JSONField(
        default=list,
        help_text="List of objectives for Act 1: [{'key': 'obj1', 'description': '...', 'required': true}]"
    )

    # Narrative Structure - Act 2 (Confrontation)
    act2_title = models.CharField(max_length=200, default="Confrontation")
    act2_description = models.TextField(help_text="Main conflict and complications")
    act2_objectives = models.JSONField(
        default=list,
        help_text="List of objectives for Act 2"
    )

    # Narrative Structure - Act 3 (Climax)
    act3_title = models.CharField(max_length=200, default="Climax")
    act3_description = models.TextField(help_text="Climactic confrontation")
    act3_objectives = models.JSONField(
        default=list,
        help_text="List of objectives for Act 3"
    )

    # Conclusion
    conclusion_success = models.TextField(
        help_text="Satisfying conclusion if mission succeeds"
    )
    conclusion_failure = models.TextField(
        help_text="Conclusion if mission fails",
        blank=True
    )
    conclusion_partial = models.TextField(
        help_text="Conclusion if mission partially succeeds",
        blank=True
    )

    # Rewards (only for public missions)
    reward_xp = models.IntegerField(default=0, help_text="XP awarded (public missions only)")
    reward_currency = models.IntegerField(default=0, help_text="Currency awarded")
    reward_items = models.JSONField(
        default=list,
        help_text="Items awarded: [{'item_key': 'key', 'quantity': 1}]"
    )
    reward_reputation = models.JSONField(
        default=dict,
        help_text="Reputation changes: {'faction_key': amount}"
    )

    # Failure consequences (public missions only)
    failure_consequences = models.JSONField(
        default=dict,
        help_text="Server state changes on failure (public missions only): {'type': 'consequence_data'}"
    )

    # Mission parameters
    time_limit = models.IntegerField(
        null=True,
        blank=True,
        help_text="Time limit in seconds (null = no limit)"
    )
    can_fail = models.BooleanField(default=True)
    can_abandon = models.BooleanField(default=True)
    is_repeatable = models.BooleanField(default=False)
    cooldown_hours = models.IntegerField(default=0, help_text="Hours before mission can be repeated")

    # Prerequisites
    required_missions_completed = models.JSONField(
        default=list,
        help_text="Mission keys that must be completed first"
    )
    required_items = models.JSONField(
        default=list,
        help_text="Items required to start: [{'item_key': 'key', 'quantity': 1, 'consumed': false}]"
    )

    # Dynamic content
    enemy_spawns = models.JSONField(
        default=list,
        help_text="Enemies to spawn: [{'npc_key': 'key', 'location': 'desc', 'act': 1, 'optional': false}]"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, help_text="Can this mission be started?")

    class Meta:
        ordering = ['required_level', 'name']
        indexes = [
            models.Index(fields=['key']),
            models.Index(fields=['is_public', 'is_active']),
            models.Index(fields=['mission_type']),
        ]

    def __str__(self):
        mission_visibility = "Public" if self.is_public else "Private"
        return f"{self.name} ({mission_visibility}, {self.get_difficulty_display()})"

    def get_total_objectives(self):
        """Return total number of objectives across all acts"""
        return (
            len(self.act1_objectives) +
            len(self.act2_objectives) +
            len(self.act3_objectives)
        )

    def can_player_start(self, player):
        """Check if player meets requirements to start this mission"""
        from .player_mission import PlayerMission

        # Check level requirement
        if player.level < self.required_level:
            return False, f"Requires level {self.required_level}"

        # Check squad size
        if player.squad:
            alive_members = [m for m in player.squad.members.all() if m.health > 0]
            if len(alive_members) < self.required_squad_size:
                return False, f"Requires {self.required_squad_size} squad members"
        elif self.required_squad_size > 1:
            return False, f"Requires {self.required_squad_size} squad members"

        # Check if already active
        active_mission = PlayerMission.objects.filter(
            player=player,
            mission=self,
            status__in=['active', 'in_progress']
        ).first()
        if active_mission:
            return False, "Mission already in progress"

        # Check if on cooldown
        if not self.is_repeatable:
            completed = PlayerMission.objects.filter(
                player=player,
                mission=self,
                status='completed'
            ).exists()
            if completed:
                return False, "Mission already completed"
        else:
            # Check cooldown
            last_completion = PlayerMission.objects.filter(
                player=player,
                mission=self,
                status='completed'
            ).order_by('-completed_at').first()

            if last_completion and self.cooldown_hours > 0:
                cooldown_end = last_completion.completed_at + timezone.timedelta(hours=self.cooldown_hours)
                if timezone.now() < cooldown_end:
                    remaining = cooldown_end - timezone.now()
                    hours = int(remaining.total_seconds() / 3600)
                    return False, f"On cooldown for {hours} more hours"

        # Check prerequisite missions
        if self.required_missions_completed:
            for prereq_key in self.required_missions_completed:
                completed = PlayerMission.objects.filter(
                    player=player,
                    mission__key=prereq_key,
                    status='completed'
                ).exists()
                if not completed:
                    try:
                        prereq_mission = Mission.objects.get(key=prereq_key)
                        return False, f"Requires completion of: {prereq_mission.name}"
                    except Mission.DoesNotExist:
                        return False, f"Requires prerequisite mission: {prereq_key}"

        # Check required items
        if self.required_items:
            from game.models import Item
            for item_req in self.required_items:
                item_key = item_req.get('item_key')
                quantity = item_req.get('quantity', 1)

                player_items = Item.objects.filter(
                    player=player,
                    key=item_key
                ).count()

                if player_items < quantity:
                    return False, f"Requires {quantity}x {item_key}"

        return True, "Requirements met"


class MissionTemplate(models.Model):
    """
    Templates for generating procedural missions
    """
    name = models.CharField(max_length=200)
    mission_type = models.CharField(max_length=20, choices=Mission.MISSION_TYPES)
    is_public = models.BooleanField(default=True)

    # Template structure with variables
    template_data = models.JSONField(
        default=dict,
        help_text="Template with variables: {{enemy_type}}, {{location}}, etc."
    )

    # Variable options
    variable_options = models.JSONField(
        default=dict,
        help_text="Options for each variable: {'enemy_type': ['orcs', 'wizards'], ...}"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"Template: {self.name}"

    def generate_mission(self, variables=None):
        """
        Generate a mission instance from this template
        Variables can be passed in or randomly selected from options
        """
        import random

        if variables is None:
            variables = {}

        # Fill in missing variables with random choices
        for var_name, options in self.variable_options.items():
            if var_name not in variables:
                variables[var_name] = random.choice(options)

        # Replace variables in template data
        mission_data = self._replace_variables(self.template_data, variables)

        # Create mission
        mission = Mission.objects.create(**mission_data)
        return mission

    def _replace_variables(self, data, variables):
        """Recursively replace variables in template data"""
        import re

        if isinstance(data, str):
            for var_name, value in variables.items():
                data = data.replace(f"{{{{{var_name}}}}}", str(value))
            return data
        elif isinstance(data, dict):
            return {k: self._replace_variables(v, variables) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._replace_variables(item, variables) for item in data]
        else:
            return data


class MissionEvent(models.Model):
    """
    Events that can occur during missions
    """
    EVENT_TYPES = [
        ('dialogue', 'Dialogue'),
        ('combat', 'Combat Encounter'),
        ('choice', 'Player Choice'),
        ('discovery', 'Discovery'),
        ('ambush', 'Ambush'),
        ('reinforcements', 'Reinforcements'),
        ('betrayal', 'Betrayal'),
        ('rescue', 'Rescue'),
        ('custom', 'Custom Event'),
    ]

    TRIGGER_TYPES = [
        ('objective_complete', 'When objective completed'),
        ('location_enter', 'When entering location'),
        ('time_elapsed', 'After time elapsed'),
        ('health_threshold', 'When health drops below threshold'),
        ('enemy_killed', 'When specific enemy killed'),
        ('item_acquired', 'When item acquired'),
        ('random', 'Random chance'),
        ('manual', 'Manually triggered'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='events')

    # Event identity
    key = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)

    # When does this event trigger?
    act = models.IntegerField(choices=[(1, 'Act 1'), (2, 'Act 2'), (3, 'Act 3')])
    trigger_type = models.CharField(max_length=30, choices=TRIGGER_TYPES)
    trigger_conditions = models.JSONField(
        default=dict,
        help_text="Conditions for triggering: {'objective_key': 'obj1', 'threshold': 50, ...}"
    )
    trigger_chance = models.FloatField(
        default=1.0,
        help_text="Probability of triggering (0.0 to 1.0)"
    )

    # Event content
    description = models.TextField(help_text="What happens in this event")

    # Event choices (for choice events)
    choices = models.JSONField(
        default=list,
        help_text="Player choices: [{'text': 'Choice text', 'outcome': 'outcome_key', 'requirements': {}}]"
    )

    # Event outcomes
    outcomes = models.JSONField(
        default=dict,
        help_text="Outcomes by outcome_key: {'outcome1': {'description': '...', 'effects': {...}}}"
    )

    # Can this event occur multiple times?
    is_repeatable = models.BooleanField(default=False)

    class Meta:
        ordering = ['mission', 'act', 'name']
        unique_together = ['mission', 'key']

    def __str__(self):
        return f"{self.mission.name} - {self.name} (Act {self.act})"


class MissionDialogue(models.Model):
    """
    Dialogue sequences for missions
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name='dialogues')

    # When does this dialogue occur?
    act = models.IntegerField(choices=[(1, 'Act 1'), (2, 'Act 2'), (3, 'Act 3'), (0, 'Hook')])
    trigger_point = models.CharField(
        max_length=50,
        help_text="When to show: 'start', 'end', 'objective_complete', etc."
    )

    # Who is speaking?
    speaker_npc = models.ForeignKey(
        'game.NPC',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    speaker_name = models.CharField(
        max_length=100,
        help_text="Override speaker name (e.g., 'Unknown Voice')"
    )

    # Dialogue content
    dialogue_tree = models.JSONField(
        default=dict,
        help_text="Dialogue tree structure with branches"
    )

    # Order in sequence
    sequence_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['mission', 'act', 'sequence_order']

    def __str__(self):
        speaker = self.speaker_name or (self.speaker_npc.name if self.speaker_npc else "Unknown")
        return f"{self.mission.name} - {speaker} (Act {self.act})"
