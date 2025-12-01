"""
Player Mission Instance Models

Tracks individual player progress through missions
"""
from django.db import models
from django.utils import timezone
import uuid


class PlayerMission(models.Model):
    """
    Tracks a player's progress through a specific mission instance
    """
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('active', 'Active'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('abandoned', 'Abandoned'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player = models.ForeignKey('game.Player', on_delete=models.CASCADE, related_name='missions')
    mission = models.ForeignKey('game.Mission', on_delete=models.CASCADE, related_name='player_instances')

    # Status tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    current_act = models.IntegerField(default=0, help_text="0=Hook, 1=Act1, 2=Act2, 3=Act3, 4=Complete")

    # Timing
    accepted_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    time_limit_expires = models.DateTimeField(null=True, blank=True)

    # Progress tracking
    objectives_completed = models.JSONField(
        default=dict,
        help_text="Track objective completion: {'act1_obj1': true, 'act2_obj1': false, ...}"
    )
    events_triggered = models.JSONField(
        default=list,
        help_text="List of event keys that have been triggered"
    )
    choices_made = models.JSONField(
        default=list,
        help_text="List of choices made: [{'event_key': 'key', 'choice': 'text', 'outcome': 'key'}]"
    )

    # Mission state
    mission_variables = models.JSONField(
        default=dict,
        help_text="Mission-specific variables: {'enemy_count': 5, 'hostages_saved': 2, ...}"
    )

    # Completion tracking
    success_level = models.CharField(
        max_length=20,
        choices=[
            ('full', 'Full Success'),
            ('partial', 'Partial Success'),
            ('failure', 'Failure'),
        ],
        null=True,
        blank=True
    )
    completion_notes = models.TextField(blank=True, help_text="Notes about how mission concluded")

    # Rewards claimed
    rewards_claimed = models.BooleanField(default=False)
    xp_awarded = models.IntegerField(default=0)
    currency_awarded = models.IntegerField(default=0)
    items_awarded = models.JSONField(default=list)

    # Squad snapshot (for reference)
    squad_snapshot = models.JSONField(
        default=dict,
        help_text="Snapshot of squad at mission start"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['player', 'status']),
            models.Index(fields=['mission', 'status']),
        ]

    def __str__(self):
        return f"{self.player.character_name} - {self.mission.name} ({self.get_status_display()})"

    def accept(self):
        """Player accepts the mission"""
        if self.status != 'available':
            return False, "Mission already accepted"

        # Check if player can start
        can_start, message = self.mission.can_player_start(self.player)
        if not can_start:
            return False, message

        self.status = 'active'
        self.accepted_at = timezone.now()
        self.current_act = 0  # Start at hook

        # Set time limit if applicable
        if self.mission.time_limit:
            self.time_limit_expires = timezone.now() + timezone.timedelta(seconds=self.mission.time_limit)

        # Take squad snapshot
        if self.player.squad:
            self.squad_snapshot = {
                'squad_name': self.player.squad.name,
                'members': [
                    {
                        'name': member.name,
                        'level': member.level,
                        'health': member.health,
                    }
                    for member in self.player.squad.members.all()
                ]
            }

        # Consume required items if specified
        if self.mission.required_items:
            from game.models import Item
            for item_req in self.mission.required_items:
                if item_req.get('consumed', False):
                    item_key = item_req['item_key']
                    quantity = item_req.get('quantity', 1)

                    items = Item.objects.filter(player=self.player, key=item_key)[:quantity]
                    for item in items:
                        item.delete()

        self.save()
        return True, f"Mission accepted: {self.mission.name}"

    def start_act(self, act_number):
        """Begin a specific act"""
        if self.current_act >= act_number:
            return False, "Act already started or completed"

        self.current_act = act_number

        if act_number == 1 and not self.started_at:
            self.started_at = timezone.now()
            self.status = 'in_progress'

        self.save()
        return True, f"Started {self.mission.get_act_title(act_number)}"

    def complete_objective(self, objective_key):
        """Mark an objective as completed"""
        if self.status not in ['active', 'in_progress']:
            return False, "Mission is not active"

        # Check if already completed
        if self.objectives_completed.get(objective_key, False):
            return False, "Objective already completed"

        # Mark as completed
        self.objectives_completed[objective_key] = True
        self.save()

        # Check if act is complete
        self._check_act_completion()

        return True, "Objective completed"

    def _check_act_completion(self):
        """Check if current act is complete and advance if so"""
        if self.current_act == 0:
            # Hook complete, move to Act 1
            self.start_act(1)
            return

        # Get objectives for current act
        act_objectives = []
        if self.current_act == 1:
            act_objectives = self.mission.act1_objectives
        elif self.current_act == 2:
            act_objectives = self.mission.act2_objectives
        elif self.current_act == 3:
            act_objectives = self.mission.act3_objectives

        # Check if all required objectives are complete
        required_objectives = [obj for obj in act_objectives if obj.get('required', True)]
        all_complete = all(
            self.objectives_completed.get(obj['key'], False)
            for obj in required_objectives
        )

        if all_complete:
            if self.current_act < 3:
                # Move to next act
                self.start_act(self.current_act + 1)
            else:
                # Mission complete
                self._complete_mission('full')

    def _complete_mission(self, success_level):
        """Complete the mission"""
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.success_level = success_level
        self.current_act = 4

        # Award rewards (only for public missions)
        if self.mission.is_public and not self.rewards_claimed:
            self._award_rewards()

        self.save()

    def _award_rewards(self):
        """Award mission rewards to player"""
        from game.models import Item

        # Award XP
        if self.mission.reward_xp > 0:
            self.player.gain_xp(self.mission.reward_xp)
            self.xp_awarded = self.mission.reward_xp

        # Award currency
        if self.mission.reward_currency > 0:
            # Assuming player has a currency field
            if hasattr(self.player, 'currency'):
                self.player.currency += self.mission.reward_currency
                self.player.save()
            self.currency_awarded = self.mission.reward_currency

        # Award items
        awarded_items = []
        for item_reward in self.mission.reward_items:
            item_key = item_reward['item_key']
            quantity = item_reward.get('quantity', 1)

            for _ in range(quantity):
                # Create item for player
                try:
                    template = Item.objects.filter(key=item_key).first()
                    if template:
                        item = Item.objects.create(
                            key=template.key,
                            name=template.name,
                            description=template.description,
                            item_type=template.item_type,
                            player=self.player,
                            location=self.player.location,
                        )
                        awarded_items.append(item.name)
                except Exception as e:
                    print(f"Error awarding item {item_key}: {e}")

        self.items_awarded = awarded_items

        # Award reputation changes
        if self.mission.reward_reputation:
            # TODO: Implement reputation system
            pass

        self.rewards_claimed = True
        self.save()

    def fail_mission(self, reason=""):
        """Fail the mission"""
        if not self.mission.can_fail:
            return False, "This mission cannot be failed"

        self.status = 'failed'
        self.completed_at = timezone.now()
        self.success_level = 'failure'
        self.completion_notes = reason

        # Apply failure consequences (public missions only)
        if self.mission.is_public and self.mission.failure_consequences:
            self._apply_failure_consequences()

        self.save()
        return True, f"Mission failed: {reason}"

    def _apply_failure_consequences(self):
        """Apply consequences of mission failure"""
        # TODO: Implement based on consequence types
        # Could include: reputation loss, area changes, NPC deaths, etc.
        pass

    def abandon_mission(self):
        """Abandon the mission"""
        if not self.mission.can_abandon:
            return False, "This mission cannot be abandoned"

        self.status = 'abandoned'
        self.completed_at = timezone.now()
        self.save()
        return True, "Mission abandoned"

    def check_time_limit(self):
        """Check if mission has exceeded time limit"""
        if self.time_limit_expires and timezone.now() > self.time_limit_expires:
            self.fail_mission("Time limit exceeded")
            return True
        return False

    def get_progress_summary(self):
        """Get a summary of mission progress"""
        total_objectives = self.mission.get_total_objectives()
        completed_count = sum(1 for completed in self.objectives_completed.values() if completed)

        return {
            'mission_name': self.mission.name,
            'status': self.get_status_display(),
            'current_act': self.current_act,
            'act_name': self.mission.get_act_title(self.current_act) if self.current_act > 0 else 'Hook',
            'objectives_completed': completed_count,
            'total_objectives': total_objectives,
            'progress_percent': int((completed_count / total_objectives * 100)) if total_objectives > 0 else 0,
            'time_remaining': self._get_time_remaining(),
            'success_level': self.success_level,
        }

    def _get_time_remaining(self):
        """Get formatted time remaining"""
        if not self.time_limit_expires:
            return None

        remaining = self.time_limit_expires - timezone.now()
        if remaining.total_seconds() <= 0:
            return "EXPIRED"

        hours = int(remaining.total_seconds() / 3600)
        minutes = int((remaining.total_seconds() % 3600) / 60)
        return f"{hours}h {minutes}m"

    def trigger_event(self, event_key):
        """Trigger a mission event"""
        if event_key in self.events_triggered:
            return False, "Event already triggered"

        self.events_triggered.append(event_key)
        self.save()
        return True, "Event triggered"

    def make_choice(self, event_key, choice_text, outcome_key):
        """Record a player choice"""
        choice_record = {
            'event_key': event_key,
            'choice': choice_text,
            'outcome': outcome_key,
            'timestamp': timezone.now().isoformat(),
        }
        self.choices_made.append(choice_record)
        self.save()
        return True, "Choice recorded"

    def set_variable(self, key, value):
        """Set a mission variable"""
        self.mission_variables[key] = value
        self.save()

    def get_variable(self, key, default=None):
        """Get a mission variable"""
        return self.mission_variables.get(key, default)

    def increment_variable(self, key, amount=1):
        """Increment a mission variable"""
        current = self.mission_variables.get(key, 0)
        self.mission_variables[key] = current + amount
        self.save()
        return self.mission_variables[key]
