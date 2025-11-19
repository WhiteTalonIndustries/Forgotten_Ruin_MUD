"""
Quest Models

Represents quests and player quest progress.
"""
from django.db import models
from django.core.validators import MinValueValidator


class Quest(models.Model):
    """
    A quest that players can undertake

    Quests have objectives, requirements, and rewards.
    """
    # Identification
    key = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="Unique quest identifier"
    )

    title = models.CharField(
        max_length=200,
        help_text="Quest title"
    )

    description = models.TextField(
        help_text="Quest description and story"
    )

    # Quest giver
    quest_giver = models.ForeignKey(
        'NPC',
        on_delete=models.CASCADE,
        related_name='quests_given',
        help_text="NPC who gives this quest"
    )

    # Requirements
    required_level = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text="Minimum level to accept quest"
    )

    prerequisite_quests = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        help_text="Quests that must be completed first"
    )

    # Objectives
    objectives = models.JSONField(
        help_text="""
        Quest objectives in format:
        [
            {'type': 'kill', 'target': 'goblin', 'count': 10},
            {'type': 'collect', 'item': 'herb', 'count': 5},
            {'type': 'talk_to', 'npc': 'elder'},
            {'type': 'visit', 'room': 'ancient_temple'},
        ]
        """
    )

    # Rewards
    experience_reward = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Experience points awarded"
    )

    currency_reward = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Currency awarded"
    )

    item_rewards = models.ManyToManyField(
        'Item',
        blank=True,
        related_name='quest_rewards',
        help_text="Items awarded upon completion"
    )

    # Quest properties
    is_repeatable = models.BooleanField(
        default=False,
        help_text="Can be repeated"
    )

    cooldown_hours = models.IntegerField(
        default=24,
        validators=[MinValueValidator(0)],
        help_text="Hours before quest can be repeated"
    )

    time_limit_minutes = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        help_text="Time limit to complete quest (minutes)"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['required_level', 'title']
        indexes = [
            models.Index(fields=['key']),
            models.Index(fields=['required_level']),
        ]
        verbose_name = "Quest"
        verbose_name_plural = "Quests"

    def __str__(self):
        return f"{self.title} (Level {self.required_level})"

    def can_accept(self, player):
        """
        Check if player can accept this quest

        Args:
            player: Player object

        Returns:
            tuple: (can_accept, reason)
        """
        if player.level < self.required_level:
            return False, f"You must be level {self.required_level} to accept this quest."

        # Check prerequisites
        for prereq in self.prerequisite_quests.all():
            completed = PlayerQuest.objects.filter(
                player=player,
                quest=prereq,
                status='completed'
            ).exists()

            if not completed:
                return False, f"You must complete '{prereq.title}' first."

        # Check if already active
        has_active = PlayerQuest.objects.filter(
            player=player,
            quest=self,
            status='active'
        ).exists()

        if has_active:
            return False, "You already have this quest."

        # Check if repeatable
        if not self.is_repeatable:
            has_completed = PlayerQuest.objects.filter(
                player=player,
                quest=self,
                status='completed'
            ).exists()

            if has_completed:
                return False, "You have already completed this quest."

        return True, ""


class PlayerQuest(models.Model):
    """
    Tracks a player's progress on a quest
    """
    player = models.ForeignKey(
        'Player',
        on_delete=models.CASCADE,
        related_name='quests',
        help_text="Player undertaking the quest"
    )

    quest = models.ForeignKey(
        Quest,
        on_delete=models.CASCADE,
        related_name='player_quests',
        help_text="The quest"
    )

    # Status
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('abandoned', 'Abandoned'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        help_text="Quest status"
    )

    # Progress
    progress = models.JSONField(
        default=dict,
        help_text="""
        Tracks objective completion:
        {
            '0': {'current': 5, 'required': 10},  # Objective index
            '1': {'current': 3, 'required': 5},
        }
        """
    )

    # Timestamps
    accepted_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When quest was accepted"
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When quest was completed"
    )

    deadline = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Quest deadline (if time-limited)"
    )

    class Meta:
        ordering = ['-accepted_at']
        indexes = [
            models.Index(fields=['player', 'status']),
            models.Index(fields=['quest', 'status']),
        ]
        verbose_name = "Player Quest"
        verbose_name_plural = "Player Quests"
        unique_together = ['player', 'quest', 'status']

    def __str__(self):
        return f"{self.player.character_name} - {self.quest.title} ({self.status})"

    @property
    def is_complete(self):
        """Check if all objectives are complete"""
        for idx, objective in enumerate(self.quest.objectives):
            progress = self.progress.get(str(idx), {})
            current = progress.get('current', 0)
            required = objective.get('count', 1)

            if current < required:
                return False

        return True

    def update_progress(self, objective_index, amount=1):
        """
        Update progress for an objective

        Args:
            objective_index: Index of the objective
            amount: Amount to increment by
        """
        key = str(objective_index)
        if key not in self.progress:
            self.progress[key] = {'current': 0}

        self.progress[key]['current'] += amount

        objective = self.quest.objectives[objective_index]
        required = objective.get('count', 1)
        self.progress[key]['required'] = required

        # Check if quest is now complete
        if self.is_complete and self.status == 'active':
            self.complete()
        else:
            self.save(update_fields=['progress'])

    def complete(self):
        """Mark quest as completed and grant rewards"""
        from django.utils import timezone

        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save(update_fields=['status', 'completed_at'])

        # Grant rewards
        self.grant_rewards()

    def grant_rewards(self):
        """Grant quest rewards to player"""
        # Experience
        if self.quest.experience_reward > 0:
            self.player.gain_experience(self.quest.experience_reward)

        # Currency
        if self.quest.currency_reward > 0:
            self.player.currency += self.quest.currency_reward
            self.player.save(update_fields=['currency'])

        # Items
        for item_template in self.quest.item_rewards.all():
            # TODO: Create copy of item and give to player
            pass

    def abandon(self):
        """Abandon the quest"""
        self.status = 'abandoned'
        self.save(update_fields=['status'])

    def fail(self):
        """Mark quest as failed"""
        self.status = 'failed'
        self.save(update_fields=['status'])
