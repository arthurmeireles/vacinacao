from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from .serializers import *
from .models import *
from rest_framework.decorators import action
from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.authtoken.models import Token
import json


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,]


@api_view(['POST'])
@authentication_classes((SessionAuthentication, TokenAuthentication, BasicAuthentication))
@permission_classes((IsAdminUser,))
def auth_test(request):
    received_json_data=json.loads(request.body)
    print(received_json_data)
    cpf = received_json_data.get("cpf")
    email = received_json_data.get("email")
    name = received_json_data.get("name")
    usuario = User.objects.filter(last_name=cpf)
    if not usuario.exists():
        usuario = User.objects.create(username=email.split("@")[0],
                                        email=email,
                                        first_name=name,
                                        last_name=cpf)
    else:
        usuario = usuario.first()
    token, created = Token.objects.get_or_create(user=usuario)

    retorno = {
        "token": token.key,
        "id": usuario.id,
        "user": UserSerializer(instance=usuario).data
    }

    return Response(retorno)



# class DuvidaViewSet(viewsets.ModelViewSet):
#     queryset = Duvida.objects.all().order_by("-id")
#     serializer_class = DuvidaSerializer
#     permission_classes = [IsAuthenticated,]

#     @action(
#         methods=['get'],
#         detail=False,
#     )
#     @transaction.atomic()
#     def em_alta(self, request, *args, **kwargs):
#         duvidas = Duvida.objects.all().order_by("-likes")
#         retorno = DuvidaSerializer(instance=duvidas, many=True)
#         return Response(retorno.data)

#     @action(
#         methods=['get'],
#         detail=False,
#     )
#     @transaction.atomic()
#     def like(self, request, *args, **kwargs):
#         if request.GET.get("duvida_id", None):
#             duvida = Duvida.objects.get(pk=request.GET.get("duvida_id"))
#             autor = User.objects.get(username=request.user)
#             if autor in duvida.dislikes_autores.all():
#                 duvida.dislikes_autores.remove(autor)
#                 duvida.dislikes -= 1
#             if autor not in duvida.likes_autores.all():
#                 duvida.likes_autores.add(autor)
#                 duvida.likes += 1
#             else:
#                 duvida.likes_autores.remove(autor)
#                 duvida.likes -= 1
#             duvida.save()
#             checar_novas_medalhas_pergunta(duvida.autor)
#             checar_novas_medalhas_pergunta(autor)
#             retorno = DuvidaSerializer(instance=duvida)
#             return Response(retorno.data)
#         return Response({})


#     @action(
#         methods=['get'],
#         detail=False,
#     )
#     @transaction.atomic()
#     def dislike(self, request, *args, **kwargs):
#         duvida = Duvida.objects.get(pk=request.GET.get("duvida_id"))
#         autor = User.objects.get(username=request.user)
#         if autor in duvida.likes_autores.all():
#             duvida.likes_autores.remove(autor)
#             duvida.likes -= 1
#         if autor not in duvida.dislikes_autores.all():
#             duvida.dislikes_autores.add(autor)
#             duvida.dislikes += 1
#         else:
#             duvida.dislikes_autores.remove(autor)
#             duvida.dislikes -= 1
#         duvida.save()
#         retorno = DuvidaSerializer(instance=duvida)
#         return Response(retorno.data)

#     @action(
#         methods=['get'],
#         detail=False,
#     )
#     @transaction.atomic()
#     def minhas_duvidas(self, request, *args, **kwargs):
#         duvidas = Duvida.objects.filter(autor=request.user)
#         if duvidas.exists():
#             retorno = DuvidaSerializer(instance=duvidas, many=True).data
#         else:
#             retorno = {}
#         return Response(retorno)