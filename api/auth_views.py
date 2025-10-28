from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import check_password
from .models import Jogador

class LoginView(APIView):
    permission_classes = [AllowAny] 

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {"error": "Email e senha são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            jogador = Jogador.objects.get(email=email)
        except Jogador.DoesNotExist:
            return Response(
                {"error": "Credenciais inválidas."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not check_password(password, jogador.password):
            return Response(
                {"error": "Credenciais inválidas."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response({"auth_token": jogador.auth_token}, status=status.HTTP_200_OK)