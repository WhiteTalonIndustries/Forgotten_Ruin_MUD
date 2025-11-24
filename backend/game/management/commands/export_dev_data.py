"""
Management command to export development database to portable fixtures

This creates JSON fixtures that can be loaded on any computer
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
import os
from datetime import datetime


class Command(BaseCommand):
    help = 'Export development database to portable JSON fixtures'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output-dir',
            type=str,
            default='fixtures',
            help='Directory to save fixtures (default: fixtures/)',
        )

    def handle(self, *args, **options):
        output_dir = options['output_dir']

        # Create fixtures directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # List of apps and models to export
        exports = [
            ('auth.User', 'users.json'),
            ('authtoken.Token', 'tokens.json'),
            ('game.Zone', 'zones.json'),
            ('game.Room', 'rooms.json'),
            ('game.Player', 'players.json'),
            ('game.NPC', 'npcs.json'),
            ('game.Item', 'items.json'),
            ('game.Quest', 'quests.json'),
        ]

        self.stdout.write(self.style.SUCCESS('Exporting development data...'))

        exported_files = []

        for model_name, filename in exports:
            filepath = os.path.join(output_dir, filename)

            try:
                with open(filepath, 'w') as f:
                    call_command('dumpdata', model_name, indent=2, stdout=f)

                # Check if file has data (more than just [])
                with open(filepath, 'r') as f:
                    content = f.read().strip()
                    if content and content != '[]':
                        self.stdout.write(f"  ✓ Exported {model_name} → {filepath}")
                        exported_files.append(filepath)
                    else:
                        self.stdout.write(self.style.WARNING(f"  ⚠ Skipped {model_name} (no data)"))
                        os.remove(filepath)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ✗ Failed to export {model_name}: {e}"))

        # Create a README with timestamp
        readme_path = os.path.join(output_dir, 'README.md')
        with open(readme_path, 'w') as f:
            f.write(f"""# Development Database Fixtures

Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Files

""")
            for filepath in exported_files:
                f.write(f"- {os.path.basename(filepath)}\n")

            f.write(f"""
## Loading These Fixtures

To load this data on another computer:

1. Make sure migrations are up to date:
   ```bash
   python manage.py migrate
   ```

2. Load all fixtures:
   ```bash
   python manage.py import_dev_data
   ```

Or load specific fixtures:
   ```bash
   python manage.py loaddata fixtures/users.json
   python manage.py loaddata fixtures/zones.json
   python manage.py loaddata fixtures/rooms.json
   python manage.py loaddata fixtures/players.json
   ```

## Notes

- These fixtures include test accounts and basic game data
- Production database is separate and not portable
- Generated with: `python manage.py export_dev_data`
""")

        self.stdout.write("\n" + "="*50)
        self.stdout.write(self.style.SUCCESS(f"✓ Exported {len(exported_files)} fixtures to {output_dir}/"))
        self.stdout.write(f"✓ Created {readme_path}")
        self.stdout.write("="*50)
        self.stdout.write(f"\nTo load on another computer:")
        self.stdout.write(f"  python manage.py import_dev_data --input-dir {output_dir}")
