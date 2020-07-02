from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Categorias(models.Model):
    Nome = models.CharField(max_length=30)

    def __str__(self):
        return self.Nome

class Produtos(models.Model):
    disponivel_escolha = [
    ('Sim','Sim'),
    ('Não','Não'),
    ]
    Nome = models.CharField(max_length=128)
    Categoriateste = models.ForeignKey(Categorias ,on_delete=models.CASCADE, default=0)
    Descrição = models.CharField(max_length=1024)
    Fotos = models.ImageField(upload_to='loja/static/produtos/fotos/')
    Fotos_2 = models.ImageField(upload_to='loja/static/produtos/fotos/')
    Preço = models.DecimalField(max_digits=10, decimal_places=2)
    Disponivel = models.CharField(max_length=8,choices=disponivel_escolha, default='Sim')

    def __str__(self):
        return f'{self.Nome} | {self.Categoriateste} | {self.Preço} | Disponível: {self.Disponivel}'

class Pedidos(models.Model):
    status_escolha = [
    ('Pedido Feito','Pedido Feito'),
    ('Pagamento Aprovado','Pagamento Aprovado'),
    ('Em transporte','Em transporte'),
    ('Entregue','Entregue'),
    ]
    Nome_do_cliente = models.CharField(max_length=128)
    Items = models.ManyToManyField(Produtos, blank=True, related_name="pedido")
    Quantidades = ArrayField(models.CharField(max_length=512))
    Preço_total = models.DecimalField(max_digits=10, decimal_places=2)
    Cpf_cliente = models.CharField(max_length=16)
    Endereço_cliente = models.CharField(max_length=512)
    Status = models.CharField(max_length=32, choices=status_escolha, default='Pedido Feito')

    def __str__(self):
        return f'Pedido ({self.id}) | CPF: {self.Cpf_cliente} | Total: {self.Preço_total} | Status: {self.Status}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=16)
