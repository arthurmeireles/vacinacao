from django.db import models
from administracao.models import *
# Create your models here.


class HorarioEstabelecimento(models.Model):
    estabelecimento = models.ForeignKey(EstabelecimentoSaude, on_delete=models.CASCADE, related_name="horarios")
    vacina = models.ForeignKey(Vacina, on_delete=models.CASCADE, related_name="horarios")
    data = models.DateTimeField()
    vagas = models.PositiveIntegerField()


class Agendamento(models.Model):
    data = models.DateTimeField()
    vacina = models.ForeignKey(Vacina, on_delete=models.CASCADE)
    estabelecimento = models.ForeignKey(EstabelecimentoSaude, related_name="agendamentos", on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="agendamentos")
    aplicado = models.BooleanField(default=False)


