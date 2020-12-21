import json

from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.aggregates import StringAgg
from django.db.models import Case, IntegerField, Q, When, Sum, Count, F, CharField, Avg, DurationField
from django.contrib.auth.forms import AuthenticationForm
from administracao.decorators import *
from datetime import datetime
from .utils import *
from administracao.forms import *
from unidecode import unidecode
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
import csv, io
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.db import connection
from agendamento.models import *


@admin_member_required
@login_required()
def estabelecimento_saude(request):
    # u = UnidadeFederativa.objects.get(
    #     codigo = '123',
    #     sigla = "RN",
    #     nome = "Rio Grande da Bosta")

    # Municipio.objects.create(estado=u,
    #     codigo="130260",
    #     nome="Algum lugar")
    form = FiltroEstabelecimentoForm(request.GET or None)
    registros = EstabelecimentoSaude.objects.prefetch_related("municipio", "municipio__estado")

    if request.GET and form.is_valid():
        cnes = form.cleaned_data["cnes"]
        nome = form.cleaned_data["nome"]

        if cnes:
            registros = registros.filter(codigo_cnes__icontains=cnes)
        if nome:
            query = Q(nome_fantasia__icontains=nome) | Q(nome_fantasia__icontains=unidecode(nome))
            registros = registros.filter(query)

    estabelecimentos = paginar_registros(request, registros, 20)
    return render(request, "estabelecimento.html",
                  locals())


@admin_member_required
@login_required()
def ver_estabelecimento(request, id):
    estabelecimento = get_object_or_404(EstabelecimentoSaude, pk=id)
    # profissionais = Usuario.objects.filter(vinculos__estabelecimento=estabelecimento).distinct().count(),
    # teleconsultas = Teleconsulta.objects.filter(autor__estabelecimento=estabelecimento).distinct().count()

    return render(request, "ver_estabelecimento.html", locals())


@admin_member_required
@login_required()
def novo_estabelecimento(request):
    form = EstabelecimentoForm(request.POST or None)

    if request.POST:
        if form.is_valid():
            form.save()

            messages.success(request, "Estabelecimento cadastrado com sucesso.")
            return HttpResponseRedirect(reverse('estabelecimentos'))
        else:
            if request.POST.get("municipio"):
                municipio_error = get_object_or_404(Municipio, pk=request.POST.get("municipio"))

            messages.warning(request, "Verifique os dados passados")

    return render(request, "novo_estabelecimento.html", locals())


@admin_member_required
@login_required()
def editar_estabelecimento(request, id):
    estabelecimento = get_object_or_404(EstabelecimentoSaude, pk=id)
    form = EstabelecimentoForm(request.POST or None, instance=estabelecimento)

    if request.POST:
        if form.is_valid():
            form.save()

            messages.success(request, "Estabelecimento editado com sucesso.")
            return HttpResponseRedirect(reverse('estabelecimentos'))
        else:
            if request.POST.get("municipio"):
                municipio_error = get_object_or_404(Municipio, pk=request.POST.get("municipio"))

            messages.warning(request, "Verifique os dados passados")

    return render(request, "novo_estabelecimento.html", locals())


