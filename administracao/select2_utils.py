from django.db.models.functions import Concat, Extract
from administracao.models import *
from agendamento.models import *
from django.db.models import Value, Q, Count
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from datetime import datetime

# ------------------ URLS Select2 ------------------ #

def buscar_municipio(request):
    municipios = Municipio.objects.filter(Q(nome__icontains=request.GET.get("q"))|Q(estado__sigla=request.GET.get("q")))
    if request.GET.get("vacina"):
        municipios = municipios.filter(unidades__horarios__vagas__gte=1,
                                        unidades__horarios__vacina__pk=request.GET.get("vacina"),
                                        unidades__horarios__data__gte=datetime.now()).distinct()
    return JsonResponse(list(municipios.annotate(
        text=Concat('nome', Value('/'), 'estado__sigla')).values("id", "text")), safe=False)


def buscar_estabelecimento(request):
    estabelecimentos = EstabelecimentoSaude.objects.filter(Q(nome_fantasia__icontains=request.GET.get("q"))|Q(codigo_cnes__icontains=request.GET.get("q")))
    if request.GET.get("vacina") and request.GET.get("municipio"):
        estabelecimentos = estabelecimentos.filter(horarios__vagas__gte=1,
                horarios__vacina__pk=request.GET.get("vacina"), municipio__pk=request.GET.get("municipio"),
                    horarios__data__gte=datetime.now()).distinct()
    return JsonResponse(list(estabelecimentos.annotate(
        text=Concat('nome_fantasia', Value('/'), 'codigo_cnes')).values("id", "text")), safe=False)


def buscar_data(request):
    # estabelecimentos = EstabelecimentoSaude.objects.filter(Q(nome_fantasia__icontains=request.GET.get("q"))|Q(codigo_cnes__icontains=request.GET.get("q")))
    retorno = []
    if request.GET.get("vacina") and request.GET.get("estabelecimento"):
        horarios = HorarioEstabelecimento.objects.filter(vacina__pk=request.GET.get("vacina"),
                        estabelecimento__pk=request.GET.get("estabelecimento"),
                        vagas__gt=0, data__gte=datetime.now())
        for horario in horarios:
            retorno.append({"id": horario.data.strftime("%d/%m/%Y %H:%M"),
                            "text": horario.data.strftime("%d/%m/%Y %H:%M")})
    return JsonResponse(retorno, safe=False)


def buscar_vacina(request):
    return JsonResponse(list(Vacina.objects.filter(nome__icontains=request.GET.get("q")).annotate(
        text=Concat('nome', Value(''))).values("id", "text")), safe=False)
