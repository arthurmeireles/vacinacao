# Sistema de vacinacao

## Configurando seu ambiente

Realize o clone do projeto e entre no diretório baixado

```sh
git clone https://github.com/beatriz-soares/vacinacao.git
cd vacinacao
```

Crie uma nova virtualenv (o exemplo abaixo é feito usando virtualenvwrapper):

```sh
mkvirtualenv vacinacao
```

Instale as dependências:

```sh
workon vacinacao
pip install -r requirements.txt
```

## Configurando o banco de dados

Crie um novo banco de dados:

```sh
sudo -u postgres psql -U postgres -c "CREATE DATABASE vacinacao;"
```

Ajuste nas settings o username e senha do seu database

```sh
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'vacinacao',
        'USER': "seu_user",
        'PASSWORD': "sua_senha",
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Crie as tabelas do projeto:

```sh
python manage.py migrate
```

#### **PRONTO!!!** Seu ambiente está configurado para executar a aplicação.

## Observações

A aplicação já vem com três usuários:

* cap-solicitante
* cap-regulador
* cap-especialista

Todos os três usuários possuem senha 'treinamento' (sem as aspas). Caso deseje, crie um administrador.

```sh
python manage.py createsuperuser
```