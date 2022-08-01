from django.urls import re_path
import beneficio.views

urlpatterns = [
    re_path(r'^login$', beneficio.views.Login.as_view(), name='login'),
    re_path(r'^revendedor/cadastro$', beneficio.views.CadastraRevendedor.as_view(), name='cadastro_revendedor'),
    re_path(r'^compra', beneficio.views.CompraRevendedor.as_view(), name='compra_revendedor'),
    re_path(r'^acumulado/cashback', beneficio.views.AcumuladoCashback.as_view(), name='acumulado_cashback'),
]
