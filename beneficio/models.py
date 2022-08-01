from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


# Create your models here.
class Revendedor(AbstractBaseUser):
    """
    :Name: Revendedor
    :description: Define informações básicas de um revendedor
    :Criação:
    :Edições:
    """
    objects = BaseUserManager()

    cpf = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=200, unique=True)
    USERNAME_FIELD = 'username'
    nm_completo = models.CharField(max_length=250, null=True)
    email = models.CharField(max_length=60, null=True)

    class Meta:
        db_table = 'revendedor'


class CompraRevendedor(models.Model):
    class Status(models.TextChoices):
        APROVADO = ('aprovado', 'Aprovado')
        EM_VALIDACAO = ('em_validacao', 'Em validação')

    revendedor = models.ForeignKey('beneficio.Revendedor', on_delete=models.DO_NOTHING)
    codigo = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=14, decimal_places=2)
    data = models.DateField()
    referencia = models.IntegerField(null=True)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.EM_VALIDACAO)

    class Meta:
        db_table = 'compra_revendedor'



