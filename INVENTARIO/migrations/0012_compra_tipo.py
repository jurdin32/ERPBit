# Generated by Django 2.1.4 on 2019-01-19 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('INVENTARIO', '0011_compra_empresa'),
    ]

    operations = [
        migrations.AddField(
            model_name='compra',
            name='tipo',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
