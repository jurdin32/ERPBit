# Generated by Django 2.0 on 2018-10-06 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('CLIENTES', '0001_initial'),
        ('USERS', '0001_initial'),
        ('CONFIGURACION', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bodega',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bodega', models.CharField(max_length=120)),
                ('descripcion', models.CharField(max_length=200)),
                ('estado', models.BooleanField(default=True)),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CONFIGURACION.DatosEmpresa')),
            ],
            options={
                'verbose_name_plural': '2. Registro de Bodegas',
            },
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoria', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=200)),
                ('estado', models.BooleanField(default=True)),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CONFIGURACION.DatosEmpresa')),
            ],
            options={
                'verbose_name_plural': '1. Registro de Categorias',
            },
        ),
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contado', models.BooleanField(default=True)),
                ('diasPlazo', models.IntegerField(default=0)),
                ('fecha', models.DateField(auto_now=True)),
                ('subtotal_0', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('subtotal_iva', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('descuento', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('iva', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('ice', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('irbpnr', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('fecha_emision', models.DateField(blank=True, null=True)),
                ('clave_acceso', models.CharField(blank=True, max_length=50, null=True)),
                ('secuencial', models.CharField(blank=True, max_length=17, null=True, unique='True')),
            ],
            options={
                'verbose_name_plural': '8. Registro de Compras',
            },
        ),
        migrations.CreateModel(
            name='DetalleCompra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('subtotal_0', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('subtotal_iva', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('descuento', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('iva', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('ice', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('irbpnr', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('codigo_iva', models.CharField(default=0, max_length=30)),
                ('tarifa_iva', models.CharField(default=0, max_length=30)),
                ('codigo_ice', models.CharField(default=0, max_length=30)),
                ('tarifa_ice', models.CharField(default=0, max_length=30)),
                ('codigo_irbpnr', models.CharField(default=0, max_length=30)),
                ('tarifa_irbpnr', models.CharField(default=0, max_length=30)),
                ('compra', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='INVENTARIO.Compra')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleProProveedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precioProveedor', models.DecimalField(decimal_places=4, max_digits=9)),
                ('porcentajeIVA', models.DecimalField(decimal_places=4, default=0, max_digits=9)),
                ('codigoIVA', models.CharField(default='000', max_length=10)),
                ('iva', models.DecimalField(decimal_places=4, default=0, max_digits=9)),
                ('codigoICE', models.CharField(default='000', max_length=10)),
                ('porcentajeICE', models.DecimalField(decimal_places=4, default=0, max_digits=9)),
                ('ice', models.DecimalField(decimal_places=4, default=0, max_digits=9)),
                ('codigoIRBPNR', models.CharField(default='000', max_length=10)),
                ('porcentajeIRBPNR', models.DecimalField(decimal_places=4, default=0, max_digits=9)),
                ('irbpnr', models.DecimalField(decimal_places=4, default=0, max_digits=9)),
                ('total', models.DecimalField(decimal_places=4, max_digits=9)),
                ('porcentajeGanancia', models.DecimalField(decimal_places=4, max_digits=9)),
                ('recargo', models.DecimalField(decimal_places=4, default=0, max_digits=9)),
                ('pvp', models.DecimalField(decimal_places=4, default=0, max_digits=9)),
                ('ivapvp', models.DecimalField(decimal_places=4, default=0, max_digits=9)),
                ('icepvp', models.DecimalField(decimal_places=4, default=0, max_digits=9)),
                ('irbpnrpvp', models.DecimalField(decimal_places=4, default=0, max_digits=9)),
                ('totalpvp', models.DecimalField(decimal_places=4, default=0, max_digits=9)),
            ],
            options={
                'verbose_name_plural': '6. Productos del Proveedor',
            },
        ),
        migrations.CreateModel(
            name='Kardex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('I', 'Ingreso'), ('E', 'Egreso')], max_length=20)),
                ('fechaCreacion', models.DateField(auto_now_add=True)),
                ('cantidad', models.IntegerField()),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('detalle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='INVENTARIO.DetalleProProveedor')),
            ],
            options={
                'verbose_name_plural': '7. Inventario - Kardex',
            },
        ),
        migrations.CreateModel(
            name='Marcas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60, unique=True)),
                ('descripcion', models.TextField()),
                ('estado', models.BooleanField(default=True)),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CONFIGURACION.DatosEmpresa')),
            ],
            options={
                'verbose_name_plural': '3. Registro de Marcas',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('PRODUCTO', 'PRODUCTO'), ('SERVICIO', 'SERVICIO')], default='PRODUCTO', max_length=20)),
                ('cod_referencia', models.CharField(blank=True, max_length=20, null=True)),
                ('nombre', models.CharField(max_length=100)),
                ('codigoBarra', models.CharField(blank=True, max_length=100, null=True)),
                ('peso', models.CharField(blank=True, max_length=10, null=True)),
                ('medida', models.CharField(blank=True, max_length=10, null=True)),
                ('estado', models.BooleanField(default=True)),
                ('usuario', models.CharField(max_length=40)),
                ('bodega', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='INVENTARIO.Bodega')),
                ('categoria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='INVENTARIO.Categoria')),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CONFIGURACION.DatosEmpresa')),
                ('marca', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='INVENTARIO.Marcas')),
            ],
            options={
                'verbose_name_plural': '5. Registro de Productos',
            },
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ruc', models.CharField(max_length=13)),
                ('razonSocial', models.CharField(max_length=150)),
                ('nombreComercial', models.CharField(max_length=150)),
                ('sector', models.CharField(max_length=150)),
                ('actividad', models.CharField(max_length=200)),
                ('telefono', models.CharField(max_length=20)),
                ('convencional', models.CharField(max_length=20)),
                ('web', models.CharField(max_length=20)),
                ('direccion', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=100)),
                ('estado', models.BooleanField(default=True)),
                ('empresa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CONFIGURACION.DatosEmpresa')),
                ('parroquia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CONFIGURACION.Lugares')),
                ('tipo_identificacion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CLIENTES.TipoIndentificacion')),
            ],
            options={
                'verbose_name_plural': '4. Registro de Proveedores',
            },
        ),
        migrations.AddField(
            model_name='detalleproproveedor',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='INVENTARIO.Producto'),
        ),
        migrations.AddField(
            model_name='detalleproproveedor',
            name='proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='INVENTARIO.Proveedor'),
        ),
        migrations.AddField(
            model_name='detallecompra',
            name='producto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='INVENTARIO.DetalleProProveedor'),
        ),
        migrations.AddField(
            model_name='compra',
            name='proveedor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='INVENTARIO.Proveedor'),
        ),
        migrations.AddField(
            model_name='compra',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='USERS.myUsuario'),
        ),
    ]
