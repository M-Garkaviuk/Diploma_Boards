from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from Diploma_Boards import settings


class TokenExpiration(TokenAuthentication):
    keyword = "Bearer"

    def authenticate_credentials(self, key):
        try:
            print("aaa")
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed("Invalid token")

        now = timezone.now()
        if not token.user.is_manager and (now - token.created).seconds > settings.TOKEN_EXPIRATION:
            token.delete()
            raise AuthenticationFailed("Token has expired.")
        return token.user, token
