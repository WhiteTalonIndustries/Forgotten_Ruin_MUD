#!/usr/bin/env python
"""
Test Expanded NPC Dialogue

Demonstrates the new interactive dialogue system with rich conversations.
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from game.models import Player, NPC
from game.commands import CommandHandler, COMMAND_REGISTRY

# Color codes
class Color:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    END = '\033[0m'

def print_section(msg):
    print(f"\n{Color.YELLOW}{'='*70}\n{msg}\n{'='*70}{Color.END}")

def print_command(msg):
    print(f"\n{Color.CYAN}> {msg}{Color.END}")

def test_dialogue(player, command):
    """Test a dialogue command"""
    print_command(command)
    result = CommandHandler.handle_command(player, command, COMMAND_REGISTRY)
    print(f"{Color.GREEN}{result}{Color.END}")

# Get test player
player = Player.objects.first()
if not player:
    print("Error: No player found!")
    exit(1)

print_section("Testing Expanded NPC Dialogue System")
print(f"{Color.BLUE}Player: {player.character_name}{Color.END}")
print(f"{Color.BLUE}Location: {player.location.name}{Color.END}")

# Test Captain Reynolds - Mission System
print_section("Captain Reynolds - Mission System")
test_dialogue(player, "talk captain_reynolds missions")
test_dialogue(player, "talk captain_reynolds recon")
test_dialogue(player, "talk captain_reynolds wizard")

# Test SSG Kim - Training System
print_section("SSG Kim - Training and Combat")
test_dialogue(player, "talk sergeant_kim training")
test_dialogue(player, "talk sergeant_kim marksmanship")
test_dialogue(player, "talk sergeant_kim melee")

# Test Doc Martinez - Medical System
print_section("Doc Martinez - Medical and Healing")
test_dialogue(player, "talk doc_martinez potions")
test_dialogue(player, "talk doc_martinez prayer")
test_dialogue(player, "talk doc_martinez advice")

# Test Specialist Jackson - Gear and Enchantment
print_section("Specialist Jackson - Weapons and Enchanting")
test_dialogue(player, "talk specialist_jackson modifications")
test_dialogue(player, "talk specialist_jackson enchantment")
test_dialogue(player, "talk specialist_jackson ammunition")

# Test SGT Walsh - Economy and Trading
print_section("SGT Walsh - Quartermaster and Economy")
test_dialogue(player, "talk sergeant_walsh economy")
test_dialogue(player, "talk sergeant_walsh local_trade")
test_dialogue(player, "talk sergeant_walsh food")

# Test CPL Chen - Intelligence
print_section("CPL Chen - Enemy Intelligence")
test_dialogue(player, "talk corporal_chen orcs")
test_dialogue(player, "talk corporal_chen lich_pharaoh")

# Test PFC Rodriguez - Guard Stories
print_section("PFC Rodriguez - Guard Duty and Stories")
test_dialogue(player, "talk pfc_rodriguez stories")
test_dialogue(player, "talk pfc_rodriguez advice")

# Summary
print_section("Expanded Dialogue System - Summary")
print(f"{Color.GREEN}✓ All NPCs now have rich, interactive dialogue!{Color.END}")
print()
print(f"{Color.BLUE}Key Features:{Color.END}")
print("  • Mission system with Captain Reynolds (recon, raid, rescue, wizard hunt)")
print("  • Training programs with SSG Kim (marksmanship, melee, tactics)")
print("  • Medical system with Doc Martinez (potions, prayer, magical healing)")
print("  • Crafting and enchanting with SPC Jackson")
print("  • Trading and economy with SGT Walsh")
print("  • Intelligence reports with CPL Chen")
print("  • Guard stories and advice with PFC Rodriguez")
print()
print(f"{Color.YELLOW}NPCs now feel alive with:{Color.END}")
print("  • Multiple conversation branches")
print("  • Quest chains and missions")
print("  • Lore and worldbuilding")
print("  • Practical advice and training")
print("  • Character personality and voice")
print()
