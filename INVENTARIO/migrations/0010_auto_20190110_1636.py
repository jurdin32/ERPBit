# Generated by Django 2.1.4 on 2019-01-10 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('INVENTARIO', '0009_auto_20190105_0810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proveedor',
            name='web',
            field=models.CharField(max_length=200),
        ),
    ]
