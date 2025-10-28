from rest_framework import serializers
from .models import Jogador, Partida

class JogadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jogador
        fields = ['id', 'nome', 'email', 'data_nascimento', 'sexo', 'categoria', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

class PartidaSerializer(serializers.ModelSerializer):
    owner_id = serializers.UUIDField(source='owner.id', read_only=True)
    jogadores_confirmados = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    jogadores_pendentes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Partida
        fields = [
            'id', 'owner_id', 'status', 'local_descricao', 'data_hora', 
            'categoria', 'tipo', 'jogadores_confirmados', 'jogadores_pendentes'
        ]
        read_only_fields = ['status', 'owner_id']

class CriarPartidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partida
        fields = ['local_descricao', 'data_hora', 'categoria', 'tipo']

class AprovarJogadorSerializer(serializers.Serializer):
    jogador_id_aprovar = serializers.UUIDField()