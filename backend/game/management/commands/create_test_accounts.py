"""
Management command to create test accounts for Forgotten Ruin MUD

This command creates the test accounts listed in TEST_CREDENTIALS.txt
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from game.models import Player, Room

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates test accounts as documented in TEST_CREDENTIALS.txt'

    def add_arguments(self, parser):
        parser.add_argument(
            '--recreate',
            action='store_true',
            help='Delete and recreate existing test accounts',
        )

    def handle(self, *args, **options):
        # Test accounts from TEST_CREDENTIALS.txt
        test_accounts = [
            {'username': 'testuser1', 'email': 'test1@example.com', 'password': 'TestPassword123!'},
            {'username': 'testuser2', 'email': 'test2@example.com', 'password': 'TestPassword123!'},
            {'username': 'testuser3', 'email': 'test3@example.com', 'password': 'TestPassword123!'},
            {'username': 'alice', 'email': 'alice@example.com', 'password': 'TestPassword123!'},
            {'username': 'bob', 'email': 'bob@example.com', 'password': 'TestPassword123!'},
        ]

        # Get starting room for players
        starting_room = Room.objects.filter(key='start').first()

        created_count = 0
        updated_count = 0
        skipped_count = 0

        for account_data in test_accounts:
            username = account_data['username']
            email = account_data['email']
            password = account_data['password']

            # Check if user exists
            existing_user = User.objects.filter(username=username).first()

            if existing_user:
                if options['recreate']:
                    self.stdout.write(f"Deleting existing user: {username}")
                    existing_user.delete()
                else:
                    self.stdout.write(
                        self.style.WARNING(f"User {username} already exists (use --recreate to delete and recreate)")
                    )
                    skipped_count += 1
                    continue

            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # Create player (or get if signal already created it)
            player, player_created = Player.objects.get_or_create(
                user=user,
                defaults={
                    'character_name': username,
                    'location': starting_room,
                    'home': starting_room
                }
            )

            if not player_created:
                # Update player if it was created by signal
                player.character_name = username
                player.location = starting_room
                player.home = starting_room
                player.save()

            created_count += 1
            self.stdout.write(
                self.style.SUCCESS(f"Created user {username} with character {player.character_name}")
            )

        # Summary
        self.stdout.write("\n" + "="*50)
        self.stdout.write(self.style.SUCCESS(f"Created: {created_count} accounts"))
        if skipped_count > 0:
            self.stdout.write(self.style.WARNING(f"Skipped: {skipped_count} accounts (already exist)"))
        self.stdout.write("="*50)
        self.stdout.write("\nAll test accounts use password: TestPassword123!")
        self.stdout.write("See TEST_CREDENTIALS.txt for full details\n")
