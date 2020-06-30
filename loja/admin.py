from django.contrib import admin

from .models import Categorias, Produtos, Pedidos
# Register your models here.

admin.site.register(Categorias)
admin.site.register(Produtos)
admin.site.register(Pedidos)
