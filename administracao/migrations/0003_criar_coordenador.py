# Importa os municipios

from django.db import migrations, models
from administracao.models import *
import csv
from django.core.management import call_command
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group


def dados_iniciais(apps, schema_editor):
    paciente = User.objects.create(username="89077810013",
                                        password=make_password("treinamento"),
                                        email="email@email.com",
                                        first_name="Fulano Paciente")
    usuario_paciente = Usuario.objects.create(user=paciente,
                                                cpf="89077810013")
    coordenador = User.objects.create(username="92347763059",
                                        password=make_password("treinamento"),
                                        email="coord@email.com",
                                        first_name="Ciclano Coordenador SUS")
    usuario_coord = Usuario.objects.create(user=coordenador,
                                                cpf="92347763059")

    profissional = User.objects.create(username="44901141090",
                                        password=make_password("treinamento"),
                                        email="prof@email.com",
                                        first_name="Beltrano Profissional Saude")
    usuario_prof = Usuario.objects.create(user=profissional,
                                                cpf="44901141090")

    coordenador_grupo, e = Group.objects.get_or_create(name="Coordenador SUS")
    profissinoal_grupo, e = Group.objects.get_or_create(name="Profissional Saude")

    coordenador.groups.add(coordenador_grupo)

    estabelecimento = EstabelecimentoSaude.objects.create(
                    codigo_cnes="123456",
                    nome_fantasia="Estabelecimento de Teste",
                    municipio=Municipio.objects.get(codigo="240810"),
                    razao_social="Estabelecimento de Teset",
                    logradouro="Rua X do Y do Z"
    )

    vinculo = ProfissionalVinculo.objects.create(
        usuario=usuario_prof,
        estabelecimento=estabelecimento,
        ativo=True
    )

    profissional.groups.add(profissinoal_grupo)


class Migration(migrations.Migration):

    dependencies = [
        ('administracao', '0002_import_municipios'),
    ]

    operations = [
        migrations.RunPython(dados_iniciais),
    ]
