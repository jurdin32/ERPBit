# Generated by Django 2.0 on 2018-12-26 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CONFIGURACION', '0029_helpers_horafecha'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='prioridad',
            field=models.IntegerField(default=0),
        ),
    ]
