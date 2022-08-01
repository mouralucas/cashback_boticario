import json

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

import BO.revendedor

URL = reverse('login')
TOKEN = None


class TestCriacaoRevendedor(APITestCase):
    def setUp(self):
        teste_user = self.client.post(URL, {'username': '111.111.111-11', 'password': '123'})
        self.teste_token = teste_user.json()['access']

    def test_criacao(self):
        revendedor = BO.revendedor.Revendedor(cpf='111.112.111-12', senha='123').set_revendedor(nm_completo='Nome de teste', email='email@gmail.com')
        self.assertTrue(revendedor['status'])

        revendedor2 = BO.revendedor.Revendedor(cpf='111.112.111-12', senha='354').set_revendedor(nm_completo='Nome de teste')
        self.assertFalse(revendedor2['status'])

    def test_login(self):
        # Testa o login sem um dos parâmetros
        response = self.client.post(URL, {'username': 'new idea'}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['password'], ['This field is required.'])

        response_2 = self.client.post(URL, {'password': 'pass'}, format='json')
        self.assertEqual(response_2.status_code, 400)
        self.assertEqual(json.loads(response_2.content)['username'], ['This field is required.'])

        response_3 = self.client.post(URL, {'username': 'teste', 'password': 'pass_teste'})
        self.assertIn('error', json.loads(response_3.content))

        response_4 = self.client.post(URL, {'username': '111.111.111-11', 'password': '123'})
        self.assertIn('access', response_4.json())

    def test_cadastro_compra(self):
        url_compra = reverse('compra_revendedor')
        response = self.client.post(url_compra, {'cpf': '111.111.111-11', 'codigo': 'T1', 'data': '2022-07-27', 'valor': 80.78})
        self.assertEqual(response.status_code, 401)

        response_2 = self.client.post(url_compra, params={'cpf': '11111111111', 'codigo': 'T1', 'data': '2022-07-27', 'valor': 80.78},
                                      content_type='application/x-www-form-urlencoded', **{'HTTP_AUTHORIZATION': f'Bearer {self.teste_token}'})
        print(json.loads(response_2.content)['descricao'])
        self.assertEqual(response_2.status_code, 200)
