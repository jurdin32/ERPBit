# Generated by Django 2.0 on 2018-11-05 03:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DOCUMENTOS_ELECTRONICOS', '0021_detallescuentascobrar_empresa'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detallescuentascobrar',
            name='nrecibo',
        ),
    ]
