from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

import BO.revendedor
import BO.revendedor


class Login(TokenObtainPairView):
    """
    :Nome da classe/função: Login
    :Descrição: View de login do vendedor
    :Criação: Lucas Penha de Moura - 27/07/2022
    :Edições:
    """
    serializer_class = BO.revendedor.Login


class CadastraRevendedor(APIView):
    """
    :Nome da classe/função: CadastraRevendedor
    :Descrição: View para cadastro do revendedor
    :Criação: Lucas Penha de Moura - 27/07/2022
    :Edições:
    """

    def post(self, *args, **kwargs):
        cpf = self.request.POST.get('cpf')
        nm_completo = self.request.POST.get('nm_completo')
        email = self.request.POST.get('email')
        senha = self.request.POST.get('senha')

        response = BO.revendedor.Revendedor(cpf=cpf, senha=senha).set_revendedor(nm_completo=nm_completo, email=email)

        return JsonResponse(response, safe=False)


class CompraRevendedor(APIView):
    permission_classes = [IsAuthenticated]

    """
    :Nome da classe/função: CompraRevendedor - get
    :Descrição: View para busca de compras do revendedor
    :Criação: Lucas Penha de Moura - 27/07/2022
    :Edições:
    """

    def get(self, *args, **kwargs):
        cpf = self.request.GET.get('cpf')

        response = BO.revendedor.Revendedor(cpf=cpf).get_compras_revendedor()

        return JsonResponse(response, safe=False)

    """
    :Nome da classe/função: CompraRevendedor - post
    :Descrição: View para cadastro de compra do revendedor
    :Criação: Lucas Penha de Moura - 27/07/2022
    :Edições:
    """

    def post(self, *args, **kwargs):
        codigo = self.request.POST.get('codigo')
        valor = self.request.POST.get('valor')
        data = self.request.POST.get('data')
        cpf = self.request.POST.get('cpf')

        response = BO.revendedor.Revendedor(cpf=cpf).set_compra(codigo=codigo, valor=valor, data=data)

        return JsonResponse(response, safe=False)


class AcumuladoCashback(APIView):
    def get(self, *args, **kwargs):
        cpf = self.request.GET.get('cpf')

        response = BO.revendedor.Revendedor(cpf=cpf).get_acumulado()

        return JsonResponse(response, safe=False)
