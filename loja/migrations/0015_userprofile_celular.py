# Generated by Django 3.0.5 on 2020-07-03 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0014_pedidos_quantidades'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='celular',
            field=models.CharField(max_length=16, null=True),
        ),
    ]
