# Cashback Revendedor Boticário

Este código pode ser usado para fazer cadastro de novos revendedores para participar do programa de benefícios de cashback do Boticário.

A solução utiliza o Django Rest Framework para simplificar a criação dos endpoints previstos. Também foi usado a biblioteca SimpleJWT que implementa a 
validação de usuários do Django Rest Framework utilizando tokens JWT.

**Obs: Para fim de avaliação foi mantido o database sqlite no commit, por conter informações básicas para pesquisa e simplificar os testes.**

## Instalação

Para a solução foi usado o Python Virtual Enviroment (venv)

A instalação é descrita abaixo, na raiz do projeto:

Para Windows 10:

```bash
python -m venv venv
venv\Scripts\activate
```

Para Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

Para instalação dos requisitos, use a função PIP, como descrito abaixo, com a venv ativada:

```bash
pip install -r requirements.txt (Windows)
pip3 install -r requirements.txt (Linux)
```

Os requisitos necessários estão descritos abaixo:

- djangorestframework
- djangorestframework-simplejwt==5.0.0
- django==3.2
- psycopg2-binary==2.8.4 (caso seja usado PostgreSQL como database)
- requests

Para rodar o projeto:

```bash
python manage.py runserver (Windows)
python3 manage.py runserver (Linux)
```

## Uso

Para usar os endpoints desenvolvos o Postman pode ser usado através das URLs descritas.

**Método:** GET
- /compra (endpoint para buscar as compras feitas por um CPF)
- /acumulado/cashback (busca o cashback acumulado para um cashback)

**Método:** POST
- /compra (endpoint para salvar as compras feitas por um CPF)
- /login (realiza o login de um revendedor, retornando o token JWT caso seja válido)
- /revendedor/cadastro (realiza o cadastro de um novo revendedor)


## Testes

Para rodar os testes bas executar o comando abaixo diretamente no terminal:

```bash
python manage.py test --keepdb (Windows)
python3 manage.py test --keepdb (Linux)
```