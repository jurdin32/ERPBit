# Generated by Django 2.1.4 on 2019-01-12 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CARTERA', '0013_cierrecaja_empresa'),
    ]

    operations = [
        migrations.AddField(
            model_name='gastosdiarios',
            name='tipo',
            field=models.CharField(default='GASTO', max_length=30),
        ),
    ]
