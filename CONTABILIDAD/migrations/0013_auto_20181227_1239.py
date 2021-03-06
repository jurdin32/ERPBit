# Generated by Django 2.0 on 2018-12-27 17:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CONTABILIDAD', '0012_enlacecuentacaja'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enlacecuentabancos',
            name='banco',
        ),
        migrations.RemoveField(
            model_name='enlacecuentabancos',
            name='cuenta',
        ),
        migrations.RemoveField(
            model_name='enlacecuentacaja',
            name='caja',
        ),
        migrations.RemoveField(
            model_name='enlacecuentacaja',
            name='cuenta',
        ),
        migrations.AddField(
            model_name='cuenta_banco',
            name='enlace',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CONTABILIDAD.PlanCuentas'),
        ),
        migrations.DeleteModel(
            name='EnlaceCuentaBancos',
        ),
        migrations.DeleteModel(
            name='EnlaceCuentaCaja',
        ),
    ]
