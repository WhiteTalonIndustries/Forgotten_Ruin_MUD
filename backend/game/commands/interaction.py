"""
Interaction Commands

Commands for interacting with NPCs and objects in the world.
"""
from .base import Command
from django.utils.html import escape


class TalkCommand(Command):
    """Talk to an NPC"""
    key = "talk"
    aliases = ["speak", "chat"]
    help_text = "Talk to an NPC. Usage: talk <npc> or talk <npc> <topic>"
    category = "Interaction"

    def execute(self, player, **kwargs):
        """Execute talk command"""
        args = kwargs.get('args', '').strip()

        if not args:
            return "Talk to whom? Usage: talk <npc> or talk <npc> <topic>"

        if not player.location:
            return "You are nowhere."

        # Parse target and optional topic
        parts = args.split(maxsplit=1)
        target_name = parts[0].lower()
        topic = parts[1].lower() if len(parts) > 1 else None

        # Find NPC in room
        npc = None
        for room_npc in player.location.npcs_here.all():
            if (target_name in room_npc.name.lower() or
                target_name in room_npc.key.lower()):
                npc = room_npc
                break

        if not npc:
            return f"There is no '{target_name}' here to talk to."

        # Check if NPC is alive
        if not npc.is_alive:
            return f"{npc.name} is dead and cannot speak."

        # Get dialogue tree
        dialogue = npc.dialogue_tree or {}

        # If no topic specified, show greeting and available topics
        if not topic:
            greeting = dialogue.get('greeting', npc.greeting_message)

            output = [f"\n{npc.name}:"]
            output.append(f'"{greeting}"')

            # Show available topics
            topics = dialogue.get('topics', {})
            if topics:
                output.append("\nYou can ask about:")
                for topic_key in topics.keys():
                    output.append(f"  - {topic_key}")
                output.append("\nUsage: talk <npc> <topic>")

            return "\n".join(output)

        # Look up topic response
        topics = dialogue.get('topics', {})

        # Try exact match first
        response = topics.get(topic)

        # Try partial match if exact fails
        if not response:
            for topic_key, topic_response in topics.items():
                if topic in topic_key or topic_key in topic:
                    response = topic_response
                    break

        if not response:
            available = ", ".join(topics.keys())
            return (f"\n{npc.name} doesn't know about '{topic}'.\n"
                   f"Try asking about: {available}")

        output = [f"\n{npc.name}:"]
        output.append(f'"{response}"')

        return "\n".join(output)


class ExamineCommand(Command):
    """Examine an object or NPC in detail"""
    key = "examine"
    aliases = ["exam", "ex", "inspect", "look at"]
    help_text = "Examine something in detail. Usage: examine <target>"
    category = "Interaction"

    def execute(self, player, **kwargs):
        """Execute examine command"""
        args = kwargs.get('args', '').strip()

        if not args:
            return "Examine what? Usage: examine <target>"

        if not player.location:
            return "You are nowhere."

        target_name = args.lower()
        room = player.location

        # Check NPCs
        for npc in room.npcs_here.all():
            if (target_name in npc.name.lower() or
                target_name in npc.key.lower()):
                return self._examine_npc(npc)

        # Check items in room
        for item in room.items_here.all():
            if (target_name in item.name.lower() or
                target_name in item.key.lower()):
                return self._examine_item(item)

        # Check players (if looking at another player)
        for other_player in room.players_here.exclude(id=player.id):
            if target_name in other_player.character_name.lower():
                return self._examine_player(other_player)

        return f"You don't see '{args}' here."

    def _examine_npc(self, npc):
        """Format NPC examination"""
        output = [f"\n{'='*60}"]
        output.append(f"{npc.name}")
        output.append('='*60)

        output.append(npc.description)

        # Status
        if not npc.is_alive:
            output.append("\n[STATUS: DECEASED]")
        elif npc.health < npc.max_health:
            health_pct = (npc.health / npc.max_health * 100)
            output.append(f"\n[Health: {health_pct:.0f}%]")

        # AI type hints
        ai_hints = {
            'merchant': "\n[This NPC buys and sells items]",
            'trainer': "\n[This NPC can train your skills]",
            'quest_giver': "\n[This NPC may have missions for you]",
            'guard': "\n[This guard watches for threats]",
        }
        if npc.ai_type in ai_hints:
            output.append(ai_hints[npc.ai_type])

        # Interaction hint
        if npc.is_alive and npc.dialogue_tree:
            output.append("\nUse 'talk " + npc.key + "' to speak with them.")

        output.append('='*60)
        return "\n".join(output)

    def _examine_item(self, item):
        """Format item examination"""
        output = [f"\n{'='*60}"]
        output.append(f"{item.name}")
        output.append('='*60)

        output.append(item.description)

        # Check for examine message in effect field
        if item.effect and isinstance(item.effect, dict):
            examine_msg = item.effect.get('examine_message')
            if examine_msg:
                output.append(f"\n{examine_msg}")

        # Item properties
        details = []

        if item.item_type != 'misc':
            details.append(f"Type: {item.get_item_type_display()}")

        if item.weight > 0:
            details.append(f"Weight: {item.weight}")

        if item.value > 0:
            details.append(f"Value: {item.value} gold")

        if not item.is_takeable:
            details.append("[This object is fixed in place]")

        if item.is_quest_item:
            details.append("[Quest Item]")

        if details:
            output.append("\n" + " | ".join(details))

        output.append('='*60)
        return "\n".join(output)

    def _examine_player(self, other_player):
        """Format player examination"""
        output = [f"\n{'='*60}"]
        output.append(f"{other_player.character_name}")
        output.append('='*60)

        output.append(other_player.description or "A fellow adventurer.")

        output.append(f"\nLevel: {other_player.level}")

        # Health status
        health_pct = (other_player.health / other_player.max_health * 100) if other_player.max_health > 0 else 0
        if health_pct > 75:
            status = "in excellent condition"
        elif health_pct > 50:
            status = "slightly wounded"
        elif health_pct > 25:
            status = "wounded"
        else:
            status = "badly wounded"

        output.append(f"They appear to be {status}.")

        output.append('='*60)
        return "\n".join(output)


