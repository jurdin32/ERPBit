# Generated by Django 2.0 on 2019-08-19 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DOCUMENTOS_ELECTRONICOS', '0054_auto_20190819_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='fecha',
            field=models.DateField(blank=True, null=True),
        ),
    ]
