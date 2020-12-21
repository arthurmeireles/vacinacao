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
from cartao_vacina.models import *
from django.core.mail import send_mail
from administracao.decorators import *
from cartao_vacina.forms import *


@profissional_member_required
def horario_estabelecimento(request):
    vinculo = ProfissionalVinculo.objects.get(pk=request.session["vinculo_id"])
    estoque = EstoqueVacina.objects.filter(estabelecimento=EstabelecimentoSaude.objects.get(pk=vinculo.estabelecimento.id))
    estabelecimento = EstabelecimentoSaude.objects.get(pk=vinculo.estabelecimento.id)
    horarios = {}
    for e in estoque:
        horarios["%s"%e.vacina.nome] = list(HorarioEstabelecimento.objects.filter(estabelecimento=estabelecimento,
                                                            vacina=e.vacina).values_list("data", "vagas"))
        for h in range(len(horarios["%s"%e.vacina.nome])):
            horarios["%s"%e.vacina.nome][h] = [
                horarios["%s"%e.vacina.nome][h][0],
                horarios["%s"%e.vacina.nome][h][1],
                Agendamento.objects.filter(data=horarios["%s"%e.vacina.nome][h][0],
                                            vacina=e.vacina,
                                            estabelecimento=estabelecimento).count()
            ]

    print(horarios)
    # if request.GET and form.is_valid():
    #     nome = form.cleaned_data["nome"]
    #     if nome:
    #         registros = registros.filter(nome__icontains=nome)

    return render(request, "horario.html",
                  locals())


# def validar_vagas(formset, horarios, vacina, estabelecimento):
#     agendamentos = Agendamento.objects.filter(vacina=vacina, estabelecimento=estabelecimento, data__gte=datetime.now())
#     for f in formset:
#         ag = agendamentos.filter(data=datetime.combine(f.cleaned_data.get("data"), f.cleaned_data.get("hora")))
#         if len(ag) > f.cleaned_data.get("vagas"):
#             return [False, [datetime.combine(f.cleaned_data.get("data"), f.cleaned_data.get("hora"))]]
#         agendamentos = agendamentos.exclude(pk__in=ag)
#     if len(agendamentos) > 0:
#         return [False, [a.data for a in agendamentos]]
#     return [True, []]


@profissional_member_required
@login_required()
def editar_horario(request, vacina_id):
    vacina = get_object_or_404(Vacina, pk=vacina_id)
    vinculo = ProfissionalVinculo.objects.get(pk=request.session["vinculo_id"])
    estabelecimento = EstabelecimentoSaude.objects.get(pk=vinculo.estabelecimento.id)
    horarios = HorarioEstabelecimento.objects.filter(estabelecimento=estabelecimento,
                                                            vacina=vacina, data__gte=datetime.now())
    initial = []
    for horario in horarios:
        initial.append({
            "data": horario.data.date(),
            "hora": horario.data.time(),
            "vagas": horario.vagas
        })
    myformset = HorarioFormSet(request.POST or None, initial=initial)

    if request.POST:
        if myformset.is_valid():
            HorarioEstabelecimento.objects.filter(estabelecimento=estabelecimento,
                                                            vacina=vacina).delete()
            for f in myformset:
                if f.cleaned_data.get("vagas") and f.cleaned_data.get("data") and f.cleaned_data.get("hora"):
                    h = HorarioEstabelecimento.objects.create(estabelecimento=estabelecimento,
                                            vacina=vacina,
                                            vagas = f.cleaned_data.get("vagas"),
                                            data = datetime.combine(f.cleaned_data.get("data"), f.cleaned_data.get("hora")))
            messages.success(request, "Horários cadastrados com sucesso.")
            return HttpResponseRedirect(reverse('horario_estabelecimento'))
        else:
            messages.warning(request, "Verifique os dados passados")

    return render(request, "editar_horario.html", locals())


@login_required
def agendamento(request):
    registros = Agendamento.objects.filter(usuario=request.user.usuario).order_by("-data")
    form = FiltroVacinaForm(request.GET or None)

    if request.GET and form.is_valid():
        data=form.cleaned_data.get("data")
        if data:
            registros = registros.filter(data__date=data)
    agendamentos = paginar_registros(request, registros, 20)

    return render(request, "agendamentos.html",
                  locals())