class UseCommand(Command):
    """Use an item or interact with an object"""
    key = "use"
    aliases = ["interact", "activate"]
    help_text = "Use an item or interact with an object. Usage: use <item>"
    category = "Interaction"

    def execute(self, player, **kwargs):
        """Execute use command"""
        args = kwargs.get('args', '').strip()

        if not args:
            return "Use what? Usage: use <item>"

        target_name = args.lower()

        # Check inventory first
        for item in player.items.all():
            if target_name in item.name.lower() or target_name in item.key.lower():
                return self._use_item(player, item)

        # Check items in room
        if player.location:
            for item in player.location.items_here.all():
                if target_name in item.name.lower() or target_name in item.key.lower():
                    return self._use_item(player, item)

        return f"You don't have or see '{args}'."

    def _use_item(self, player, item):
        """Use an item"""
        # Check if item is usable
        if item.item_type == 'consumable':
            return self._consume_item(player, item)
        elif item.item_type == 'tool':
            return f"You use the {item.name}. (Tool functionality not yet implemented)"
        elif not item.is_takeable:
            # Interactive object
            return f"You interact with the {item.name}. (Interactive object functionality not yet implemented)"
        else:
            return f"You're not sure how to use the {item.name}."

    def _consume_item(self, player, item):
        """Consume a consumable item"""
        if item.uses_remaining is not None and item.uses_remaining <= 0:
            return f"The {item.name} is depleted."

        # Apply effect
        if item.effect and isinstance(item.effect, dict):
            effect_type = item.effect.get('type')
            amount = item.effect.get('amount', 0)

            if effect_type == 'heal':
                old_health = player.health
                player.heal(amount)
                healed = player.health - old_health

                # Reduce uses
                if item.uses_remaining is not None:
                    item.uses_remaining -= 1
                    if item.uses_remaining <= 0:
                        item.delete()
                        return f"You use the {item.name} and restore {healed} health. The {item.name} is now depleted."
                    else:
                        item.save()

                return f"You use the {item.name} and restore {healed} health."

            elif effect_type == 'mana':
                old_mana = player.mana
                player.restore_mana(amount)
                restored = player.mana - old_mana

                # Reduce uses
                if item.uses_remaining is not None:
                    item.uses_remaining -= 1
                    if item.uses_remaining <= 0:
                        item.delete()
                        return f"You use the {item.name} and restore {restored} mana. The {item.name} is now depleted."
                    else:
                        item.save()

                return f"You use the {item.name} and restore {restored} mana."

        return f"You use the {item.name}, but nothing happens."
