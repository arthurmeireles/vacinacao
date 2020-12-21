from django.db import models
from administracao.models import *
# Create your models here.

class CartaoVacina(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="cartao")
    vacinas = models.ManyToManyField(Vacina, through="VacinaUsuario")


class VacinaUsuario(models.Model):
    cartao = models.ForeignKey(CartaoVacina, on_delete=models.CASCADE)
    vacina = models.ForeignKey(Vacina, on_delete=models.CASCADE)
    data = models.DateTimeField()
    responsavel = models.ForeignKey(Usuario, related_name="vacinas_aplicadas", on_delete=models.CASCADE)
    local = models.ForeignKey(EstabelecimentoSaude, related_name="vacinas_aplicadas", on_delete=models.CASCADE, null=True)

