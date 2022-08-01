import json
from datetime import datetime, timedelta

import requests
from django.contrib.auth import authenticate
from django.db.models import Sum
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

import beneficio.models


class Revendedor:
    def __init__(self, cpf=None, senha=None):
        self.cpf = cpf
        if self.cpf:
            self.cpf = self.cpf.replace('.', '').replace('-', '')
        self.senha = senha

    def set_revendedor(self, nm_completo=None, email=None):
        if not self.cpf or not self.senha or not nm_completo or not email:
            response = {
                'status': False,
                'descricao': 'Todos os campos são obrigatórios'
            }
            return response

        revendedor = beneficio.models.Revendedor.objects.filter(cpf=self.cpf).first()

        if revendedor:
            response = {
                'status': False,
                'descricao': 'Revendedor já cadastrado'
            }
            return response

        revendedor = beneficio.models.Revendedor()
        revendedor.nm_completo = nm_completo
        revendedor.email = email
        revendedor.cpf = self.cpf
        revendedor.username = self.cpf
        revendedor.set_password(self.senha)
        revendedor.save()

        response = {
            'status': True,
            'revendedor_id': revendedor.pk
        }

        return response

    def set_compra(self, codigo=None, valor=None, data=None):
        if not self.cpf:
            response = {
                'status': False,
                'descricao': 'É preciso fornecedor o CPF do revendedor'
            }
            return response

        compra = beneficio.models.CompraRevendedor()

        revendedor = self._get_revendedor()
        if not revendedor:
            response = {
                'status': False,
                'descricao': 'Revendedor não cadastrado'
            }
            return response

        compra.revendedor = self._get_revendedor()
        compra.codigo = codigo
        compra.valor = valor
        if self.cpf in ['15350946056']:
            compra.status = 'aprovado'
        compra.data = data
        # Criação do campo referência para simplificar o cálculo na busca de compras e total de cashback
        dat_compra_date = self._data_to_datetime(data)
        referencia_ano = dat_compra_date.year
        referencia_mes = dat_compra_date.month
        compra.referencia = referencia_ano * 100 + referencia_mes
        compra.save()

        response = {
            'status': True,
        }

        return response

    def get_compras_revendedor(self):
        if not self.cpf:
            response = {
                'status': False,
                'descricao': 'É preciso fornecedor o CPF do revendedor'
            }
            return response

        compras = beneficio.models.CompraRevendedor.objects.values('codigo', 'data', 'valor', 'status', 'referencia').filter(revendedor__cpf=self.cpf)

        aux = compras.values('referencia').annotate(total=Sum('valor'))
        total_mes = {i['referencia']: i['total'] for i in aux}

        for compra in compras:
            if total_mes[compra['referencia']] <= 1000:
                compra['perc_cashback'] = '10%'
                compra['vlr_cashback'] = float(compra['valor']) * 0.1

            if 1000 < total_mes[compra['referencia']] <= 1500:
                compra['perc_cashback'] = '15%'
                compra['vlr_cashback'] = float(compra['valor']) * 0.15

            if total_mes[compra['referencia']] > 1500:
                compra['perc_cashback'] = '20%'
                compra['vlr_cashback'] = float(compra['valor']) * 0.2

        response = {
            'status': True,
            'compras': list(compras)
        }
        return response

    def get_acumulado(self):
        if not self.cpf:
            response = {
                'status': False,
                'descricao': 'É preciso fornecedor o CPF do revendedor'
            }
            return response

        if not self._get_revendedor():
            response = {
                'status': False,
                'descricao': 'Revendedor não cadastrado'
            }
            return response

        headers = {'token': 'ZXPURQOARHiMc6Y0flhRC1LVlZQVFRnm', 'content-type': 'application/json'}
        url = 'https://mdaqk8ek5j.execute-api.us-east-1.amazonaws.com/v1/cashback'
        data = {
            'cpf': self.cpf
        }
        total_boticario = requests.get(url=url, params=data, headers=headers)
        response_boticario = json.loads(total_boticario.content)

        total_acumulado = beneficio.models.CompraRevendedor.objects.filter(revendedor__cpf=self.cpf).aggregate(total=Sum('valor'))

        response = {
            'status': True,
            'api_boticario': response_boticario,
            'total_calculado': float(total_acumulado['total']) if total_acumulado['total'] else 0
        }

        return response

    def _get_revendedor(self):
        revendedor = beneficio.models.Revendedor.objects.filter(cpf=self.cpf).first()

        return revendedor

    def _data_to_datetime(self, anomesdiaformatado, formato='%Y-%m-%d'):
        try:
            return datetime.strptime(anomesdiaformatado, formato)
        except Exception as e:
            print(e)
            return None


class LoginApiSerializer(TokenObtainPairSerializer):
    """
    :Nome da classe/função: LoginApiSerializer
    :Descrição: Classe de serialização do login da API
    :Criação: Lucas Penha de Moura - 25/07/2022
    :Edições:
    """

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def validate(self, attrs):
        """
        :Nome da classe/função: validate
        :Descrição: Função para validação do username/senha fornecidos para autenticação na API
        :Criação: Lucas Penha de Moura - 25/07/2022
        :Edições:
        """
        try:
            request = self.context["request"]
        except KeyError:
            raise serializers.ValidationError({'error': 'Houve um erro na autenticação'})

        if request:
            request_data = request.data
        else:
            raise serializers.ValidationError({'error': 'Houve um erro na autenticação'})

        if "username" in request_data and "password" in request_data:
            username = request_data['username'].replace('.', '').replace('-', '')
            user = authenticate(username=username, password=request_data['password'])

            if not user:
                raise serializers.ValidationError({'error': 'Usuário ou senha inválidos'})

            refresh = self.get_token(user=user)
            data = {
                'expire': datetime.now() + timedelta(days=1),
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }

            return data

        else:
            raise serializers.ValidationError({'error': 'Usuário e senhas são campos obrigatórios'})


class Login(LoginApiSerializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def get_serializer_class(self):
        pass

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['user'] = user.username
        token['usr_info'] = ''

        return token