@admin_member_required
@login_required()
def upload_csv(request):
    municipios_nao_encontrados = set()
    if request.POST:
        csv_file = request.FILES['file']
        # let's check if it is a csv file
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'O arquivo importado não estava no formato CSV.')
            return HttpResponseRedirect(reverse('estabelecimentos'))
        data_set = csv_file.read().decode('UTF-8')
        # setup a stream which is when we loop through each line we are able to handle a data in a stream
        io_string = io.StringIO(data_set)
        next(io_string)
        HEADERS = {
            "CO_CNES": 1,
            "NO_RAZAO_SOCIAL": 5,
            "NO_FANTASIA": 6,
            "NO_LOGRADOURO": 7,
            "NU_ENDERECO": 8,
            "NO_COMPLEMENTO": 9,
            "NO_BAIRRO": 10,
            "CO_CEP": 11,
            "NU_TELEFONE": 16,
            "CO_MUNICIPIO_GESTOR": 31
        }
        municipios = [m[0] for m in Municipio.objects.all().values_list("codigo")]
        estabelecimentos = [e[0] for e in EstabelecimentoSaude.objects.all().values_list("codigo_cnes")]
        
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            if column[HEADERS["CO_CNES"]] in estabelecimentos:
                EstabelecimentoSaude.objects.filter(codigo_cnes=column[HEADERS["CO_CNES"]])\
                    .update(
                        razao_social = column[HEADERS["NO_RAZAO_SOCIAL"]],
                        nome_fantasia = column[HEADERS["NO_FANTASIA"]],
                        logradouro = column[HEADERS["NO_LOGRADOURO"]],
                        endereco = column[HEADERS["NU_ENDERECO"]],
                        complemento = column[HEADERS["NO_COMPLEMENTO"]],
                        bairro = column[HEADERS["NO_BAIRRO"]],
                        cep = column[HEADERS["CO_CEP"]],
                        telefone = column[HEADERS["NU_TELEFONE"]],
                    )
            else:
                if column[HEADERS["CO_MUNICIPIO_GESTOR"]] in municipios:
                    EstabelecimentoSaude.objects.create(
                            codigo_cnes=column[HEADERS["CO_CNES"]],
                            municipio = Municipio.objects.get(codigo=column[HEADERS["CO_MUNICIPIO_GESTOR"]]),
                            razao_social = column[HEADERS["NO_RAZAO_SOCIAL"]],
                            nome_fantasia = column[HEADERS["NO_FANTASIA"]],
                            logradouro = column[HEADERS["NO_LOGRADOURO"]],
                            endereco = column[HEADERS["NU_ENDERECO"]],
                            complemento = column[HEADERS["NO_COMPLEMENTO"]],
                            bairro = column[HEADERS["NO_BAIRRO"]],
                            cep = column[HEADERS["CO_CEP"]],
                            telefone = column[HEADERS["NU_TELEFONE"]],
                        )
                else:
                    municipios_nao_encontrados.add(column[HEADERS["CO_MUNICIPIO_GESTOR"]])

    messages.success(request, "Importação bem sucedida!")
    if municipios_nao_encontrados:
        messages.warning(request, "Os estabelecimentos nos municipios de IBGEs = %s \
            não foram importados pois o municipio não está presente no banco de dados.\
             Cadastre esses municípios e tente novamente"%(str(municipios_nao_encontrados)))
    return HttpResponseRedirect(reverse('estabelecimentos'))


@admin_member_required
@login_required()
def municipio(request):
    form = FiltroMunicipioForm(request.GET or None)
    registros = Municipio.objects.all()

    if request.GET and form.is_valid():
        ibge = form.cleaned_data["ibge"]
        nome = form.cleaned_data["nome"]
        estado = form.cleaned_data["estado"]

        if ibge:
            registros = registros.filter(codigo__icontains=ibge)
        if nome:
            registros = registros.filter(nome__icontains=nome)
        if estado:
            registros = registros.filter(estado=estado)

    municipios = paginar_registros(request, registros, 20)
    return render(request, "municipio.html",
                  locals())

@admin_member_required
@login_required()
def ver_municipio(request, id):
    municipio = get_object_or_404(Municipio, pk=id)
    # profissionais = Usuario.objects.filter(vinculos__estabelecimento=estabelecimento).distinct().count(),
    # teleconsultas = Teleconsulta.objects.filter(autor__estabelecimento=estabelecimento).distinct().count()

    return render(request, "ver_municipio.html", locals())


@admin_member_required
@login_required()
def novo_municipio(request):
    form = MunicipioForm(request.POST or None)

    if request.POST:
        if form.is_valid():
            form.save()

            messages.success(request, "Municipio cadastrado com sucesso.")
            return HttpResponseRedirect(reverse('municipios'))
        else:
            messages.warning(request, "Verifique os dados passados")

    return render(request, "novo_municipio.html", locals())


@admin_member_required
@login_required()
def editar_municipio(request, id):
    municipio = get_object_or_404(Municipio, pk=id)
    form = MunicipioForm(request.POST or None, instance=municipio)

    if request.POST:
        if form.is_valid():
            form.save()

            messages.success(request, "Municipio editado com sucesso.")
            return HttpResponseRedirect(reverse('municipios'))
        else:
            messages.warning(request, "Verifique os dados passados")

    return render(request, "novo_municipio.html", locals())


