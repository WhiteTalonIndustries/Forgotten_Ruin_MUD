"""
Squad Models

Represents a 9-person US Army Ranger squad controlled by the player.
Based on the Forgotten Ruin lore.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Squad(models.Model):
    """
    A 9-person Ranger squad controlled by a player

    Squad composition:
    - 1 Squad Leader (Staff Sergeant) - player's primary character
    - 2 Fire Teams (Alpha and Bravo), each with:
      - 1 Team Leader (Sergeant)
      - 1 Automatic Rifleman (Specialist)
      - 1 Grenadier (Specialist)
      - 1 Rifleman (Private First Class)
    """
    # Link to player
    player = models.OneToOneField(
        'Player',
        on_delete=models.CASCADE,
        related_name='squad',
        help_text="Player who commands this squad"
    )

    # Squad identity
    squad_name = models.CharField(
        max_length=100,
        help_text="Squad designation (e.g., 'Alpha Squad', 'Bravo Squad')"
    )

    callsign = models.CharField(
        max_length=50,
        blank=True,
        help_text="Radio callsign (e.g., 'Havoc', 'Reaper')"
    )

    # Squad status
    morale = models.IntegerField(
        default=100,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Squad morale (affects performance)"
    )

    cohesion = models.IntegerField(
        default=50,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Squad cohesion (improves with battles fought together)"
    )

    # Squad stats (aggregated from members)
    total_kills = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Total enemy kills by squad"
    )

    missions_completed = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Number of missions completed"
    )

    # Supply tracking
    ammunition_556mm = models.IntegerField(
        default=1000,
        validators=[MinValueValidator(0)],
        help_text="5.56mm rounds for M4A1 carbines"
    )

    ammunition_556mm_belt = models.IntegerField(
        default=600,
        validators=[MinValueValidator(0)],
        help_text="5.56mm belt ammunition for M249 LMGs"
    )

    grenades_frag = models.IntegerField(
        default=20,
        validators=[MinValueValidator(0)],
        help_text="Fragmentation grenades"
    )

    grenades_40mm = models.IntegerField(
        default=30,
        validators=[MinValueValidator(0)],
        help_text="40mm grenades for M320 launchers"
    )

    # Medical supplies
    medkits = models.IntegerField(
        default=10,
        validators=[MinValueValidator(0)],
        help_text="First aid kits"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Squad"
        verbose_name_plural = "Squads"

    def __str__(self):
        return f"{self.squad_name} ({self.player.character_name})"

    @property
    def squad_leader(self):
        """Get the Squad Leader (player's primary character)"""
        return self.members.filter(role='squad_leader').first()

    @property
    def alpha_team(self):
        """Get Alpha Team members"""
        return self.members.filter(fire_team='alpha').order_by('role')

    @property
    def bravo_team(self):
        """Get Bravo Team members"""
        return self.members.filter(fire_team='bravo').order_by('role')

    @property
    def alive_members(self):
        """Get all living squad members"""
        return self.members.filter(is_alive=True)

    @property
    def casualty_count(self):
        """Count casualties"""
        return self.members.filter(is_alive=False).count()

    @property
    def average_health(self):
        """Calculate average health percentage of squad"""
        alive = self.alive_members
        if not alive:
            return 0
        total = sum(member.health_percentage for member in alive)
        return total / alive.count()

    def resupply_ammunition(self, amount_556=100, amount_556_belt=100):
        """Resupply squad ammunition"""
        self.ammunition_556mm += amount_556
        self.ammunition_556mm_belt += amount_556_belt
        self.save(update_fields=['ammunition_556mm', 'ammunition_556mm_belt'])

    def use_ammunition(self, rounds_556=0, rounds_556_belt=0):
        """Use ammunition (returns True if enough ammo available)"""
        if self.ammunition_556mm >= rounds_556 and self.ammunition_556mm_belt >= rounds_556_belt:
            self.ammunition_556mm -= rounds_556
            self.ammunition_556mm_belt -= rounds_556_belt
            self.save(update_fields=['ammunition_556mm', 'ammunition_556mm_belt'])
            return True
        return False


class SquadMember(models.Model):
    """
    Individual squad member

    Represents one of the 9 Rangers in a squad.
    """
    # Link to squad
    squad = models.ForeignKey(
        Squad,
        on_delete=models.CASCADE,
        related_name='members',
        help_text="Squad this member belongs to"
    )

    # Identity
    name = models.CharField(
        max_length=100,
        help_text="Member's name (e.g., 'SSG Thompson')"
    )

    rank = models.CharField(
        max_length=50,
        choices=[
            ('staff_sergeant', 'Staff Sergeant (SSG)'),
            ('sergeant', 'Sergeant (SGT)'),
            ('specialist', 'Specialist (SPC)'),
            ('private_first_class', 'Private First Class (PFC)'),
        ],
        help_text="Military rank"
    )

    # Organization
    fire_team = models.CharField(
        max_length=20,
        choices=[
            ('hq', 'Squad HQ'),
            ('alpha', 'Alpha Team'),
            ('bravo', 'Bravo Team'),
        ],
        help_text="Fire team assignment"
    )

    role = models.CharField(
        max_length=30,
        choices=[
            ('squad_leader', 'Squad Leader'),
            ('team_leader', 'Team Leader'),
            ('automatic_rifleman', 'Automatic Rifleman'),
            ('grenadier', 'Grenadier'),
            ('rifleman', 'Rifleman'),
        ],
        help_text="Primary role in squad"
    )

    # Secondary duties
    secondary_duty = models.CharField(
        max_length=20,
        blank=True,
        choices=[
            ('', 'None'),
            ('medic', 'Medic'),
            ('engineer', 'Engineer'),
            ('talker', 'Talker (Linguist)'),
        ],
        help_text="Secondary specialty"
    )

    # Primary weapon
    primary_weapon = models.CharField(
        max_length=50,
        choices=[
            ('m4a1', 'M4A1 Carbine'),
            ('m4a1_m320', 'M4A1 with M320 Grenade Launcher'),
            ('m249', 'M249 Light Machine Gun'),
        ],
        help_text="Primary weapon"
    )

    # Health
    health = models.IntegerField(
        default=100,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Current health"
    )

    max_health = models.IntegerField(
        default=100,
        validators=[MinValueValidator(1)],
        help_text="Maximum health"
    )

    is_alive = models.BooleanField(
        default=True,
        help_text="Whether member is alive"
    )

    # Status effects
    is_wounded = models.BooleanField(
        default=False,
        help_text="Has injuries affecting performance"
    )

    is_suppressed = models.BooleanField(
        default=False,
        help_text="Currently suppressed by enemy fire"
    )

    # Stats
    strength = models.IntegerField(
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(20)],
        help_text="Physical power"
    )

    dexterity = models.IntegerField(
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(20)],
        help_text="Agility and accuracy"
    )

    constitution = models.IntegerField(
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(20)],
        help_text="Endurance and toughness"
    )

    intelligence = models.IntegerField(
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(20)],
        help_text="Tactical awareness"
    )

    # Skills (improve through use)
    marksmanship = models.IntegerField(
        default=50,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Shooting accuracy"
    )

    melee_combat = models.IntegerField(
        default=30,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Close quarters combat"
    )

    explosives = models.IntegerField(
        default=20,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Explosives and demolitions"
    )

    medical = models.IntegerField(
        default=10,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Medical treatment"
    )

    engineering = models.IntegerField(
        default=10,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Repairs and fortifications"
    )

    tactics = models.IntegerField(
        default=30,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Tactical decision making"
    )

    # Combat stats
    kills = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Confirmed kills"
    )

    shots_fired = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Total shots fired"
    )

    # Experience
    experience = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Combat experience points"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['fire_team', 'role']
        indexes = [
            models.Index(fields=['squad', 'fire_team']),
            models.Index(fields=['is_alive']),
        ]
        verbose_name = "Squad Member"
        verbose_name_plural = "Squad Members"

    def __str__(self):
        return f"{self.name} ({self.get_role_display()}) - {self.squad.squad_name}"

    @property
    def health_percentage(self):
        """Get health as percentage"""
        return (self.health / self.max_health) * 100 if self.max_health > 0 else 0

    @property
    def rank_display(self):
        """Get abbreviated rank"""
        rank_abbrev = {
            'staff_sergeant': 'SSG',
            'sergeant': 'SGT',
            'specialist': 'SPC',
            'private_first_class': 'PFC',
        }
        return rank_abbrev.get(self.rank, self.rank)

    @property
    def weapon_display(self):
        """Get weapon display name"""
        weapons = {
            'm4a1': 'M4A1 Carbine',
            'm4a1_m320': 'M4A1 w/ M320 GL',
            'm249': 'M249 LMG',
        }
        return weapons.get(self.primary_weapon, self.primary_weapon)

    def take_damage(self, amount):
        """Apply damage to squad member"""
        self.health = max(0, self.health - amount)
        if self.health == 0:
            self.is_alive = False
        elif self.health < self.max_health * 0.5:
            self.is_wounded = True
        self.save(update_fields=['health', 'is_alive', 'is_wounded'])

    def heal(self, amount):
        """Heal squad member"""
        old_health = self.health
        self.health = min(self.health + amount, self.max_health)
        if self.health > self.max_health * 0.5:
            self.is_wounded = False
        self.save(update_fields=['health', 'is_wounded'])
        return self.health - old_health

    def improve_skill(self, skill_name, amount=1):
        """Improve a skill through use"""
        if hasattr(self, skill_name):
            current = getattr(self, skill_name)
            setattr(self, skill_name, min(current + amount, 100))
            self.save(update_fields=[skill_name])
