from django.shortcuts import render
import json

from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.aggregates import StringAgg
from django.db.models import Case, IntegerField, Q, When, Sum, Count, F, CharField, Avg, DurationField

from administracao.decorators import admin_member_required
from datetime import datetime
from administracao.utils import *
from agendamento.forms import *
from unidecode import unidecode
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
import csv, io
from agendamento.models import *
from administracao.models import *
from .models import *
from .forms import *
# Create your views here.

@login_required
def cartao_vacina(request):
    form = FiltroVacinaForm(request.GET or None)
    cartao, encontrado = CartaoVacina.objects.get_or_create(usuario=request.user.usuario)
    registros = VacinaUsuario.objects.filter(cartao=cartao)

    if request.GET and form.is_valid():
        data=form.cleaned_data.get("data")
        if data:
            registros = registros.filter(data__date=data)
    vacinas = paginar_registros(request, registros, 20)

    return render(request, "cartao_vacina.html",
                  locals())


@login_required
def cadastrar_vacina_privada(request):
    form = VacinaPrivadaForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            vacina = form.save(commit=False)
            vacina.cartao = request.user.usuario.cartao
            vacina.responsavel = request.user.usuario
            vacina.save()
            messages.success(request, "Vacina cadastrada com sucesso.")
            return HttpResponseRedirect(reverse('cartao_vacina'))
        else:
            messages.warning(request, "Verifique os dados passados")

    return render(request, "vacina_privada.html",
                  locals())