@login_required()
def vacina(request):
    form = FiltroNomeForm(request.GET or None)
    registros = Vacina.objects.all()

    if request.GET and form.is_valid():
        nome = form.cleaned_data["nome"]
        if nome:
            registros = registros.filter(nome__icontains=nome)

    vacinas = paginar_registros(request, registros, 20)
    return render(request, "vacina.html",
                  locals())


@admin_member_required
@login_required()
def nova_vacina(request):
    form = VacinaForm(request.POST or None)
    myformset = VacinaEstoqueFormSet(request.POST or None)
    if request.POST:
        if form.is_valid():
            vacina = form.save()
            estoques = []
            for f in myformset:
                if f.is_valid():
                    if f.cleaned_data.get("estabelecimento") and f.cleaned_data.get("qtd"):
                        estoques.append(EstoqueVacina(vacina=vacina,
                                                    estabelecimento=f.cleaned_data.get("estabelecimento"),
                                                    qtd=f.cleaned_data.get("qtd")))
            EstoqueVacina.objects.bulk_create(estoques)
            messages.success(request, "Vacina cadastrada com sucesso.")
            return HttpResponseRedirect(reverse('vacinas'))
        else:
            messages.warning(request, "Verifique os dados passados")

    return render(request, "nova_vacina.html", locals())


@login_required()
def editar_vacina(request, id):
    vacina = get_object_or_404(Vacina, pk=id)
    form = VacinaForm(request.POST or None, instance=vacina)
    if request.session.get("perfil") == "coordenador":
        estoques = EstoqueVacina.objects.filter(vacina=vacina)
    elif request.session.get("perfil") == "profissional":
        form.fields["nome"].widget.attrs['readonly'] = True
        estoques = EstoqueVacina.objects.filter(vacina=vacina,
            estabelecimento=ProfissionalVinculo.objects.get(pk=request.session.get("vinculo_id")).estabelecimento)
    initial = [{"estabelecimento": e.estabelecimento,
                "qtd": e.qtd} for e in estoques]
    
    myformset = VacinaEstoqueFormSet(request.POST or None, initial=initial)
    
    if request.session.get("perfil") == "profissional":
        for f in myformset:
            vinculo = ProfissionalVinculo.objects.get(pk=request.session.get("vinculo_id"))
            f.fields["estabelecimento"].queryset = EstabelecimentoSaude.objects.filter(pk=vinculo.estabelecimento.id)
    
    if request.POST:
        if form.is_valid():
            vacina = form.save()
            cont = 0
            for f in myformset:
                if cont == 0 or request.session.get("perfil") == "coordenador":
                    if f.is_valid():
                        estoque = EstoqueVacina.objects.filter(estabelecimento=f.cleaned_data.get("estabelecimento"),
                                                                vacina=vacina)
                        if f.cleaned_data.get("estabelecimento"):
                            if estoque.exists():
                                estoque = estoque.first()
                                estoque.qtd = f.cleaned_data.get("qtd", 0)
                                estoque.save()
                            else:
                                EstoqueVacina.objects.create(vacina=vacina,
                                                        estabelecimento=f.cleaned_data.get("estabelecimento"),
                                                        qtd=f.cleaned_data.get("qtd", 0))
                    else:
                        # if f.cleaned_data.get("estabelecimento") or f.cleaned_data.get("qtd"):
                        messages.warning(request, "Verifique os dados passados")
                        return render(request, "nova_vacina.html", locals())
                cont += 1
            
            messages.success(request, "Vacina editada com sucesso.")
            return HttpResponseRedirect(reverse('vacinas'))
        else:
            messages.warning(request, "Verifique os dados passados")

    return render(request, "nova_vacina.html", locals())


@admin_member_required
@login_required()
def usuario(request):
    form = FiltroNomeForm(request.GET or None)
    registros = Usuario.objects.all()

    if request.GET and form.is_valid():
        nome = form.cleaned_data["nome"]
        if nome:
            registros = registros.filter(Q(user__first_name__icontains=nome)|Q(cpf__icontains=nome))

    usuarios = paginar_registros(request, registros, 20)
    return render(request, "usuario.html",
                  locals())


