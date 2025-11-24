"""
Management command to import development database from portable fixtures

This loads JSON fixtures that were exported from another computer
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
import os
import glob


class Command(BaseCommand):
    help = 'Import development database from portable JSON fixtures'

    def add_arguments(self, parser):
        parser.add_argument(
            '--input-dir',
            type=str,
            default='fixtures',
            help='Directory containing fixtures (default: fixtures/)',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear database before importing (WARNING: deletes all data)',
        )

    def handle(self, *args, **options):
        input_dir = options['input_dir']

        if not os.path.exists(input_dir):
            self.stdout.write(self.style.ERROR(f"Directory not found: {input_dir}"))
            self.stdout.write("\nRun 'python manage.py export_dev_data' first to create fixtures.")
            return

        if options['clear']:
            self.stdout.write(self.style.WARNING("⚠️  WARNING: This will delete all existing data!"))
            confirm = input("Type 'yes' to continue: ")
            if confirm.lower() != 'yes':
                self.stdout.write("Cancelled.")
                return

            self.stdout.write("Flushing database...")
            call_command('flush', '--noinput')

        # Find all JSON fixture files
        fixture_files = sorted(glob.glob(os.path.join(input_dir, '*.json')))

        if not fixture_files:
            self.stdout.write(self.style.ERROR(f"No fixture files found in {input_dir}/"))
            return

        self.stdout.write(self.style.SUCCESS('Importing development data...'))

        # Load fixtures in dependency order
        load_order = [
            'users.json',      # Users first
            'tokens.json',     # Then auth tokens
            'zones.json',      # Then zones
            'rooms.json',      # Then rooms (depends on zones)
            'players.json',    # Then players (depends on users and rooms)
            'npcs.json',       # Then NPCs
            'items.json',      # Then items
            'quests.json',     # Finally quests
        ]

        loaded_count = 0
        for filename in load_order:
            filepath = os.path.join(input_dir, filename)
            if os.path.exists(filepath):
                try:
                    call_command('loaddata', filepath, verbosity=0)
                    self.stdout.write(f"  ✓ Loaded {filename}")
                    loaded_count += 1
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"  ✗ Failed to load {filename}: {e}"))

        # Load any remaining fixtures not in the order list
        for filepath in fixture_files:
            filename = os.path.basename(filepath)
            if filename not in load_order:
                try:
                    call_command('loaddata', filepath, verbosity=0)
                    self.stdout.write(f"  ✓ Loaded {filename}")
                    loaded_count += 1
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"  ⚠ Skipped {filename}: {e}"))

        self.stdout.write("\n" + "="*50)
        self.stdout.write(self.style.SUCCESS(f"✓ Loaded {loaded_count} fixtures from {input_dir}/"))
        self.stdout.write("="*50)
