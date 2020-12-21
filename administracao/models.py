from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.safestring import mark_safe
from datetime import date


class UnidadeFederativa(models.Model):
    codigo = models.CharField(max_length=2, unique=True, primary_key=True)
    sigla = models.CharField(max_length=2, unique=True)
    nome = models.CharField(max_length=60, unique=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return u'%s/%s' % (self.nome, self.sigla)


class Municipio(models.Model):
    estado = models.ForeignKey(UnidadeFederativa, related_name="municipios", on_delete=models.CASCADE)
    codigo = models.CharField(max_length=6, unique=True)
    nome = models.CharField(max_length=60)

    def __str__(self):
        return "%s/%s" % (self.nome, self.estado.sigla)


class EstabelecimentoSaude(models.Model):
    codigo_cnes = models.CharField(verbose_name=u'CNES', max_length=8, unique=True)
    nome_fantasia = models.CharField(max_length=300)
    municipio = models.ForeignKey(Municipio, related_name="unidades", on_delete=models.CASCADE)
    razao_social = models.CharField(max_length=300, null=True, blank=True)
    logradouro = models.CharField(max_length=300, null=True, blank=True)
    endereco = models.CharField(max_length=300, null=True, blank=True)
    complemento = models.CharField(max_length=300, null=True, blank=True)
    bairro = models.CharField(max_length=300, null=True, blank=True)
    cep = models.CharField(max_length=300, null=True, blank=True)
    telefone = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return u'%s - %s' % (self.codigo_cnes, self.nome_fantasia)


class Usuario(models.Model):
    user = models.OneToOneField(User, related_name="usuario", on_delete=models.CASCADE)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    data_nascimento = models.DateField(null=True)

    def __str__(self):
        return '%s - %s' % (self.cpf, self.user.first_name)

    def idade(self):
        today = date.today()
        if self.data_nascimento:
            return today.year - self.data_nascimento.year - (
                        (today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day))
        else:
            return "Não informada"


class ProfissionalVinculo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="vinculos")
    estabelecimento = models.ForeignKey(EstabelecimentoSaude, on_delete=models.CASCADE, related_name="vinculos")
    ativo = models.BooleanField(default=True)


class Vacina(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return '%s' % (self.nome)


class EstoqueVacina(models.Model):
    vacina = models.ForeignKey(Vacina, on_delete=models.CASCADE, related_name="estabelecimentos")
    estabelecimento = models.ForeignKey(EstabelecimentoSaude, on_delete=models.CASCADE, related_name="vacinas")
    qtd = models.PositiveIntegerField(default=0)