@admin_member_required
@login_required()
def novo_usuario(request):
    # Group.objects.create(name="Coordenador SUS")
    # Group.objects.create(name="Profissional Saude")
    form = NovoUsuarioForm(request.POST or None)
    myformset = VinculoFormSet(request.POST or None)
    if request.POST:
        if form.is_valid():
            usuario = form.save(commit=False)
            user = User.objects.create(username=form.cleaned_data.get("cpf"),
                                        password=make_password(form.cleaned_data.get("password1")),
                                        email=form.cleaned_data.get("email"),
                                        first_name=form.cleaned_data.get("nome"))
            if form.cleaned_data.get("grupo"):
                user.groups.add(form.cleaned_data.get("grupo"))

            usuario.user = user
            usuario.save()
            for f in myformset:
                if f.is_valid():
                    if f.cleaned_data.get("estabelecimento") and f.cleaned_data.get("ativo"):
                        ProfissionalVinculo.objects.create(
                            usuario=usuario,
                            estabelecimento=f.cleaned_data.get("estabelecimento"),
                            ativo=f.cleaned_data.get("ativo")
                        )

            messages.success(request, "Usuário cadastrado com sucesso.")
            return HttpResponseRedirect(reverse('usuarios'))
        else:
            messages.warning(request, "Verifique os dados passados")

    return render(request, "novo_usuario.html", locals())


@admin_member_required
@login_required()
def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, pk=id)
    form = NovoUsuarioForm(request.POST or None, instance=usuario,
                            initial={"nome":usuario.user.first_name,
                                    "grupo":usuario.user.groups.first(),
                                    "email":usuario.user.email })
    vinculos = ProfissionalVinculo.objects.filter(usuario=usuario)
    initial = [{"estabelecimento": e.estabelecimento,
                "ativo": e.ativo} for e in vinculos]
    myformset = VinculoFormSet(request.POST or None, initial=initial)
    if request.POST:
        if form.is_valid():
            usuario = form.save()
            user = usuario.user
            user.username=form.cleaned_data.get("cpf")
            if form.cleaned_data.get("password1"):
                user.password=make_password(form.cleaned_data.get("password1"))
            user.email=form.cleaned_data.get("email")
            user.first_name=form.cleaned_data.get("nome")
            user.save()

            user.groups.clear()
            if form.cleaned_data.get("grupo"):
                user.groups.add(form.cleaned_data.get("grupo"))

            for f in myformset:
                if f.is_valid():
                    if f.cleaned_data.get("estabelecimento"):
                        vinculo = ProfissionalVinculo.objects.filter(
                            usuario=usuario,
                            estabelecimento=f.cleaned_data.get("estabelecimento"),
                        )
                        if vinculo.exists():
                            vinculo = vinculo.first()
                            vinculo.ativo = f.cleaned_data.get("ativo")
                            vinculo.save()
                        else:
                            vinculo = ProfissionalVinculo.objects.create(
                            usuario=usuario,
                            estabelecimento=f.cleaned_data.get("estabelecimento"),
                            ativo = f.cleaned_data.get("ativo")
                        )
                else:
                    print("form nao eh valido")
            messages.success(request, "Usuário editado com sucesso.")
            return HttpResponseRedirect(reverse('usuarios'))
        else:
            messages.warning(request, "Verifique os dados passados")

    return render(request, "novo_usuario.html", locals())


def login_aplicacao(request):
    """
    # Caso o usuário esteja autenticado, é redirecionado para página principal
    if request.user.is_authenticated:
        save_log_access(request, request.user)

        if request.user.is_superuser:
            return HttpResponseRedirect(reverse('administracao:index'))
        else:
            return HttpResponseRedirect(reverse('comum:index'))
    """

    form = AuthenticationForm(request)

    if request.POST:
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            coordenador, e = Group.objects.get_or_create(name="Coordenador SUS")
            profissinoal, e = Group.objects.get_or_create(name="Profissional Saude")

            if coordenador in request.user.groups.all():
                request.session["perfil"] = "coordenador"
            elif profissinoal in request.user.groups.all() and request.user.usuario.vinculos.filter(ativo=True).exists():
                request.session["perfil"] = "profissional"
                request.session["vinculo_id"] = request.user.usuario.vinculos.filter(ativo=True).first().id
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.warning(request, "Login/senha incorretos ou seu login está inativo")

    return render(request, 'login.html', locals())


