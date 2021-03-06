# Generated by Django 2.0 on 2019-01-20 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CARTERA', '0014_gastosdiarios_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='cierrecaja',
            name='bil1',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
        migrations.AddField(
            model_name='cierrecaja',
            name='bil10',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
        migrations.AddField(
            model_name='cierrecaja',
            name='bil100',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
        migrations.AddField(
            model_name='cierrecaja',
            name='bil20',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
        migrations.AddField(
            model_name='cierrecaja',
            name='bil5',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
        migrations.AddField(
            model_name='cierrecaja',
            name='bil50',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
        migrations.AddField(
            model_name='cierrecaja',
            name='mon1',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
        migrations.AddField(
            model_name='cierrecaja',
            name='mon10',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
        migrations.AddField(
            model_name='cierrecaja',
            name='mon100',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
        migrations.AddField(
            model_name='cierrecaja',
            name='mon25',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
        migrations.AddField(
            model_name='cierrecaja',
            name='mon5',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
        migrations.AddField(
            model_name='cierrecaja',
            name='mon50',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
    ]
