"""
WebSocket Middleware

Custom middleware for WebSocket connections.
"""
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
import jwt
from django.conf import settings

User = get_user_model()


class TokenAuthMiddleware(BaseMiddleware):
    """
    JWT token authentication middleware for WebSocket connections

    Extracts JWT token from query string and authenticates user.
    """

    async def __call__(self, scope, receive, send):
        # Extract token from query string
        query_string = scope.get('query_string', b'').decode()
        token = self.extract_token(query_string)

        if token:
            try:
                # Decode JWT token
                payload = jwt.decode(
                    token,
                    settings.SECRET_KEY,
                    algorithms=['HS256']
                )
                user_id = payload.get('user_id')

                # Get user from database
                scope['user'] = await self.get_user(user_id)
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, Exception):
                scope['user'] = AnonymousUser()
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
    def get_user(self, user_id):
        """Get user from database"""
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return AnonymousUser()

    @database_sync_to_async
    def get_user_from_session(self, scope):
        """Get user from Django session"""
        from django.contrib.auth.models import User
        session = scope.get('session', {})
        user_id = session.get('_auth_user_id')

        if user_id:
            try:
                return User.objects.get(id=user_id)
            except User.DoesNotExist:
                pass

        return AnonymousUser()
