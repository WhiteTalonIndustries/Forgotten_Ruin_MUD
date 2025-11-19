"""
Combat Commands

Commands for combat actions.
"""
from .base import Command


class AttackCommand(Command):
    """Attack a target"""
    key = "attack"
    aliases = ["kill", "fight"]
    help_text = "Attack a target"
    category = "Combat"

    def execute(self, player, **kwargs):
        """Execute attack command"""
        target_name = kwargs.get('args', '').strip()

        if not target_name:
            return "Attack whom?"

        if not player.location:
            return "You are nowhere."

        if player.position == 'dead':
            return "You are dead and cannot attack."

        if player.location.is_safe:
            return "You cannot attack here. This is a safe zone."

        # Find target NPC
        target = player.location.npcs_here.filter(
            name__iexact=target_name,
            is_alive=True
        ).first()

        if not target:
            return f"You don't see '{target_name}' here."

        if not target.is_attackable:
            return f"You cannot attack {target.name}."

        # TODO: Initiate combat
        # For now, simple damage calculation
        import random
        damage = random.randint(1, 10) + player.strength

        target.take_damage(damage)

        # Broadcast
        player.location.broadcast(
            f"{player.character_name} attacks {target.name} for {damage} damage!",
            exclude=player
        )

        result = f"You attack {target.name} for {damage} damage!"

        if target.health == 0:
            result += f"\nYou have slain {target.name}!"
            player.gain_experience(target.experience_reward)

        return result
