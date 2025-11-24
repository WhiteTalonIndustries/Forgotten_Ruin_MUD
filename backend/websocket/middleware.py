"""
WebSocket Middleware

Custom middleware for WebSocket connections.
"""
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()


class TokenAuthMiddleware(BaseMiddleware):
    """
    Token authentication middleware for WebSocket connections

    Supports both DRF Token and session authentication.
    Extracts token from query string and authenticates user.
    """

    async def __call__(self, scope, receive, send):
        # Extract token from query string
        query_string = scope.get('query_string', b'').decode()
        token_key = self.extract_token(query_string)

        if token_key:
            # Try DRF Token authentication
            scope['user'] = await self.get_user_from_token(token_key)
        else:
            # Try session authentication as fallback
            if 'session' in scope:
                scope['user'] = await self.get_user_from_session(scope)
            else:
                scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)

    def extract_token(self, query_string):
        """Extract token from query string"""
        for param in query_string.split('&'):
            if param.startswith('token='):
                return param.split('=')[1]
        return None

    @database_sync_to_async
    def get_user_from_token(self, token_key):
        """Get user from DRF token"""
        try:
            token = Token.objects.select_related('user').get(key=token_key)
            return token.user
        except Token.DoesNotExist:
            return AnonymousUser()

    @database_sync_to_async
    def get_user_from_session(self, scope):
        """Get user from Django session"""
        session = scope.get('session', {})
        user_id = session.get('_auth_user_id')

        if user_id:
            try:
                return User.objects.get(id=user_id)
            except User.DoesNotExist:
                pass

        return AnonymousUser()