@login_required
def agendar_vacinacao(request):
    form = AgendamentoForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            agendamento = form.save(commit=False)
            agendamentos_previos = Agendamento.objects.filter(usuario=request.user.usuario,
                                        vacina=agendamento.vacina,
                                        data__gte=datetime.now())
            # if agendamentos_previos.exists():
            #     messages.warning(request, "Já existe um agendamento marcado para a vacina %s"%agendamento.vacina.nome)
            #     return HttpResponseRedirect(reverse('agendamentos'))

            agendamento.usuario = request.user.usuario
            agendamento.save()

            horario = HorarioEstabelecimento.objects.filter(estabelecimento=agendamento.estabelecimento,
                                    vacina=agendamento.vacina,
                                    data=agendamento.data).first()
            horario.vagas -= 1
            horario.save()

            mensagem = """
                Prezado(a) %s,
                O seu agendamento para a vacina %s foi confirmado no local e horário abaixo.

                Local: %s, (%s-%s/%s)
                Data/Hora: %s
            
            """%(request.user.first_name, agendamento.vacina.nome, agendamento.estabelecimento.nome_fantasia,
                    agendamento.estabelecimento.logradouro, agendamento.estabelecimento.municipio.nome,
                    agendamento.estabelecimento.municipio.estado.sigla,
                    agendamento.data.strftime("%d/%m/%Y %H:%M"))
            send_mail(u'Agendamento de Vacina',
                    mensagem,
                  u'lais.ufrn@gmail.com', [request.user.email], fail_silently=False)
            messages.success(request, "Agendamento realizado com sucesso.")
            return HttpResponseRedirect(reverse('agendamentos'))
        else:
            messages.warning(request, "Verifique os dados passados")
    return render(request, "novo_agendamento.html", locals())


@login_required
def fila_agendamento(request):
    if request.session.get("perfil") == "profissional":
        vinculo = ProfissionalVinculo.objects.get(pk=request.session["vinculo_id"])
        estabelecimento = EstabelecimentoSaude.objects.get(pk=vinculo.estabelecimento.id)
        fila = Agendamento.objects.filter(data__date=datetime.now(), 
            estabelecimento=estabelecimento,
            aplicado=False).order_by("data")
    else:
        meu_agendamento = Agendamento.objects.filter(data__date=datetime.now(), 
                                    usuario=request.user.usuario,
                                    aplicado=False)
        if meu_agendamento.exists():
            meu_agendamento = meu_agendamento.first()
            estabelecimento = meu_agendamento.estabelecimento
            fila = Agendamento.objects.filter(data__date=datetime.now(), 
                                    estabelecimento=meu_agendamento.estabelecimento,
                                    aplicado=False).order_by("data")
        else:
            fila = []
    
    return render(request, "fila_agendamento.html", locals())


@login_required
def fila_agendamento_json(request):
    fila = []
    if request.session.get("perfil") == "profissional":
        vinculo = ProfissionalVinculo.objects.get(pk=request.session["vinculo_id"])
        estabelecimento = EstabelecimentoSaude.objects.get(pk=vinculo.estabelecimento.id)
        fila = Agendamento.objects.filter(data__date=datetime.now(), 
            estabelecimento=estabelecimento,
            aplicado=False).order_by("data")
    else:
        meu_agendamento = Agendamento.objects.filter(data__date=datetime.now(), 
                                    usuario=request.user.usuario,
                                    aplicado=False)
        if meu_agendamento.exists():
            meu_agendamento = meu_agendamento.first()
            fila = Agendamento.objects.filter(data__date=datetime.now(), 
                                    estabelecimento=meu_agendamento.estabelecimento,
                                    aplicado=False).order_by("data")
    retorno = []
    for a in fila:
        retorno.append({
            "usuario__user__first_name": a.usuario.user.first_name,
            "data": a.data.strftime("%H:%M"),
            "vacina__nome": a.vacina.nome,
            "id": a.id,
            "user_id": a.usuario.user.id
        })
    return JsonResponse(retorno, safe=False)


@profissional_member_required
def chamar_fila(request, id):
    agendamento = Agendamento.objects.get(pk=id)
    agendamento.aplicado = True
    agendamento.save()

    cartao, e = CartaoVacina.objects.get_or_create(usuario=agendamento.usuario)
    vacina = VacinaUsuario.objects.create(
        cartao=cartao,
        vacina=agendamento.vacina,
        data=datetime.now(),
        responsavel=request.user.usuario,
        local=agendamento.estabelecimento
    )

    mensagem = """
                Prezado(a) %s,
                A sua aplicaçao da vacina %s foi registrada no local e horário abaixo.

                Local: %s, (%s-%s/%s)
                Data/Hora: %s
            
            """%(agendamento.usuario.user.first_name, agendamento.vacina.nome, agendamento.estabelecimento.nome_fantasia,
                    agendamento.estabelecimento.logradouro, agendamento.estabelecimento.municipio.nome,
                    agendamento.estabelecimento.municipio.estado.sigla,
                    vacina.data.strftime("%d/%m/%Y %H:%M"))
    send_mail(u'Registro de Vacina',
            mensagem,
            u'lais.ufrn@gmail.com', [agendamento.usuario.user.email], fail_silently=False)

    return JsonResponse([{"response":200}], safe=False)
    