# Security Best Practices for Web-Based MUDs

## Overview
Security is critical for protecting both the web host infrastructure and individual user data. This document outlines comprehensive security measures for a web-based MUD implementation.

## Authentication & Authorization

### 1. User Authentication

#### Password Security
```python
# Django settings.py
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',  # Recommended
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
]

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 12}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

**Best Practices:**
- Use Argon2 or PBKDF2 for password hashing
- Minimum password length: 12 characters
- Require mix of uppercase, lowercase, numbers, symbols
- Check against common password databases
- Enforce password rotation for admin accounts
- Never store passwords in plain text or reversible encryption

#### Multi-Factor Authentication (MFA)
```python
# Using django-otp
from django_otp.decorators import otp_required

@otp_required
def admin_panel(request):
    # Only accessible with 2FA
    pass
```

**Recommendations:**
- Require MFA for admin/staff accounts
- Optional MFA for regular players
- Support TOTP (Time-based One-Time Password)
- Backup recovery codes

#### Token-Based Authentication
```python
# JWT implementation
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),  # Short-lived
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}
```

**Best Practices:**
- Use short-lived access tokens (15-30 minutes)
- Implement refresh token rotation
- Blacklist tokens on logout
- Store tokens securely on client (httpOnly cookies preferred)

### 2. Session Management

```python
# Django settings.py
SESSION_COOKIE_SECURE = True  # HTTPS only
SESSION_COOKIE_HTTPONLY = True  # No JavaScript access
SESSION_COOKIE_SAMESITE = 'Strict'  # CSRF protection
SESSION_COOKIE_AGE = 3600  # 1 hour
SESSION_SAVE_EVERY_REQUEST = True  # Refresh on activity

# Session timeout on inactivity
MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
]

SESSION_EXPIRE_SECONDS = 1800  # 30 minutes
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
```

**Best Practices:**
- Force session renewal after login
- Implement idle timeout
- Regenerate session ID on privilege escalation
- Clear sessions on logout
- Monitor for session hijacking attempts

### 3. Authorization & Access Control

```python
# Role-based access control (RBAC)
from django.contrib.auth.models import Group, Permission

# Define roles
admin_group = Group.objects.create(name='Admin')
moderator_group = Group.objects.create(name='Moderator')
player_group = Group.objects.create(name='Player')

# Assign permissions
can_ban_users = Permission.objects.get(codename='ban_user')
moderator_group.permissions.add(can_ban_users)

# Check permissions
from django.contrib.auth.decorators import permission_required

@permission_required('game.ban_user', raise_exception=True)
def ban_player(request, player_id):
    # Only users with ban_user permission can access
    pass
```

**Best Practices:**
- Implement least privilege principle
- Use role-based access control (RBAC)
- Validate authorization on every API request
- Audit permission changes
- Separate admin and player contexts

## Input Validation & Sanitization

### 1. Command Input Validation

```python
import re
from django.core.exceptions import ValidationError

class CommandValidator:
    """Validate and sanitize player commands"""

    ALLOWED_COMMAND_PATTERN = re.compile(r'^[a-zA-Z0-9\s\-_]+$')
    MAX_COMMAND_LENGTH = 500

    @staticmethod
    def validate_command(raw_input):
        """Validate player input"""
        if not raw_input:
            raise ValidationError("Empty command")

        if len(raw_input) > CommandValidator.MAX_COMMAND_LENGTH:
            raise ValidationError("Command too long")

        if not CommandValidator.ALLOWED_COMMAND_PATTERN.match(raw_input):
            raise ValidationError("Invalid characters in command")

        return raw_input.strip()

    @staticmethod
    def sanitize_output(text):
        """Sanitize text before sending to client"""
        from html import escape
        return escape(text)
```

**Best Practices:**
- Whitelist allowed characters
- Limit input length
- Sanitize all user-generated content
- Escape HTML in output to prevent XSS
- Validate data types (integers, strings, etc.)

### 2. SQL Injection Prevention

```python
# GOOD: Using Django ORM (parameterized queries)
Player.objects.filter(character_name=user_input)

# GOOD: Using raw SQL with parameters
from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT * FROM players WHERE name = %s", [user_input])

# BAD: String concatenation (NEVER DO THIS)
# cursor.execute(f"SELECT * FROM players WHERE name = '{user_input}'")
```

**Best Practices:**
- Always use ORM or parameterized queries
- Never concatenate user input into SQL
- Use query builders instead of raw SQL when possible
- Limit database user permissions
- Enable query logging and monitoring

### 3. NoSQL Injection Prevention

```python
# If using JSONField or MongoDB
import json

