"""
Generate Test Data Script

Creates test users, players, rooms, and zones for manual and automated testing.

Usage:
    python manage.py shell < tests/generate_test_data.py

Or from Django shell:
    from tests.generate_test_data import generate_all_test_data
    generate_all_test_data()
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from django.contrib.auth import get_user_model
from game.models import Player, Room, Zone, Exit

User = get_user_model()


def generate_test_users():
    """Generate test user accounts"""
    print("Creating test users...")

    test_users = [
        {'username': 'testuser1', 'email': 'test1@example.com', 'password': 'TestPassword123!'},
        {'username': 'testuser2', 'email': 'test2@example.com', 'password': 'TestPassword123!'},
        {'username': 'testuser3', 'email': 'test3@example.com', 'password': 'TestPassword123!'},
        {'username': 'alice', 'email': 'alice@example.com', 'password': 'TestPassword123!'},
        {'username': 'bob', 'email': 'bob@example.com', 'password': 'TestPassword123!'},
    ]

    created_users = []
    for user_data in test_users:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email']
            }
        )
        if created:
            user.set_password(user_data['password'])
            user.save()
            print(f"  ✓ Created user: {user.username}")
        else:
            print(f"  - User already exists: {user.username}")

        created_users.append(user)

    return created_users


def generate_test_zones():
    """Generate test zones"""
    print("\nCreating test zones...")

    test_zones = [
        {'key': 'newbie_zone', 'name': 'Newbie Zone', 'description': 'A safe area for new players to learn the game.'},
        {'key': 'forest', 'name': 'Dark Forest', 'description': 'A mysterious forest full of danger.'},
        {'key': 'town', 'name': 'Riverside Town', 'description': 'A bustling town with shops and taverns.'},
    ]

    created_zones = []
    for zone_data in test_zones:
        zone, created = Zone.objects.get_or_create(
            key=zone_data['key'],
            defaults={
                'name': zone_data['name'],
                'description': zone_data['description']
            }
        )
        if created:
            print(f"  ✓ Created zone: {zone.name}")
        else:
            print(f"  - Zone already exists: {zone.name}")

        created_zones.append(zone)

    return created_zones


def generate_test_rooms(zones):
    """Generate test rooms"""
    print("\nCreating test rooms...")

    newbie_zone = zones[0]
    forest_zone = zones[1]
    town_zone = zones[2]

    test_rooms = [
        {
            'key': 'start',
            'name': 'Starting Room',
            'description': 'You are in a small clearing. This is where all new adventurers begin their journey.',
            'zone': newbie_zone,
            'is_safe': True
        },
        {
            'key': 'training_grounds',
            'name': 'Training Grounds',
            'description': 'A large open area with training dummies and practice weapons.',
            'zone': newbie_zone,
            'is_safe': True
        },
        {
            'key': 'forest_entrance',
            'name': 'Forest Entrance',
            'description': 'The edge of a dark and foreboding forest.',
            'zone': forest_zone,
            'is_safe': False
        },
        {
            'key': 'deep_forest',
            'name': 'Deep in the Forest',
            'description': 'You are surrounded by tall trees. Strange sounds echo around you.',
            'zone': forest_zone,
            'is_safe': False,
            'is_dark': True
        },
        {
            'key': 'town_square',
            'name': 'Town Square',
            'description': 'The bustling center of Riverside Town. People go about their daily business.',
            'zone': town_zone,
            'is_safe': True
        },
        {
            'key': 'tavern',
            'name': 'The Rusty Anchor Tavern',
            'description': 'A cozy tavern filled with the smell of ale and roasted meat.',
            'zone': town_zone,
            'is_safe': True,
            'is_indoors': True
        },
    ]

    created_rooms = []
    for room_data in test_rooms:
        room, created = Room.objects.get_or_create(
            key=room_data['key'],
            defaults=room_data
        )
        if created:
            print(f"  ✓ Created room: {room.name}")
        else:
            print(f"  - Room already exists: {room.name}")

        created_rooms.append(room)

    return created_rooms


def generate_test_exits(rooms):
    """Generate exits between rooms"""
    print("\nCreating exits between rooms...")

    # Helper function to get room by key
    room_dict = {room.key: room for room in rooms}

    exits_data = [
        # Newbie zone connections
        ('start', 'training_grounds', 'north', 'south'),
        ('training_grounds', 'forest_entrance', 'east', 'west'),
        ('training_grounds', 'town_square', 'west', 'east'),

        # Forest connections
        ('forest_entrance', 'deep_forest', 'north', 'south'),

        # Town connections
        ('town_square', 'tavern', 'north', 'south'),
    ]

    created_exits = []
    for source_key, dest_key, direction, reverse_direction in exits_data:
        if source_key not in room_dict or dest_key not in room_dict:
            print(f"  ! Skipping exit: {source_key} -> {dest_key} (room not found)")
            continue

        # Create exit in one direction
        exit_forward, created = Exit.objects.get_or_create(
            source=room_dict[source_key],
            destination=room_dict[dest_key],
            direction=direction,
            defaults={'name': direction}
        )
        if created:
            print(f"  ✓ Created exit: {source_key} -> {dest_key} ({direction})")

        # Create exit in reverse direction
        exit_backward, created = Exit.objects.get_or_create(
            source=room_dict[dest_key],
            destination=room_dict[source_key],
            direction=reverse_direction,
            defaults={'name': reverse_direction}
        )
        if created:
            print(f"  ✓ Created exit: {dest_key} -> {source_key} ({reverse_direction})")

        created_exits.extend([exit_forward, exit_backward])

    return created_exits


def generate_test_players(users, start_room):
    """Generate player characters for test users"""
    print("\nCreating test players...")

    created_players = []
    for user in users:
        # Check if player already exists
        if hasattr(user, 'player'):
            print(f"  - Player already exists for user: {user.username}")
            created_players.append(user.player)
            continue

        # Create player
        player = Player.objects.create(
            user=user,
            character_name=user.username.capitalize(),
            location=start_room,
            home=start_room
        )
        print(f"  ✓ Created player: {player.character_name}")
        created_players.append(player)

    return created_players


def clean_test_data():
    """Remove all test data (use with caution!)"""
    print("\n⚠️  CLEANING TEST DATA ⚠️")
    confirm = input("Are you sure you want to delete all test data? (yes/no): ")

    if confirm.lower() != 'yes':
        print("Cancelled.")
        return

    print("Deleting test players...")
    Player.objects.filter(user__username__startswith='test').delete()
    Player.objects.filter(user__username__in=['alice', 'bob']).delete()

    print("Deleting test users...")
    User.objects.filter(username__startswith='test').delete()
    User.objects.filter(username__in=['alice', 'bob']).delete()

    print("Deleting test exits...")
    Exit.objects.all().delete()

    print("Deleting test rooms...")
    Room.objects.all().delete()

    print("Deleting test zones...")
    Zone.objects.all().delete()

    print("✓ Test data cleaned!")


def generate_all_test_data():
    """Generate complete test dataset"""
    print("=" * 60)
    print("GENERATING TEST DATA FOR FORGOTTEN RUIN MUD")
    print("=" * 60)

    # Generate in order (respecting dependencies)
    users = generate_test_users()
    zones = generate_test_zones()
    rooms = generate_test_rooms(zones)
    exits = generate_test_exits(rooms)

    # Get starting room
    start_room = Room.objects.get(key='start')
    players = generate_test_players(users, start_room)

    print("\n" + "=" * 60)
    print("TEST DATA GENERATION COMPLETE!")
    print("=" * 60)
    print(f"\nCreated:")
    print(f"  - {len(users)} users")
    print(f"  - {len(zones)} zones")
    print(f"  - {len(rooms)} rooms")
    print(f"  - {len(exits)} exits")
    print(f"  - {len(players)} players")

    print("\nTest Accounts:")
    print("  Username: testuser1 | Password: TestPassword123!")
    print("  Username: testuser2 | Password: TestPassword123!")
    print("  Username: testuser3 | Password: TestPassword123!")
    print("  Username: alice     | Password: TestPassword123!")
    print("  Username: bob       | Password: TestPassword123!")

    print("\nYou can now:")
    print("  1. Run automated tests: pytest")
    print("  2. Login to the game with test accounts")
    print("  3. Test chat commands between users")

    return {
        'users': users,
        'zones': zones,
        'rooms': rooms,
        'exits': exits,
        'players': players
    }


if __name__ == '__main__':
    # Run when executed directly
    generate_all_test_data()
