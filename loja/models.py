from django.db import models

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
    Fotos = models.ImageField(upload_to='static/produtos/fotos/')
    Preço = models.DecimalField(max_digits=10, decimal_places=2)
    Disponivel = models.CharField(max_length=8,choices=disponivel_escolha, default='Sim')

    def __str__(self):
        return f'{self.Nome} | {self.Categoriateste} | {self.Preço} | Disponível: {self.Disponivel}'
