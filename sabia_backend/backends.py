# coding: utf-8

from social.backends.oauth import BaseOAuth2

from administracao.models import Usuario, ProfissionalVinculo, EstabelecimentoSaude

from django.contrib.auth.models import User, Group

class SabiaOAuth2(BaseOAuth2):
    name = 'sabia'
    AUTHORIZATION_URL = 'https://login.sabia.ufrn.br/oauth/authorize/'
    ACCESS_TOKEN_METHOD = 'POST'
    ACCESS_TOKEN_URL = 'https://login.sabia.ufrn.br/oauth/token/'
    ID_KEY = 'cpf'
    RESPONSE_TYPE = 'code'
    REDIRECT_STATE = True
    STATE_PARAMETER = True
    USER_DATA_URL = 'https://login.sabia.ufrn.br/api/perfil/dados/'

    def add_cpf_mask(self, cpf):
        return cpf[0:3] + "." + cpf[3:6] + "." + cpf[6:9] + "-" + cpf[9:11]

    def remove_cpf_mask(self, cpf):
        return cpf.replace('.', '').replace('-', '')

    def get_sexo(self, sexo):
        switcher = {
            "F": 1,
            "M": 2,
        }
        return switcher.get(sexo, 3)

    def user_data(self, access_token, *args, **kwargs):
        return self.request(
            url=self.USER_DATA_URL,
            data={'scope': kwargs['response']['scope']},
            method='POST',
            headers={'Authorization': 'Bearer {0}'.format(access_token)}
        ).json()

    def get_user_details(self, response):
        """
        Retorna um dicionário mapeando os fields do settings.AUTH_USER_MODEL.
        você pode fazer aqui outras coisas, como salvar os dados do usuário
        (`response`) em algum outro model.
        """
        splitted_name = response['name'].split()
        first_name, last_name = splitted_name[0], ''

        if len(splitted_name) > 1:
            last_name = splitted_name[-1]
        return {
            'username': response['cpf'],
            'first_name': first_name.strip(),
            'last_name': last_name.strip(),
            'email': response['email'],
        }

    def extra_data(self, user, uid, response, details=None, *args, **kwargs):
        # cpf = self.add_cpf_mask(self.remove_cpf_mask(response['cpf']))
        # print(response)
        u = User.objects.get(username=response['cpf'])
        u.first_name = response['name']
        u.save()

        ps = Usuario.objects.filter(cpf=response['cpf'])

        if not ps.exists():
            ps = Usuario.objects.create(
                user=User.objects.get(username=response['cpf']),
                cpf=response['cpf'],
            )

        return super(SabiaOAuth2, self).extra_data(user, uid, response, details, *args, **kwargs)