def safe_json_query(user_input):
    """Safely parse JSON input"""
    try:
        data = json.loads(user_input)
        # Validate structure
        if not isinstance(data, dict):
            raise ValueError("Expected object")
        # Whitelist allowed keys
        allowed_keys = {'action', 'target', 'data'}
        if not set(data.keys()).issubset(allowed_keys):
            raise ValueError("Invalid keys")
        return data
    except json.JSONDecodeError:
        raise ValidationError("Invalid JSON")
```

### 4. Cross-Site Scripting (XSS) Prevention

```python
from django.utils.html import escape
from bleach import clean

def sanitize_chat_message(message):
    """Sanitize chat messages to prevent XSS"""
    # Remove all HTML tags
    cleaned = clean(message, tags=[], strip=True)
    return cleaned

def allow_limited_html(message):
    """Allow safe HTML tags only"""
    allowed_tags = ['b', 'i', 'u', 'em', 'strong']
    allowed_attrs = {}
    cleaned = clean(message, tags=allowed_tags, attributes=allowed_attrs, strip=True)
    return cleaned
```

**Best Practices:**
- Escape all user-generated content
- Use Content Security Policy (CSP) headers
- Sanitize HTML if allowing any markup
- Use template auto-escaping
- Validate URL schemes (prevent javascript: URLs)

## WebSocket Security

### 1. WebSocket Authentication

```python
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
import jwt

class JWTAuthMiddleware(BaseMiddleware):
    """Authenticate WebSocket connections via JWT"""

    async def __call__(self, scope, receive, send):
        # Extract token from query string or headers
        query_string = scope.get('query_string', b'').decode()
        token = self.extract_token(query_string)

        if token:
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                scope['user'] = await self.get_user(payload['user_id'])
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
                scope['user'] = AnonymousUser()
        else:
            scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user(self, user_id):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return AnonymousUser()

    def extract_token(self, query_string):
        for pair in query_string.split('&'):
            if pair.startswith('token='):
                return pair.split('=')[1]
        return None
```

### 2. Rate Limiting

```python
from django.core.cache import cache
from django.http import HttpResponseForbidden

class RateLimiter:
    """Prevent command spam and abuse"""

    @staticmethod
    def check_rate_limit(user_id, action, max_requests=10, window=60):
        """
        Check if user has exceeded rate limit
        max_requests: Maximum number of requests
        window: Time window in seconds
        """
        cache_key = f'ratelimit:{user_id}:{action}'
        current_count = cache.get(cache_key, 0)

        if current_count >= max_requests:
            return False  # Rate limit exceeded

        cache.set(cache_key, current_count + 1, window)
        return True

# Usage in WebSocket consumer
async def receive(self, text_data):
    user_id = self.scope['user'].id

    if not RateLimiter.check_rate_limit(user_id, 'command', max_requests=20, window=10):
        await self.send(text_data=json.dumps({
            'error': 'Rate limit exceeded. Please slow down.'
        }))
        return

    # Process command
    await self.process_command(text_data)
```

### 3. Message Validation

```python
import json
from jsonschema import validate, ValidationError

MESSAGE_SCHEMA = {
    "type": "object",
    "properties": {
        "action": {"type": "string", "maxLength": 50},
        "data": {"type": "object"},
        "timestamp": {"type": "number"}
    },
    "required": ["action"],
    "additionalProperties": False
}

async def receive(self, text_data):
    """Validate incoming WebSocket messages"""
    try:
        data = json.loads(text_data)
        validate(instance=data, schema=MESSAGE_SCHEMA)
    except (json.JSONDecodeError, ValidationError) as e:
        await self.send(text_data=json.dumps({
            'error': 'Invalid message format'
        }))
        return

    # Process valid message
    await self.process_message(data)
```

## Data Protection

### 1. Encryption

```python
# Django settings.py
# HTTPS enforcement
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Cookie security
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
```

**Best Practices:**
- Use TLS 1.2 or higher
- Encrypt sensitive data at rest
- Use strong cipher suites
- Implement certificate pinning for mobile apps
- Encrypt database backups

### 2. Personal Data Protection (GDPR Compliance)

```python
class PlayerDataExport:
    """Export player data for GDPR compliance"""

    @staticmethod
    def export_player_data(player):
        """Export all player data"""
        return {
            'personal_info': {
                'username': player.user.username,
                'email': player.user.email,
                'created_at': player.user.date_joined.isoformat(),
            },
            'game_data': {
                'character_name': player.character_name,
                'level': player.level,
                'achievements': list(player.achievements.values()),
            },
            'activity_logs': list(player.activity_logs.values()),
        }

    @staticmethod
    def anonymize_player(player):
        """Anonymize player data for deletion requests"""
        player.user.username = f"deleted_user_{player.id}"
        player.user.email = f"deleted_{player.id}@example.com"
        player.user.is_active = False
        player.character_name = f"Deleted_{player.id}"
        player.save()
        player.user.save()

        # Delete or anonymize activity logs
        player.chat_messages.all().update(message="[deleted]", player_name="[deleted]")
