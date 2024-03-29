# Generated by Django 3.0.5 on 2020-06-23 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categorias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nome', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Produtos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nome', models.CharField(max_length=128)),
                ('Descrição', models.CharField(max_length=1024)),
                ('Fotos', models.ImageField(upload_to='static/produtos/fotos/')),
                ('Fotos_2', models.ImageField(upload_to='static/produtos/fotos/')),
                ('Preço', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Disponivel', models.CharField(choices=[('Sim', 'Sim'), ('Não', 'Não')], default='Sim', max_length=8)),
                ('Categoriateste', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='loja.Categorias')),
            ],
        ),
    ]
