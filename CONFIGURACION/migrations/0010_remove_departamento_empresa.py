# Generated by Django 2.0 on 2018-12-14 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CONFIGURACION', '0009_remove_funciones_empresa'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='departamento',
            name='empresa',
        ),
    ]
