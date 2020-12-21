"""vacinacao URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from administracao.viewsets import *
from administracao.views import *
from agendamento.views import *
from cartao_vacina.views import *
from rest_framework import routers, serializers, viewsets
from administracao.select2_utils import *

router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
# router.register(r'duvidas', DuvidaViewSet)
# router.register(r'respostas', RespostaViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', index, name='index'),
    path('', include('social.apps.django_app.urls', namespace='social')),
    path('relatorios/', relatorios, name='relatorios'),
    # path('sabia', auth_test),
    path('accounts/login/', login_aplicacao, name='login_aplicacao'),
    path('accounts/logout/', logout_aplicacao, name='logout_aplicacao'),
    path('cadastro/', cadastro, name='cadastro'),

    path('estabelecimentos/', estabelecimento_saude, name='estabelecimentos'),
    path('estabelecimentos/novo/', novo_estabelecimento, name='novo_estabelecimento'),
    path('estabelecimentos/<int:id>/', ver_estabelecimento, name='ver_estabelecimento'),
    path('estabelecimentos/editar/<int:id>/', editar_estabelecimento, name='editar_estabelecimento'),
    path('estabelecimentos/upload_csv/', upload_csv, name='upload_csv'),
    path('select2/', include('django_select2.urls')),

    path('municipios/', municipio, name='municipios'),
    path('municipios/novo/', novo_municipio, name='novo_municipio'),
    path('municipios/<int:id>/', ver_municipio, name='ver_municipio'),
    path('municipios/editar/<int:id>/', editar_municipio, name='editar_municipio'),

    path('vacinas/', vacina, name='vacinas'),
    path('vacinas/nova/', nova_vacina, name='nova_vacina'),
    # path('municipios/<int:id>/', ver_municipio, name='ver_municipio'),
    path('vacinas/editar/<int:id>/', editar_vacina, name='editar_vacina'),

    path('usuarios/', usuario, name='usuarios'),
    path('usuarios/novo/', novo_usuario, name='novo_usuario'),
    # path('municipios/<int:id>/', ver_municipio, name='ver_municipio'),
    path('usuarios/editar/<int:id>/', editar_usuario, name='editar_usuario'),
    path('usuarios/alterar_vinculo/', alterar_vinculo, name='alterar_vinculo'),

    path('horarios/', horario_estabelecimento, name='horario_estabelecimento'),
    path('horarios/editar/<int:vacina_id>/', editar_horario, name='editar_horario'),

    path('agendamentos/', agendamento, name='agendamentos'),
    path('agendamentos/fila/', fila_agendamento, name='fila_agendamento'),
    path('agendamentos/chamar/<int:id>/', chamar_fila, name='chamar_fila'),
    path('agendamentos/fila/json/', fila_agendamento_json, name='fila_agendamento_json'),
    path('novo_agendamento/', agendar_vacinacao, name='novo_agendamento'),

    path('cartao_vacina/', cartao_vacina, name='cartao_vacina'),
    path('cartao_vacina/cadastrar', cadastrar_vacina_privada, name='cadastrar_vacina_privada'),

    path('select2/buscar/municipio/', buscar_municipio, name="buscar_municipio"),
    path('select2/buscar/vacina/', buscar_vacina, name="buscar_vacina"),
    path('select2/buscar/estabelecimento/', buscar_estabelecimento, name="buscar_estabelecimento"),
    path('select2/buscar/data/', buscar_data, name="buscar_data"),
    # path('select2/buscar/categorias_cbo/', buscar_categoria_cbo, name="buscar_categoria_cbo"),
    # path('select2/buscar/cbos/', buscar_especialidade, name="buscar_especialidade"),
    # path('select2/buscar/cids/', buscar_cid, name="buscar_cid"),
    # path('select2/buscar/ciaps/', buscar_ciap, name="buscar_ciap"),
    # path('select2/buscar/usuario/', buscar_usuario, name="buscar_usuario"),
    # path('select2/buscar/profissional/', buscar_profissional, name="buscar_profissional"),


]