def logout_aplicacao(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_aplicacao'))


@login_required
def index(request):
    coordenador, e = Group.objects.get_or_create(name="Coordenador SUS")
    profissinoal, e = Group.objects.get_or_create(name="Profissional Saude")

    if coordenador in request.user.groups.all():
        request.session["perfil"] = "coordenador"
    elif profissinoal in request.user.groups.all() and request.user.usuario.vinculos.filter(ativo=True).exists():
        request.session["perfil"] = "profissional"
        if not request.session.get("vinculo_id"):
            request.session["vinculo_id"] = request.user.usuario.vinculos.filter(ativo=True).first().id

    if request.session.get("perfil") == "profissional":
        return HttpResponseRedirect(reverse('fila_agendamento'))
    elif request.session.get("perfil") == "coordenador":
        return HttpResponseRedirect(reverse('relatorios'))
    else:
        return HttpResponseRedirect(reverse('fila_agendamento'))
    return render(request, 'index.html', locals())


@profissional_member_required
def alterar_vinculo(request):
    vinculos = ProfissionalVinculo.objects.filter(usuario=request.user.usuario, ativo=True)
    if request.GET.get("vinculo_id"):
        request.session["vinculo_id"] = request.GET.get("vinculo_id")
        messages.success(request, "Vínculo alterado.")
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'vinculos.html', locals())


