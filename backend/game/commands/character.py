"""
Character Commands

Commands for viewing and managing character information.
"""
from .base import Command


class CharacterSheetCommand(Command):
    """Display character sheet and squad information"""
    key = "sheet"
    aliases = ["char", "character", "squad"]
    help_text = "Display your character sheet and squad roster"
    category = "Character"

    def execute(self, player, **kwargs):
        """Execute character sheet command"""
        args = kwargs.get('args', '').strip().lower()

        if not hasattr(player, 'squad'):
            return "You don't have a squad yet. Contact an administrator."

        squad = player.squad

        # Choose what to display
        if args == 'stats':
            return self.display_squad_stats(squad)
        elif args == 'alpha':
            return self.display_fire_team(squad, 'alpha')
        elif args == 'bravo':
            return self.display_fire_team(squad, 'bravo')
        elif args == 'supplies':
            return self.display_supplies(squad)
        else:
            return self.display_full_sheet(player, squad)

    def display_full_sheet(self, player, squad):
        """Display complete character sheet"""
        output = []

        # Header
        output.append("=" * 70)
        output.append(f"  RANGER SQUAD - {squad.squad_name.upper()}")
        output.append(f"  Callsign: {squad.callsign} | Commander: {player.character_name}")
        output.append("=" * 70)

        # Squad Status
        alive = squad.alive_members.count()
        total = squad.members.count()
        casualties = squad.casualty_count

        output.append(f"\nSquad Status:")
        output.append(f"  Personnel: {alive}/{total} alive ({casualties} casualties)")
        output.append(f"  Morale: {squad.morale}/100")
        output.append(f"  Cohesion: {squad.cohesion}/100")
        output.append(f"  Average Health: {squad.average_health:.0f}%")

        # Squad Leader (HQ)
        leader = squad.squad_leader
        if leader:
            output.append(f"\n{'─' * 70}")
            output.append(f"SQUAD HQ")
            output.append(f"{'─' * 70}")
            output.append(self.format_member(leader))

        # Alpha Team
        output.append(f"\n{'─' * 70}")
        output.append(f"ALPHA TEAM")
        output.append(f"{'─' * 70}")
        for member in squad.alpha_team:
            output.append(self.format_member(member))

        # Bravo Team
        output.append(f"\n{'─' * 70}")
        output.append(f"BRAVO TEAM")
        output.append(f"{'─' * 70}")
        for member in squad.bravo_team:
            output.append(self.format_member(member))

        # Combat Record
        output.append(f"\n{'─' * 70}")
        output.append(f"COMBAT RECORD")
        output.append(f"{'─' * 70}")
        output.append(f"  Total Kills: {squad.total_kills}")
        output.append(f"  Missions Completed: {squad.missions_completed}")

        # Commands
        output.append(f"\n{'─' * 70}")
        output.append("Commands:")
        output.append("  sheet stats     - View detailed squad statistics")
        output.append("  sheet alpha     - View Alpha Team details")
        output.append("  sheet bravo     - View Bravo Team details")
        output.append("  sheet supplies  - View ammunition and supplies")
        output.append("=" * 70)

        return "\n".join(output)

    def format_member(self, member):
        """Format a squad member for display"""
        # Health bar
        health_pct = member.health_percentage
        bar_length = 10
        filled = int((health_pct / 100) * bar_length)
        health_bar = "█" * filled + "░" * (bar_length - filled)

        # Status indicators
        status = ""
        if not member.is_alive:
            status = "[KIA]"
            health_bar = "✝" * bar_length
        elif member.is_wounded:
            status = "[WOUNDED]"
        elif member.is_suppressed:
            status = "[SUPPRESSED]"

        # Secondary duty
        duty = f" - {member.get_secondary_duty_display()}" if member.secondary_duty else ""

        return (
            f"  {member.name:<25} {member.weapon_display:<18} "
            f"{health_bar} {health_pct:>3.0f}% {status}{duty}"
        )

    def display_fire_team(self, squad, team):
        """Display detailed fire team information"""
        output = []

        team_name = team.capitalize()
        members = squad.alpha_team if team == 'alpha' else squad.bravo_team

        output.append(f"\n{'=' * 70}")
        output.append(f"  {team_name.upper()} TEAM - {squad.squad_name}")
        output.append(f"{'=' * 70}")

        for member in members:
            output.append(f"\n{member.name} - {member.get_role_display()}")
            output.append(f"{'─' * 70}")
            output.append(f"  Rank: {member.rank_display}")
            output.append(f"  Primary Weapon: {member.weapon_display}")
            if member.secondary_duty:
                output.append(f"  Secondary Duty: {member.get_secondary_duty_display()}")

            # Health
            status = "Alive" if member.is_alive else "KIA"
            if member.is_wounded:
                status += " (Wounded)"
            output.append(f"  Health: {member.health}/{member.max_health} ({member.health_percentage:.0f}%) - {status}")

            # Stats
            output.append(f"\n  Combat Stats:")
            output.append(f"    STR: {member.strength:<2}  DEX: {member.dexterity:<2}  "
                         f"CON: {member.constitution:<2}  INT: {member.intelligence:<2}")

            # Skills
            output.append(f"\n  Skills:")
            output.append(f"    Marksmanship: {member.marksmanship}/100  "
                         f"Melee: {member.melee_combat}/100  "
                         f"Tactics: {member.tactics}/100")
            output.append(f"    Medical: {member.medical}/100  "
                         f"Engineering: {member.engineering}/100  "
                         f"Explosives: {member.explosives}/100")

            # Combat record
            accuracy = (member.kills / member.shots_fired * 100) if member.shots_fired > 0 else 0
            output.append(f"\n  Combat Record:")
            output.append(f"    Kills: {member.kills}")
            output.append(f"    Shots Fired: {member.shots_fired}")
            output.append(f"    Accuracy: {accuracy:.1f}%")
            output.append(f"    Experience: {member.experience} XP")

        output.append(f"\n{'=' * 70}")
        return "\n".join(output)

    def display_supplies(self, squad):
        """Display ammunition and supply status"""
        output = []

        output.append(f"\n{'=' * 70}")
        output.append(f"  AMMUNITION & SUPPLIES - {squad.squad_name}")
        output.append(f"{'=' * 70}")

        output.append(f"\nAmmunition:")
        output.append(f"  5.56mm (M4A1):     {squad.ammunition_556mm:>5} rounds")
        output.append(f"  5.56mm Belt (M249): {squad.ammunition_556mm_belt:>5} rounds")
        output.append(f"  Frag Grenades:      {squad.grenades_frag:>5}")
        output.append(f"  40mm Grenades:      {squad.grenades_40mm:>5}")

        output.append(f"\nMedical Supplies:")
        output.append(f"  First Aid Kits:     {squad.medkits:>5}")

        # Calculate ammo per weapon
        m4_count = squad.members.filter(primary_weapon__in=['m4a1', 'm4a1_m320']).count()
        m249_count = squad.members.filter(primary_weapon='m249').count()

        if m4_count > 0:
            ammo_per_m4 = squad.ammunition_556mm // m4_count
            output.append(f"\nRounds per M4A1: {ammo_per_m4} (~{ammo_per_m4 // 30} magazines)")

        if m249_count > 0:
            ammo_per_m249 = squad.ammunition_556mm_belt // m249_count
            output.append(f"Rounds per M249: {ammo_per_m249}")

        # Warning levels
        output.append(f"\nSupply Status:")
        warnings = []
        if squad.ammunition_556mm < 300:
            warnings.append("⚠ Low on 5.56mm ammunition")
        if squad.ammunition_556mm_belt < 200:
            warnings.append("⚠ Low on M249 ammunition")
        if squad.medkits < 3:
            warnings.append("⚠ Low on medical supplies")

        if warnings:
            for warning in warnings:
                output.append(f"  {warning}")
        else:
            output.append("  ✓ All supplies adequate")

        output.append(f"\n{'=' * 70}")
        return "\n".join(output)

    def display_squad_stats(self, squad):
        """Display aggregate squad statistics"""
        output = []

        output.append(f"\n{'=' * 70}")
        output.append(f"  SQUAD STATISTICS - {squad.squad_name}")
        output.append(f"{'=' * 70}")

        # Personnel breakdown
        alive = squad.alive_members
        total = squad.members.count()

        output.append(f"\nPersonnel Status:")
        output.append(f"  Total: {total}")
        output.append(f"  Alive: {alive.count()}")
        output.append(f"  KIA: {squad.casualty_count}")
        output.append(f"  Wounded: {alive.filter(is_wounded=True).count()}")

        # Role breakdown
        output.append(f"\nRoles:")
        output.append(f"  Squad Leader: {squad.members.filter(role='squad_leader').count()}")
        output.append(f"  Team Leaders: {squad.members.filter(role='team_leader').count()}")
        output.append(f"  Automatic Riflemen: {squad.members.filter(role='automatic_rifleman').count()}")
        output.append(f"  Grenadiers: {squad.members.filter(role='grenadier').count()}")
        output.append(f"  Riflemen: {squad.members.filter(role='rifleman').count()}")

        # Secondary duties
        output.append(f"\nSecondary Duties:")
        output.append(f"  Medics: {squad.members.filter(secondary_duty='medic').count()}")
        output.append(f"  Engineers: {squad.members.filter(secondary_duty='engineer').count()}")
        output.append(f"  Talkers: {squad.members.filter(secondary_duty='talker').count()}")

        # Combat statistics
        total_kills = sum(m.kills for m in alive)
        total_shots = sum(m.shots_fired for m in alive)
        avg_accuracy = (total_kills / total_shots * 100) if total_shots > 0 else 0

        output.append(f"\nCombat Performance:")
        output.append(f"  Total Kills: {squad.total_kills}")
        output.append(f"  Squad Accuracy: {avg_accuracy:.1f}%")
        output.append(f"  Missions: {squad.missions_completed}")
        output.append(f"  Morale: {squad.morale}/100")
        output.append(f"  Cohesion: {squad.cohesion}/100")

        # Average skills
        if alive.count() > 0:
            avg_marksmanship = sum(m.marksmanship for m in alive) / alive.count()
            avg_melee = sum(m.melee_combat for m in alive) / alive.count()
            avg_tactics = sum(m.tactics for m in alive) / alive.count()

            output.append(f"\nAverage Skills:")
            output.append(f"  Marksmanship: {avg_marksmanship:.1f}/100")
            output.append(f"  Melee Combat: {avg_melee:.1f}/100")
            output.append(f"  Tactics: {avg_tactics:.1f}/100")

        output.append(f"\n{'=' * 70}")
        return "\n".join(output)
