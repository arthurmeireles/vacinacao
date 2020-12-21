# Importa os municipios

from django.db import migrations, models
from administracao.models import *
import csv
from django.core.management import call_command

def load_fixture(apps, schema_editor):
    call_command('loaddata', 'ufs', app_label='administracao')

def upload_csv(apps, schema_editor):
    HEADERS = {
        "UF": 0,
        "Nome_UF": 1,
        "Codigo_Municipio": 2,
        "Nome_Municipio": 3,
    }
    municipios = [m[0] for m in Municipio.objects.all().values_list("codigo")]
    estabelecimentos = [e[0] for e in EstabelecimentoSaude.objects.all().values_list("codigo_cnes")]
    with open('municipios_ibge.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for column in spamreader:
            if column[HEADERS["UF"]] != "UF":
                uf = UnidadeFederativa.objects.get(codigo=column[HEADERS["UF"]])
                if column[HEADERS["Codigo_Municipio"]] in municipios:
                    Municipio.objects.filter(codigo=column[HEADERS["Codigo_Municipio"]])\
                        .update(
                            estado = uf,
                            nome = column[HEADERS["Nome_Municipio"]],
                        )
                else:
                    Municipio.objects.create(codigo=column[HEADERS["Codigo_Municipio"]],
                            estado = uf,
                            nome = column[HEADERS["Nome_Municipio"]],
                        )


class Migration(migrations.Migration):

    dependencies = [
        ('administracao', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_fixture),
        migrations.RunPython(upload_csv),
    ]
