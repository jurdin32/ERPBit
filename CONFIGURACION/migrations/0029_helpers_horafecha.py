# Generated by Django 2.0 on 2018-12-23 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CONFIGURACION', '0028_helpers_descripcion'),
    ]

    operations = [
        migrations.AddField(
            model_name='helpers',
            name='horaFecha',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
