# Generated by Django 2.0 on 2018-11-03 17:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DOCUMENTOS_ELECTRONICOS', '0009_auto_20181103_1222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuentasporcobrar',
            name='factura',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DOCUMENTOS_ELECTRONICOS.Factura', unique=True),
        ),
    ]
