# Generated by Django 3.0.5 on 2020-07-02 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0013_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidos',
            name='Quantidades',
            field=models.CharField(max_length=512, null=True),
        ),
    ]