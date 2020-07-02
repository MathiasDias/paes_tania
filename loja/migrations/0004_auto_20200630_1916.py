# Generated by Django 3.0.5 on 2020-06-30 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0003_auto_20200623_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produtos',
            name='Fotos',
            field=models.ImageField(upload_to='loja/static/produtos/fotos/'),
        ),
        migrations.AlterField(
            model_name='produtos',
            name='Fotos_2',
            field=models.ImageField(upload_to='loja/static/produtos/fotos/'),
        ),
        migrations.CreateModel(
            name='Pedidos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nome_do_cliente', models.CharField(max_length=128)),
                ('Preço_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Cpf_cliente', models.CharField(max_length=16)),
                ('Endereço_cliente', models.CharField(max_length=512)),
                ('Status', models.CharField(choices=[('Pedido Feito', 'Pedido Feito'), ('Pagamento Aprovado', 'Pagamento Aprovado'), ('Em transporte', 'Em transporte'), ('Entregue', 'Entregue')], default='Pedido Feito', max_length=32)),
                ('Itens', models.ManyToManyField(blank=True, related_name='pedido', to='loja.Produtos')),
            ],
        ),
    ]