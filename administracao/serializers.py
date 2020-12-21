from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from administracao.models import *

# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff']

    def to_representation(self, instance):
        data = super(UserSerializer, self).to_representation(instance)
        retorno = {
            "username": instance.username,
            "email": instance.email,
            "medalhas": {"ouro": [],
                            "prata": [],
                            "bronze": []}
        }
        
        return retorno


# class DuvidaSerializer(serializers.ModelSerializer):
#     tags = serializers.PrimaryKeyRelatedField(many=True, read_only=True, required=False)
#     likes_autores = serializers.PrimaryKeyRelatedField(many=True, read_only=True, required=False)
#     dislikes_autores = serializers.PrimaryKeyRelatedField(many=True, read_only=True, required=False)

#     class Meta:
#         model = Duvida
#         fields = "__all__"

#     def create(self, validated_data):
#         duvida = Duvida.objects.create(**validated_data)
#         checar_novas_medalhas_pergunta(duvida.autor)
#         return duvida

#     def to_representation(self, instance):
#         data = super(DuvidaSerializer, self).to_representation(instance)
#         retorno = {
#                 "id": instance.id,
#                 "titulo": instance.titulo,
#                 "descricao": instance.descricao,
#                 "likes": instance.likes,
#                 "dislikes": instance.dislikes,
#                 "likes_autores": list(instance.likes_autores.values_list("id")),
#                 "dislikes_autores": list(instance.dislikes_autores.values_list("id")),
#                 "autor":UserSerializer(instance.autor).data,
#                 "respostas": {
#                     "lista": RespostaSerializer(instance.respostas.all().order_by("-id"), many=True).data
#                 }
#         }
#         retorno["likes_autores"] = [i[0] for i in retorno["likes_autores"]]
#         retorno["dislikes_autores"] = [i[0] for i in retorno["dislikes_autores"]]
#         if len(instance.respostas.all()) > 0:
#             retorno["respostas"]["destaque"] = RespostaSerializer(instance.respostas.all().order_by("-likes")[0]).data
#         else:
#             retorno["respostas"]["destaque"] = None

#         return retorno