```

**Best Practices:**
- Allow users to export their data
- Implement data deletion requests
- Anonymize data instead of deleting when needed for integrity
- Document data retention policies
- Obtain consent for data collection

## Infrastructure Security

### 1. Server Configuration

```nginx
# Nginx configuration
server {
    listen 443 ssl http2;
    server_name yourgame.com;

    # SSL configuration
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;

    location /api/login/ {
        limit_req zone=login burst=2 nodelay;
        proxy_pass http://django;
    }

    # WebSocket upgrade
    location /ws/ {
        proxy_pass http://django;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### 2. Firewall Configuration

```bash
# UFW (Uncomplicated Firewall) - Ubuntu
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable

# Allow only specific IPs for admin access
sudo ufw allow from YOUR_IP to any port 8000
```

### 3. Environment Variables

```python
# Never commit secrets to version control
# Use environment variables
import os
from pathlib import Path

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
DATABASE_PASSWORD = os.environ.get('DB_PASSWORD')
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')

# Validate required environment variables
if not SECRET_KEY:
    raise ValueError("DJANGO_SECRET_KEY environment variable not set")
```

## Monitoring & Logging

### 1. Security Logging

```python
import logging

security_logger = logging.getLogger('security')

class SecurityMiddleware:
    """Log security-relevant events"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log authentication attempts
        if request.path == '/api/login/':
            security_logger.info(f"Login attempt from {request.META.get('REMOTE_ADDR')}")

        response = self.get_response(request)

        # Log failed logins
        if request.path == '/api/login/' and response.status_code == 401:
            security_logger.warning(
                f"Failed login attempt from {request.META.get('REMOTE_ADDR')} "
                f"for user {request.POST.get('username')}"
            )

        return response
```

### 2. Intrusion Detection

```python
from django.core.cache import cache

class IntrusionDetection:
    """Detect and respond to suspicious activity"""

    @staticmethod
    def track_failed_login(ip_address, username):
        """Track failed login attempts"""
        cache_key = f'failed_logins:{ip_address}'
        failed_count = cache.get(cache_key, 0)
        failed_count += 1

        if failed_count >= 5:
            # Temporarily ban IP
            cache.set(f'banned_ip:{ip_address}', True, 3600)  # 1 hour ban
            security_logger.critical(f"IP {ip_address} banned for excessive failed logins")

        cache.set(cache_key, failed_count, 900)  # 15 minute window

    @staticmethod
    def is_ip_banned(ip_address):
        """Check if IP is banned"""
        return cache.get(f'banned_ip:{ip_address}', False)
```

### 3. Audit Trail

```python
class AuditLog(models.Model):
    """Track important user actions"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=100)
    details = models.JSONField()
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)

def log_audit_event(user, action, details, request):
    """Log security-relevant events"""
    AuditLog.objects.create(
        user=user,
        action=action,
        details=details,
        ip_address=request.META.get('REMOTE_ADDR')
    )
```

## DDoS Protection

### 1. Application-Level Protection

```python
# Django settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'throttle.middleware.ThrottleMiddleware',  # Rate limiting
]

# Throttle settings
THROTTLE_ZONES = {
    'api': {
        'VARY': 'throttle.zones.RemoteIP',
        'NUM_BUCKETS': 10,
        'BUCKET_INTERVAL': 60,
        'BUCKET_CAPACITY': 50,
    },
}
```

### 2. Infrastructure-Level Protection

**Recommendations:**
- Use CDN (Cloudflare, Akamai) for DDoS mitigation
- Implement rate limiting at load balancer level
- Configure SYN flood protection
- Use fail2ban for automatic IP banning
- Set up geographic IP filtering if needed

## Code Security

### 1. Dependency Management

```bash
# Keep dependencies updated
pip list --outdated
pip install -U package_name

# Security vulnerability scanning
pip install safety
safety check

# requirements.txt with version pinning
Django==4.2.7  # Not Django>=4.0
channels==4.0.0
channels-redis==4.1.0
```

### 2. Security Headers

```python
# Django settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
]

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# CSP
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
```

## Best Practices Summary

1. **Never trust client input** - Validate and sanitize everything
2. **Principle of least privilege** - Grant minimum necessary permissions
3. **Defense in depth** - Multiple layers of security
4. **Security by default** - Secure configurations out of the box
5. **Keep updated** - Regular security patches and updates
6. **Monitor continuously** - Log and alert on suspicious activity
7. **Encrypt everything** - Data in transit and at rest
8. **Audit regularly** - Security reviews and penetration testing
9. **Educate users** - Strong password policies and security awareness
10. **Incident response plan** - Prepare for security breaches

## Conclusion

Security must be a fundamental consideration throughout development, not an afterthought. Implement these practices from the start to protect your infrastructure, your game, and your players.
