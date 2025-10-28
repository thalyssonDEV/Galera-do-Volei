from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import Jogador, Partida
from .serializers import (
    JogadorSerializer, PartidaSerializer, 
    CriarPartidaSerializer, AprovarJogadorSerializer
)

class JogadorViewSet(viewsets.ModelViewSet):
    queryset = Jogador.objects.all()
    serializer_class = JogadorSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post', 'get']


class PartidaViewSet(viewsets.ModelViewSet):
    queryset = Partida.objects.all()
    http_method_names = ['post', 'get']

    def get_serializer_class(self):
        if self.action == 'create':
            return CriarPartidaSerializer
        return PartidaSerializer
    
    def perform_create(self, serializer):
        # Define o owner da partida como o usuário que fez a requisição
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], url_path='solicitar-adesao')
    def solicitar_adesao(self, request, pk=None):
        partida = self.get_object()
        # O solicitante é o próprio usuário autenticado
        partida.jogadores_pendentes.add(request.user)
        return Response({"message": "Solicitação registrada."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='aprovar-jogador')
    def aprovar_jogador(self, request, pk=None):
        partida = self.get_object()
        
        if partida.owner != request.user:
            return Response({"error": "Apenas o dono da partida pode aprovar."}, status=status.HTTP_403_FORBIDDEN)

        serializer = AprovarJogadorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        jogador_id = serializer.validated_data['jogador_id_aprovar']
        jogador = get_object_or_404(Jogador, pk=jogador_id)

        if jogador not in partida.jogadores_pendentes.all():
            return Response({"error": "Jogador não está na lista de pendentes."}, status=status.HTTP_400_BAD_REQUEST)

        partida.jogadores_pendentes.remove(jogador)
        partida.jogadores_confirmados.add(jogador)
        
        return Response(PartidaSerializer(partida).data, status=status.HTTP_200_OK)

    def _change_partida_status(self, request, pk, new_status):
        partida = get_object_or_404(Partida, pk=pk)
        if partida.owner != request.user:
            return Response({"error": "Apenas o dono da partida pode alterar seu status."}, status=status.HTTP_403_FORBIDDEN)
        
        partida.status = new_status
        partida.save()
        return Response(PartidaSerializer(partida).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='fechar-adesao')
    def fechar_adesao(self, request, pk=None):
        return self._change_partida_status(request, pk, Partida.Status.COMPLETA)

    @action(detail=True, methods=['post'], url_path='finalizar')
    def finalizar(self, request, pk=None):
        return self._change_partida_status(request, pk, Partida.Status.REALIZADA)

    @action(detail=True, methods=['post'], url_path='cancelar')
    def cancelar(self, request, pk=None):
        return self._change_partida_status(request, pk, Partida.Status.CANCELADA)