"""
Test settings for Forgotten Ruin MUD project.

This file imports from the main settings and overrides database and channel settings
for testing. Uses SQLite by default for ease of setup, but can use PostgreSQL
if the USE_POSTGRES_FOR_TESTS environment variable is set.
"""

from .settings import *

# Database configuration for tests
# Use PostgreSQL if available and requested, otherwise use SQLite
if os.environ.get('USE_POSTGRES_FOR_TESTS'):
    # PostgreSQL for testing (handles async tests better)
    import getpass
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('TEST_DB_NAME', 'test_forgotten_ruin'),
            'USER': os.environ.get('DB_USER', getpass.getuser()),  # Use current system user
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '5432'),
            'TEST': {
                'NAME': 'test_forgotten_ruin',
            }
        }
    }
else:
    # SQLite for testing (default - easier setup, but async tests may fail)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
            'ATOMIC_REQUESTS': False,
            'OPTIONS': {
                'timeout': 30,
            },
            'TEST': {
                'NAME': ':memory:',
            }
        }
    }

# Use in-memory channel layer for testing
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

# Keep password validators for proper testing
# (inherited from settings.py)

# Faster password hashing for tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
