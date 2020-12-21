# Teleconsultoria 2.0

Caso seu computador não esteja configurado para desenvolver projetos Django use o [tutorial](https://github.com/jdoper/config_python).

## Configurando seu ambiente

Realize o clone do projeto e entre no diretório baixado

```sh
git clone http://git.lais.huol.ufrn.br/telessaude/teleconsultoria2.0.git
cd teleconsultoria2.0
```

Crie uma nova virtualenv (o exemplo abaixo é feito usando virtualenvwrapper):

```sh
mkvirtualenv teleconsultoria2
```

Instale as dependências:

```sh
workon teleconsultoria2
pip install -r requirements.txt
```

## Configurando o banco de dados

Crie um novo banco de dados:

```sh
sudo -u postgres psql -U postgres -c "CREATE DATABASE teleconsultoria2;"
```

Crie as tabelas do projeto:

```sh
python manage.py migrate
```

Insira os dados iniciais para o banco de dados da aplicação:

```sh
sudo -u postgres psql -U postgres -d teleconsultoria2 -a -f initial_data.sql
```

Sincronize o banco:

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