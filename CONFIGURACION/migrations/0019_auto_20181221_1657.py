# Generated by Django 2.0 on 2018-12-21 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CONFIGURACION', '0018_items_enlace'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='enlace',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
