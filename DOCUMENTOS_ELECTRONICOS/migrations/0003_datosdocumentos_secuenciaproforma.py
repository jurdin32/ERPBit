# Generated by Django 2.0 on 2018-10-09 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DOCUMENTOS_ELECTRONICOS', '0002_auto_20181009_0900'),
    ]

    operations = [
        migrations.AddField(
            model_name='datosdocumentos',
            name='secuenciaProforma',
            field=models.IntegerField(default=1),
        ),
    ]
