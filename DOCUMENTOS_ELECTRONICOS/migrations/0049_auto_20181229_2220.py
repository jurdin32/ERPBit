# Generated by Django 2.0 on 2018-12-30 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DOCUMENTOS_ELECTRONICOS', '0048_auto_20181229_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guiaremision',
            name='fecha',
            field=models.DateField(auto_now_add=True),
        ),
    ]
