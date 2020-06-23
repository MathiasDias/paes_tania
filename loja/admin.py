from django.contrib import admin

from .models import Categorias, Produtos
# Register your models here.

admin.site.register(Categorias)
admin.site.register(Produtos)
