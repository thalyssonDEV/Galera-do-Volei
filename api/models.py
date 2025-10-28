import uuid
from django.db import models
from django.contrib.auth.hashers import make_password

class Jogador(models.Model):
    class Sexo(models.TextChoices):
        MASCULINO = 'MASCULINO', 'Masculino'
        FEMININO = 'FEMININO', 'Feminino'

    class Categoria(models.TextChoices):
        AMADOR = 'AMADOR', 'Amador'
        INTERMEDIARIO = 'INTERMEDIARIO', 'Intermediário'
        PROFISSIONAL = 'PROFISSIONAL', 'Profissional'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    data_nascimento = models.DateField()
    sexo = models.CharField(max_length=10, choices=Sexo.choices)
    categoria = models.CharField(max_length=15, choices=Categoria.choices)
    password = models.CharField(max_length=128)
    auth_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.password = make_password(self.password)
        else:
            try:
                original = Jogador.objects.get(pk=self.pk)
                if self.password != original.password:
                    self.password = make_password(self.password)
            except Jogador.DoesNotExist:
                self.password = make_password(self.password)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome
    
    @property
    def is_authenticated(self):
        return True

class Partida(models.Model):
    class Status(models.TextChoices):
        EM_ADESAO = 'EM_ADESAO', 'Em Adesão'
        COMPLETA = 'COMPLETA', 'Completa'
        REALIZADA = 'REALIZADA', 'Realizada'
        CANCELADA = 'CANCELADA', 'Cancelada'

    class Categoria(models.TextChoices):
        AMADOR = 'AMADOR', 'Amador'
        INTERMEDIARIO = 'INTERMEDIARIO', 'Intermediário'
        PROFISSIONAL = 'PROFISSIONAL', 'Profissional'

    class Tipo(models.TextChoices):
        MASCULINA = 'MASCULINA', 'Masculina'
        FEMININA = 'FEMININA', 'Feminina'
        MISTA = 'MISTA', 'Mista'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(Jogador, on_delete=models.CASCADE, related_name='partidas_criadas')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.EM_ADESAO)
    local_descricao = models.CharField(max_length=255)
    data_hora = models.DateTimeField()
    categoria = models.CharField(max_length=15, choices=Categoria.choices)
    tipo = models.CharField(max_length=10, choices=Tipo.choices)
    
    jogadores_confirmados = models.ManyToManyField(Jogador, related_name='partidas_confirmadas', blank=True)
    jogadores_pendentes = models.ManyToManyField(Jogador, related_name='partidas_pendentes', blank=True)

    def __str__(self):
        return f"Partida em {self.local_descricao} - {self.data_hora.strftime('%d/%m/%Y %H:%M')}"