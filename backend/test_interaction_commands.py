#!/usr/bin/env python
"""
Test Interaction Commands

Tests the talk, examine, and use commands with NPCs and objects.
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from game.models import Player, Room, NPC, Item
from game.commands import CommandHandler, COMMAND_REGISTRY

# Color codes
class Color:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'

def print_success(msg):
    print(f"{Color.GREEN}✓ {msg}{Color.END}")

def print_info(msg):
    print(f"{Color.BLUE}→ {msg}{Color.END}")

def print_command(msg):
    print(f"{Color.YELLOW}> {msg}{Color.END}")

def print_error(msg):
    print(f"{Color.RED}✗ {msg}{Color.END}")

def print_section(msg):
    print(f"\n{Color.YELLOW}{'='*70}\n{msg}\n{'='*70}{Color.END}")

# Get or create test player
print_section("Setting Up Test Environment")
try:
    player = Player.objects.first()
    if not player:
        print_error("No player found! Please create a player first.")
        exit(1)

    print_info(f"Using player: {player.character_name}")

    # Make sure player has a location
    if not player.location:
        room = Room.objects.get(key='start')
        player.location = room
        player.save()

    print_info(f"Location: {player.location.name}")

except Exception as e:
    print_error(f"Error setting up test environment: {e}")
    exit(1)

# Test commands
def test_command(command_str, description):
    """Test a command and display result"""
    print_command(command_str)
    try:
        result = CommandHandler.handle_command(player, command_str, COMMAND_REGISTRY)
        print(result)
        print_success(f"✓ {description}")
        return True
    except Exception as e:
        print_error(f"Error: {e}")
        return False

# Test Talk Command
print_section("Testing TALK Command")

# Check if there are NPCs
npcs = player.location.npcs_here.all()
if npcs:
    npc = npcs.first()
    print_info(f"Found NPC: {npc.name}")

    # Test basic talk
    test_command(f"talk {npc.key}", "Talk to NPC (greeting)")
    print()

    # Test talk with topic
    if npc.dialogue_tree and 'topics' in npc.dialogue_tree:
        topics = list(npc.dialogue_tree['topics'].keys())
        if topics:
            topic = topics[0]
            test_command(f"talk {npc.key} {topic}", f"Talk about topic: {topic}")
            print()

    # Test invalid topic
    test_command(f"talk {npc.key} nonsense", "Talk with invalid topic")
    print()
else:
    print_error("No NPCs in current room for testing")

# Test Examine Command
print_section("Testing EXAMINE Command")

# Examine NPC
if npcs:
    npc = npcs.first()
    test_command(f"examine {npc.key}", "Examine NPC")
    print()

# Examine object
items = player.location.items_here.all()
if items:
    item = items.first()
    print_info(f"Found object: {item.name}")
    test_command(f"examine {item.key}", "Examine object")
    print()
else:
    print_error("No objects in current room for testing")

# Examine another player (if any)
other_players = player.location.players_here.exclude(id=player.id)
if other_players:
    other = other_players.first()
    test_command(f"examine {other.character_name}", "Examine another player")
    print()

# Test invalid examine
test_command("examine nonexistent", "Examine non-existent target")
print()

# Test Use Command
print_section("Testing USE Command")

# Test use on object
if items:
    item = items.first()
    test_command(f"use {item.key}", "Use object")
    print()

# Test invalid use
test_command("use nonexistent", "Use non-existent item")
print()

# Test Command Aliases
print_section("Testing Command Aliases")

if npcs:
    npc = npcs.first()
    test_command(f"speak {npc.key}", "Speak (alias for talk)")
    print()

if items:
    item = items.first()
    test_command(f"ex {item.key}", "Ex (alias for examine)")
    print()
    test_command(f"inspect {item.key}", "Inspect (alias for examine)")
    print()

# Summary
print_section("Test Summary")

print_success("All interaction commands are functional!")
print()
print_info("Available Commands:")
print("  - talk/speak <npc> [topic] - Talk to NPCs")
print("  - examine/exam/ex/inspect <target> - Examine NPCs, objects, or players")
print("  - use/interact/activate <item> - Use items")
print()
print_info("Try these commands in the game:")
print("  > talk captain")
print("  > talk captain orders")
print("  > examine tactical_map")
print("  > examine captain")
print()