def cadastro(request):
    form = NovoUsuarioExternoForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            usuario = form.save(commit=False)
            user = User.objects.create(username=form.cleaned_data.get("cpf"),
                                        password=make_password(form.cleaned_data.get("password1")),
                                        email=form.cleaned_data.get("email"),
                                        first_name=form.cleaned_data.get("nome"))
            usuario.user = user
            usuario.save()
            mensagem = """
                Prezado(a) %s,
                O seu seu cadastro no Sistema de Vacinação foi registrado.
                O seu NOME DE USUÁRIO é o seu CPF.
            
            """%(user.first_name)
            send_mail(u'Cadastro no Sistema de Vacinação',
                    mensagem,
                  u'lais.ufrn@gmail.com', [user.email], fail_silently=False)
            messages.success(request, "Usuário cadastrado com sucesso.")
            return HttpResponseRedirect(reverse('login_aplicacao'))
        else:
            messages.warning(request, "Verifique os dados passados")
    return render(request, 'cadastro.html', locals())


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def relatorios(request):
    # estoque = EstoqueVacina.objects.values('estabelecimento__nome_fantasia', 'vacina__nome').annotate(total=Sum('qtd'))
    # agendamento = Agendamento.objects.filter(data__date__month=datetime.now().month, data__date__year=datetime.now().year, aplicado=True).values('estabelecimento__municipio__nome','estabelecimento__municipio__estado__sigla').annotate(total=Count('estabelecimento__municipio__nome'))
    if request.session.get("perfil") == "coordenador":
        with connection.cursor() as cursor:
            sql = """SELECT "administracao_estabelecimentosaude"."nome_fantasia",
                    "administracao_vacina"."nome", SUM("administracao_estoquevacina"."qtd")
                    AS "total" FROM "administracao_estoquevacina"
                    INNER JOIN "administracao_estabelecimentosaude" ON
                    ("administracao_estoquevacina"."estabelecimento_id" =
                    "administracao_estabelecimentosaude"."id")
                    INNER JOIN "administracao_vacina" ON
                    ("administracao_estoquevacina"."vacina_id" = "administracao_vacina"."id")
                    GROUP BY "administracao_estabelecimentosaude"."nome_fantasia", "administracao_vacina"."nome"
                """
            cursor.execute(sql)
            a = dictfetchall(cursor)
            graficos = {}
            for row in a:
                if not graficos.get(row["nome"]):
                    graficos[row["nome"]] = []
                graficos[row["nome"]].append({
                    "name": row["nome_fantasia"],
                    "y":row["total"]})

            sql = """SELECT "administracao_municipio"."nome", "administracao_unidadefederativa"."sigla",
                COUNT("administracao_municipio"."nome") AS "total" FROM "agendamento_agendamento"
                INNER JOIN "administracao_estabelecimentosaude" ON
                ("agendamento_agendamento"."estabelecimento_id" = "administracao_estabelecimentosaude"."id")
                INNER JOIN "administracao_municipio" ON ("administracao_estabelecimentosaude"."municipio_id"
                = "administracao_municipio"."id") INNER JOIN "administracao_unidadefederativa"
                ON ("administracao_municipio"."estado_id" = "administracao_unidadefederativa"."codigo")
                WHERE ("agendamento_agendamento"."aplicado"
                AND EXTRACT('month' FROM ("agendamento_agendamento"."data"
                AT TIME ZONE 'UTC')::date) = """+str(datetime.now().month)+""" AND ("agendamento_agendamento"."data"
                AT TIME ZONE 'UTC')::date BETWEEN to_date('"""+str(datetime.now().year)+"""-01-01','YYYY-MM-DD') AND to_date('"""+str(datetime.now().year)+"""-12-31','YYYY-MM-DD'))
                GROUP BY "administracao_municipio"."nome", "administracao_unidadefederativa"."sigla"
                """
            cursor.execute(sql)
            a = dictfetchall(cursor)
            graficos_barra = [[],[]]
            for row in a:
                graficos_barra[0].append("%s/%s"%(row["nome"],row["sigla"]))
                graficos_barra[1].append(row["total"])
        return render(request, 'relatorios_coord.html', locals())
    elif request.session.get("perfil") == "profissional":
        estabelecimento = ProfissionalVinculo.objects.get(pk=request.session["vinculo_id"]).estabelecimento
        # estoque = EstoqueVacina.objects.filter(estabelecimento=estabelecimento).values('vacina__nome').annotate(total=Sum('qtd'))
        # agendamento = Agendamento.objects.filter(data__date__month=datetime.now().month, data__date__year=datetime.now().year, aplicado=True, estabelecimento=estabelecimento).values('vacina__nome').annotate(total=Count('vacina__nome'))
        with connection.cursor() as cursor:
            sql = """
                    SELECT "administracao_vacina"."nome", SUM("administracao_estoquevacina"."qtd")
                    AS "total" FROM "administracao_estoquevacina" INNER JOIN "administracao_vacina"
                    ON ("administracao_estoquevacina"."vacina_id" = "administracao_vacina"."id")
                    WHERE "administracao_estoquevacina"."estabelecimento_id" = """+str(estabelecimento.id)+"""
                    GROUP BY "administracao_vacina"."nome"
            """
            cursor.execute(sql)
            a = dictfetchall(cursor)
            graficos = {}
            for row in a:
                if not graficos.get("Vacinas"):
                    graficos["Vacinas"] = []
                graficos["Vacinas"].append({
                    "name": row["nome"],
                    "y":row["total"]})

            graficos_barra = [[],[]]
            sql = """
                    SELECT "administracao_vacina"."nome", COUNT("administracao_vacina"."nome")
                    AS "total" FROM "agendamento_agendamento" INNER JOIN "administracao_vacina"
                    ON ("agendamento_agendamento"."vacina_id" = "administracao_vacina"."id")
                    WHERE ("agendamento_agendamento"."aplicado"
                    AND EXTRACT('month' FROM ("agendamento_agendamento"."data" AT TIME ZONE 'UTC')::date) = """+str(datetime.now().month)+"""
                    AND ("agendamento_agendamento"."data" AT TIME ZONE 'UTC')::date
                    BETWEEN to_date('"""+str(datetime.now().year)+"""-01-01','YYYY-MM-DD') AND to_date('"""+str(datetime.now().year)+"""-12-31','YYYY-MM-DD')
                    AND "agendamento_agendamento"."estabelecimento_id" = """+str(estabelecimento.id)+""")
                    GROUP BY "administracao_vacina"."nome"
            """

            cursor.execute(sql)
            a = dictfetchall(cursor)
            graficos_barra = [[],[]]
            for row in a:
                graficos_barra[0].append(row["nome"])
                graficos_barra[1].append(row["total"])

        return render(request, 'relatorios_prof.html', locals())


