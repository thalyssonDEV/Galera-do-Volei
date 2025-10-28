from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import Jogador
from django.core.exceptions import ValidationError # Importe isso

class SimpleTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]

        try:
            jogador = Jogador.objects.get(auth_token=token)
        except (Jogador.DoesNotExist, ValidationError):
            raise AuthenticationFailed('Token inválido ou mal formado.')

        return (jogador, None)