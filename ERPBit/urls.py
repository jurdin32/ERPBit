from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from CARTERA.views import *
from CONFIGURACION import views as configuracion_views
from CLIENTES import views as clientes_views
from CONFIGURACION.views import *
from CONTABILIDAD.views import *
from DOCUMENTOS_ELECTRONICOS.views import convertirNota_to_Factura
from ERPBit.prueba import ConsulatDocumento
from INVENTARIO import views as inventario_views
from NOTIFICACIONES.views import *
from SRI.views import formulario104AMesual, formulario104ASemestral, formulario104, formulario104ObtenerVentas
from TALENTO_HUMANO import views as talento_humano_views
from DOCUMENTOS_ELECTRONICOS import views as documentos_electronicos
from TALENTO_HUMANO.views import *
from TRANSPORTE import views as transporte_view
from REPORTES import views as reportes_view

urlpatterns = [
    path('admin/', admin.site.urls),

    # path('api-auth/', include('rest_framework.urls')),
    # path('accounts/profile/', admin.site.urls),
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('', configuracion_views.IndexView, name='index'),
    path('login/', configuracion_views.LoginView, name='login'),
    path('logout/', configuracion_views.LogoutView, name='logout'),


    #subir migracion
    path('subir/migrar/', clientes_views.simple_upload, name='subirMigracion'),


    # Urls APP CLIENTE
    path('clientes/', clientes_views.ClienteView, name ='clientes'),
    path('clientes/registroCliente', clientes_views.RegistroClienteView, name ='registroClientes'),
    path('clientes/editarCliente/<int:id>/', clientes_views.EditarClienteView, name='editarCliente'),
    path('clientes/deleteCliente/<int:id>/', clientes_views.DeshabilitarClienteView, name='eliminarCliente'),
    path('clientes/reporteClientes/', clientes_views.ReporteClientes, name='reporteClientes'),
    path('clientes/reportesDinamicos/', clientes_views.ReporteClientesDinamicos, name='reporteDinamicos'),
    path('clientes/listarClienteAjax/', clientes_views.ListarClientesAjax, name='listarClienteAjax'),
    path('clientes/migrar/', clientes_views.migrarClientes, name='migrarClientes'),

    # Urls APP CONFIGURACION
    path('configuracion/usuarios/', configuracion_views.UsuarioView, name='usuarios'),
    path('configuracion/registroUser/', configuracion_views.RegistroUserView, name='registroUsuer'),
    path('configuracion/usuarios/edit/<int:id>/', configuracion_views.EditarUserView, name='editarUsuario'),
    path('configuracion/usuarios/delete/<int:id>/', configuracion_views.DeshabilitarUserView, name='eliminarUsuario'),
    path('configuracion/reporteUsuarios/', configuracion_views.ReporteUsuarios, name='reporteUsuarios'),
    path('configuracion/lugar/<int:Id>/', configuracion_views.Lugar, name="lugar"),
    path('configuracion/lugares/', configuracion_views.lugares, name="lugares"),
    path('configuracion/lugares/<int:id>/<slug:s>/', configuracion_views.registroProvinciasCantonParroquia, name="registroProvinciasCantonParroquia"),
    path('configuracion/lugares/edit/<int:id>/', configuracion_views.editarProvinciasCantonParroquia, name="editarProvinciasCantonParroquia"),

    path('configuracion/annios/',configuracion_views.annios, name= 'annios'),
    path('configuracion/annios/<int:id>/',configuracion_views.annios, name= 'ActualizarAnnios'),
    path('configuracion/annios/activar/<int:id>/',configuracion_views.activarAnnio, name= 'activarAnios'),

    path('configuracion/grupos/', configuracion_views.GrupoView, name='grupos'),
    path('configuracion/grupos/<int:id>/', configuracion_views.modificarGrupo, name='modificarGrupos'),
    path('configuracion/registroGrupo/', configuracion_views.RegistroGrupoView, name='registroGrupo'),

    path('configuracion/empresa/',configuracion_views.EmpresaView, name= 'empresas'),
    path('configuracion/registroEmpresa/', configuracion_views.RegistroEmpresaView, name='registroEmpresa'),
    path('configuracion/editarEmpresa/<int:id>/', configuracion_views.EditarEmpresaView, name="editarEmpresa"),
    path('configuracion/eliminarEmpresa/<int:id>/', configuracion_views.DeshabilitarEmpresaView, name="eliminarEmpresa"),

    path('configuracion/departamentos/', configuracion_views.DerpartamentoView, name="departamentos"),
    path('configuracion/registroDepartamentos/', configuracion_views.RegistroDerpartamentoView, name="registroDepartamentos"),
    path('configuracion/editarDepartamentos/<int:id>/', configuracion_views.EditarDerpartamentoView, name="editarDepartamento"),
    path('configuracion/deleteDepartamentos/<int:id>/', configuracion_views.DeshabilitarDepartamentoView, name="deleteDepartamento"),

    path('configuracion/usuarios/changePassword/<int:id>/', configuracion_views.CambiarClaveView, name='cambiarClave'),

    #Conffiguracion de reportes
    path('configuracion/configuracionReportes/', configuracion_views.configuracionReportes, name="configuracionReportes"),



    # Urls APP INVENTARIO
    path('inventario/producto/', inventario_views.ProductoView, name='productos'),
    path('inventario/producto/registro/', inventario_views.RegistroProductosView, name='registroProductos'),
    path('inventario/producto/edit/<int:id>/<int:idDet>/', inventario_views.ProductoEditarView, name='editarProductos'),
    path('inventario/producto/delete/<int:id>/', inventario_views.EliminarProductoView, name='eliminarProducto'),
    path('inventario/producto/delete/det/<int:id>/', inventario_views.EliminarDetalleProducto, name='eliminarProductoDetalle'),

    path('inventario/servicios/', inventario_views.ServicioView, name='servicios'),
    path('inventario/servicios/registro/', inventario_views.registroServicios, name='registroServicios'),
    path('inventario/servicios/edit/<int:id>/<int:idDet>/', inventario_views.ServicioEditarView, name='editarServicios'),
    path('inventario/servicios/delete/del/<int:id>/', inventario_views.EliminarServicioView, name='eliminarServiciosProductos'),
    path('inventario/servicios/delete/<int:id>/', inventario_views.EliminarDetalleServicio, name='eliminarServiciosDetalles'),

    path('inventario/proveedor/', inventario_views.ProveedorView, name='proveedores'),
    path('inventario/registroProveedores/', inventario_views.RegistroProveedorView, name='registroProveedores'),
    path('inventario/editarProveedor/<int:id>/', inventario_views.EditarProveedorView, name='editarProveedores'),
    path('inventario/deleteProveedor/<int:id>/', inventario_views.DeshabilitarProveedorView, name='eliminarProveedores'),
    path('inventario/reporteProveedor/', inventario_views.ReporteProveedor, name='reporteProveedor'),



    path('inventario/bodega/', inventario_views.BodegaView, name='bodegas'),
    path('inventario/registroBodega/', inventario_views.registroBodegasView, name='registroBodegas'),
    path('inventario/bodega/edit/<int:id>/', inventario_views.editarBodegaView, name='editarBodegas'),
    path('inventario/bodega/delete/<int:id>/', inventario_views.eliminarBodega, name='eliminarBodegas'),

    path('inventario/existencias/', inventario_views.existenciasIngresosEgresos, name='existenciasIngresosEgresos'),
    path('inventario/exitencias/registro/<int:id>/', inventario_views.registroExistencias, name='registroExistencias'),
    path('inventario/kardex/', inventario_views.kardexGeneral, name='kardexGeneral'),
    path('inventario/exitenciasr/ingresos/<int:id>/', inventario_views.reporteIngresosR, name='reporteIngresosR'),
    path('inventario/exitenciasr/egresos/<int:id>/', inventario_views.reporteEgresosR, name='reporteEgresosR'),
    path('inventario/exitenciasr/egresos/<int:id>/', inventario_views.reporteEgresosR, name='reporteEgresosR'),
    path('inventario/exitenciasr/total/<int:id>/', inventario_views.reporteTotalR, name='reporteTotalR'),
    #pdf
    path('inventario/exitencias/ingresos/<int:id>/<slug:f1>/<slug:f2>/', inventario_views.reporteIngresos, name='reporteIngresos'),
    path('inventario/exitencias/egresos/<int:id>/<slug:f1>/<slug:f2>/', inventario_views.reporteEgresos, name='reporteEgresos'),
    path('inventario/exitencias/total/<int:id>/<slug:f1>/<slug:f2>/', inventario_views.reporteTotal, name='reporteTotal'),

    #Marcas
    path('inventario/marcas/', inventario_views.MarcasView, name='existenciasMarcas'),
    path('inventario/registroMarca/', inventario_views.registroMarcas, name='registroMarcas'),
    path('inventario/marca/edit/<int:id>/', inventario_views.editarMarcas, name='editarMarcas'),
    path('inventario/marca/delete/<int:id>/', inventario_views.EliminarMarcasView, name='eliminarMarcas'),

    #Categorias
    path('inventario/categorias/', inventario_views.Categorias, name='categorias'),
    path('inventario/categorias/registro/', inventario_views.registrarCategoria, name='registroCategorias'),
    path('inventario/categoria/edit/<int:id>/', inventario_views.editarCategoria, name='registroCategorias'),
    path('inventario/categoria/delete/<int:id>/', inventario_views.EliminarCategoriaView, name='eliminarMarcas'),

    #Inventario
    path('inventario/Compras/', inventario_views.ComprasView, name ='compras'),
    path('inventario/registroCompra/<int:n>/', inventario_views.RegistroComprasView, name ='registroCompra'),
    path('inventario/Compra/<int:idCompra>/', inventario_views.detallesCompra,name='detalleCompra'),
    path('inventario/Compra_ver/<int:idCompra>/', inventario_views.ver_compras,name='verCompra'),


    # Urls APP TALENTO HUMANO
    path('telento_humano/empleados/', talento_humano_views.EmpleadoView, name='empleados'),
    path('telento_humano/registroEmpleados/', talento_humano_views.RegistroEmpleadoView, name='registroEmpleados'),
    path('telento_humano/editarEmpleados/<int:id>/', talento_humano_views.EditarEmpleadoView, name='editarEmpleados'),
    path('telento_humano/deleteEmpleado/<int:id>/', talento_humano_views.DeshabilitarEmpleadoView, name='deleteEmpleado'),

    path('telento_humano/empleado/sueldo/', talento_humano_views.suedosEmpleado, name='sueldosySalarios'),
    path('telento_humano/empleado/sueldo/deshabilitar/<int:id_sueldo>/', talento_humano_views.desabilitarSueldo, name='desabilitarSueldo'),
    path('telento_humano/empleado/sueldo/deshabilitar/None/', talento_humano_views.desabilitarSueldoTroll, name='desabilitarSueldo'),
    path('telento_humano/empleado/sueldo/registro/<int:id_empleado>/', talento_humano_views.CrearSueldo, name='CrearSueldo'),
    path('telento_humano/empleado/sueldo/edit/<int:id_empleado>/<int:sueldot>/', talento_humano_views.editarSueldo, name='editarSueldo'),
    path('telento_humano/empleado/sueldo/actDesacSueldo/<int:empleado>/<int:id>/', talento_humano_views.actDesacSueldo, name='actDesacSueldo'),


    path('telento_humano/rolPagos/', talento_humano_views.RolPagosView, name='rolPagos'),
    path('telento_humano/rolPagos/<int:id_empleado>/', talento_humano_views.RolPagosEmpleado, name='condiguracionRol'),
    path('telento_humano/rolPagos/eliminar/<int:id>/<int:id_emp>/', talento_humano_views.eliminarRol, name='eliminarRol'),
    path('telento_humano/rolPagos/print/<int:rem>/', talento_humano_views.rolIndividual, name='rolIndividual'),
    path('telento_humano/rolPagos/consolidado/', talento_humano_views.rolConsolidado, name='rolConsolidado'),
    path('telento_humano/rolPagos/consolidado/annio/<int:id>/', talento_humano_views.rolConsolidadoAnnio, name='rolConsolidadoAnio'),
    path('telento_humano/rolPagos/consolidado/annio/<int:id>/<slug:f1>/', talento_humano_views.rolConsolidadoSueldos, name='rolConsolidadoSueldos'),
    path('telento_humano/rolPagos/consolidado/mensual/<int:idAnio>/<slug:f1>/',talento_humano_views.rolConsolidadoMensual,name='rolConsolidadoMensual'),

    path('telento_humano/cargos/', CargosView, name='cargos'),
    path('telento_humano/cargos/eliminar/<int:id>/', CargosView, name='eliminarCargos'),

    path('telento_humano/cargos/registro/', crearCargos, name='registrarCargos'),
    path('telento_humano/cargos/registro/<int:id>/', crearCargos, name='editarCargos'),

    # Urls APP DOCUMENTOS ELECTRONICOS
    path('documentos_electronicos/Facturas/', documentos_electronicos.FacturasView, name ='facturas'),
    path('documentos_electronicos/registroFactura/', documentos_electronicos.RegistroFacturasView, name ='registroFactura'),
    path('documentos_electronicos/Facturas/<int:idFactura>/', documentos_electronicos.detallesFactura, name ='detalleFactura'),
    path('documentos_electronicos/Facturas/xml/<int:n>/', documentos_electronicos.facturaXML, name ='facturaXML'),
    path('documentos_electronicos/Facturas/json/<int:n>/', documentos_electronicos.facturaJSON, name ='facturaJSON'),

    path('documentos_electronicos/Proformas/', documentos_electronicos.ProfromasView, name ='proformas'),
    path('documentos_electronicos/registroProforma/', documentos_electronicos.RegistroProformasView, name ='registroProformas'),
    path('documentos_electronicos/Proformas/<int:idFactura>/', documentos_electronicos.detallesProforma, name ='detalleProforma'),

    path('documentos_electronicos/Facturas/Detalles/<int:id>/', documentos_electronicos.detalles, name ='detalle'),
    path('documentos_electronicos/Proformas/enviar/<int:idFactura>/', documentos_electronicos.enviarProforma, name ='enviarProforma'),

    path('documentos_electronicos/guiasRemision/', documentos_electronicos.GuiaRemisionView, name ='guiaRemision'),
    path('documentos_electronicos/registroGuiaRemision/', documentos_electronicos.RegistroGuiaRemisionView, name="registroGuiaRemision"),
    path('documentos_electronicos/guiaRemision/<int:idGuia>/', documentos_electronicos.guiRemisionRide, name="repguiaRemision"),
    path('documentos_electronicos/guiaRemisionS/<slug:codigo>/', documentos_electronicos.guiRemisionRideSlug, name="guiRemisionRideSlug"),
    path('documentos_electronicos/guiaRemision/json/<int:n>/',documentos_electronicos.guiaRemisionJSON, name="guiRemisionJSon"),
    path('documentos_electronicos/guiaRemision/xml/<int:n>/',documentos_electronicos.guiaRemisionXML, name="guiRemisionXML"),

    path('documentos_electronicos/notasVenta/', documentos_electronicos.notasVenta, name ='notasVenta'),
    path('documentos_electronicos/notasVenta/registro/', documentos_electronicos.RegistroNotasView, name ='registroNotasVenta'),
    path('documentos_electronicos/notasVenta/<int:idFactura>/', documentos_electronicos.detallesNotaVenta, name ='detalleNotaVenta'),
    path('documentos_electronicos/recibo/<int:idFactura>/', documentos_electronicos.reciboFactura, name ='reciboFactura'),

    path('documentos_electronicos/retenciones/', documentos_electronicos.RetencionesView, name ='retenciones'),
    path('documentos_electronicos/registroRetenciones/<int:id>/', documentos_electronicos.RegistroRetencionesView, name ='registroRetenciones'),
    path('documentos_electronicos/retenciones/json/<int:n>/',documentos_electronicos.RetencionJSON, name="guiRemisionJSon"),
    path('documentos_electronicos/retenciones/xml/<int:n>/',documentos_electronicos.RetencionXML, name="retencionXML"),
    path('documentos_electronicos/retenciones/ride/<int:id>/', documentos_electronicos.RetencionRideSlug, name="retencionRideSlug"),

    path('documentos_electronicos/notaDebito/', documentos_electronicos.NotaDebitoView, name ='notaDebito'),
    path('documentos_electronicos/notaCredito/', documentos_electronicos.NotaCreditoView, name ='notaCredito'),

    path('documentos_electronicos/registroNotaDebito/', documentos_electronicos.RegistroNotaDebitoView, name ='registroNotaDebito'),
    path('documentos_electronicos/registroNotaCredito/', documentos_electronicos.RegistroNotaCreditoView, name ='registroNotaCredito'),

    path('documentos_electronicos/reportesDinamicos/', documentos_electronicos.ReporteDinamicos, name='reporteDinamicoDoc'),
    path('documentos_electronicos/reportes/', documentos_electronicos.ConsulatDocumento, name='reporte'),

    path('documentos_electronicos/configuracion/', documentos_electronicos.Configuracion,name='configuracion'),
    path('documentos_electronicos/configuracion/<int:id>/', documentos_electronicos.Configuracion,name='configuracionActivar'),

    path('documentos_electronicos/codEstablecimiento/', documentos_electronicos.CodEstablecimiento, name='codEstablecimiento'),
    path('documentos_electronicos/registroCondEstablecimiento/', documentos_electronicos.RegistroCodEstablecimiento, name='registroCodEstablecimiento'),
    path('documentos_electronicos/codEstablecimiento/editar/<int:id>/', documentos_electronicos.EditarCodEstablecimiento, name='editarcodEstablecimiento'),
    path('documentos_electronicos/codEstablecimiento/delete/<int:id>/', documentos_electronicos.DeshabilitarCodEstablecimiento, name='eliminarcodEstablecimiento'),

    path('documentos_electronicos/puntoEmision/', documentos_electronicos.PuntoEmisionView, name='puntoEmision'),
    path('documentos_electronicos/registroPuntoEmision/', documentos_electronicos.RegistroPuntoEmision, name='registroPuntoEmision'),
    path('documentos_electronicos/puntoEmision/editar/<int:id>/', documentos_electronicos.EditarPuntoEmision, name='editarPuntoEmision'),
    path('documentos_electronicos/puntoEmision/delete/<int:id>/', documentos_electronicos.DeshabilitarPuntoEmision, name='eliminarPuntoEmision'),
    path('documentos_electronicos/anular/<int:id>/', documentos_electronicos.anularFactura, name='anulacionFactura'),

    # Urls APP TRANSPORTE
    path('transporte/empresas/', transporte_view.EmpresaView, name='empresasTrans'),
    path('transporte/registroEmpresasTrans/', transporte_view.RegistroEmpresaTransView, name='registroEmpresasTrans'),
    path('transporte/editarEmpresa/<int:id>/', transporte_view.EditarEmpresaView, name='editarEmpresa'),
    path('transporte/deleteEmpresa/<int:id>/', transporte_view.DeshabilitarEmpresaView, name='eliminarEmpresa'),

    path('transporte/conductores/', transporte_view.ConductorView, name='conductores'),
    path('transporte/registroConductor/', transporte_view.RegistroConductorView, name='registroConductor'),
    path('transporte/editarConductor/<int:id>/', transporte_view.EditarConductorView, name='editarConductor'),
    path('transporte/deleteConductor/<int:id>/', transporte_view.DeshabilitarConductorView, name='eliminarConductor'),

    path('transporte/vehiculos/', transporte_view.VehiculoView, name='vehiculos'),
    path('transporte/registroVehiculos/', transporte_view.RegistroVehiculoView, name='registroVehiculo'),
    path('transporte/editarVehiculo/<int:id>/', transporte_view.EditarVehiculoView, name='editarVehiculo'),
    path('transporte/deleteVehiculo/<int:id>/', transporte_view.DeshabilitarVehiculoView, name='eliminarVehiculo'),
    path('transporte/reporteTransporte/', transporte_view.ReporteTransporte, name='reporteTransporte'),

    #URLS APP CARTERA
    path('cartera/apertura/', aperturaCaja, name='aperturaCaja'),
    path('cartera/gastosDiarios/', gastosDiarios, name='gastosDiarios'),
    path('cartera/cierreCaja/', cierreCaja, name='cierreCaja'),

    path('cartera/cuentasCobrar/', CuentasCobraar, name='cuentasCobrar'),
    path('cartera/cuentasCobrar/registro/<int:idFactura>/', registroCuentas, name='registrocuentasCobrar'),
    path('cartera/cuentasCobrar/tablaPagos/<int:idCuenta>/', TablaPagosCuentasCobrar, name='tablapagosCuentasCobrar'),
    path('cartera/cuentasCobrar/pagar/<int:idDetalle>/', PagarCuentaCobrar, name='PagarCuentaCobrar'),
    path('cartera/cuentasCobrar/pagar/recibo/<int:idDetalle>/', ReciboPgoCuentaCobrar, name='ReciboPgoCuentaCobrar'),
    path('cartera/cuentasCobrar/pagar/parcial/', PagarCuentaCobrarPPT, name='PagarCuentaCobrarPPT'),
    path('cartera/cuentasCobrar/nota_to_factura/<int:idFactura>/', convertirNota_to_Factura, name='convertirNota_to_Factura'),


    path('cartera/cuentasPagar/', CuentasPagar, name='cuentasPagar'),
    path('cartera/anticiposSueldo/', AnticiposSueldo, name='anticiposSueldo'),
    path('cartera/anticiposSueldo/<int:id>/', registroAnticipo, name='anticiposSueldoEmpleado'),
    path('cartera/devoluciones/', Devoluciones, name='devoluciones'),

    path('cartera/cajasUsuarios/', cajasUsuariosEmpresa, name='cajasUsuarios'),


    #contabilidad
    path('contabilidad/catalogo/', catalogoCuentas, name='catalogoCuentas'),
    path('contabilidad/catalogo/edit/<int:id>/', catalogoCuentas, name='registrarCatalogoCuentas'),
    path('contabilidad/catalogo/delete/<int:id>/', eliminarCuenta, name='eliminarCuenta'),
    path('contabilidad/registro/', registroContable, name='registroContable'),

    path('contabilidad/bancos/', registroBancos, name='registroBancos'),
    path('contabilidad/bancos/<int:id>/', registroBancos, name='modificarBancos'),
    path('contabilidad/bancos/del/<int:id>/', desactivarRegistroBancos, name='EliminarBancos'),

    path('contabilidad/porcentajes_retencion/', porcentajes_retencion, name='porcentajes'),

    #documentacion
    path('docs/', documentacion, name='documentacion'),
    path('docs/<int:id>/', documentacionDetalles, name='documentacionDetalles'),

    path('sri/104/ImpuestoAgregado/', formulario104, name="formulario104"),
    path('sri/104A/Mensual/', formulario104AMesual, name='formulario104AMensual'),
    path('sri/obtenerVentas/', formulario104ObtenerVentas, name='obtenerVentas'),
    path('sri/104A/Semestral/', formulario104ASemestral, name='formulario104ASemestral'),

    #noticias:
    path('noticias/', noticias, name='noticias'),
    path('noticias/oo/<int:id>/', visualizarMensaje, name='noticiasVer'),
    path('noticias/oio/<int:id>/', responderMensaje, name='responderMensaje'),
    path('noticias/componer/', componerMensaje, name='componerMensaje'),
    path('noticias/consultas/', ConsultaDocumentos, name='consultas' ),
    path('consulta/listar/', ListarDocumentos, name='listar'),
    path('consulta/listarPDF/<int:idFactura>/', ConsultaDocumentoPdf, name='listar'),
    path('consulta/listarPDFRetencion/<int:idRetencion>/', ConsultaDocumentoPdfRetencion, name='listar'),
    path('consulta/listarPDFGuia/<int:idGuia>/', ConsultaDocumentoPdfGuia, name='listar'),

    path('chat/hilos/', hilos, name='hilosUsuario'),
    path('chat/hilos/<int:pk>/', agregarMensaje, name='agregarMensaje'),

    path('conectados/', usuariosActivos, name='conectados'),

    #Reportes
    path('reportes/reporteProductos/', reportes_view.ReporteProductos, name='reporteProductos'),
    path('reportes/productos/', reportes_view.ConsulatProductos, name='consultaProductos'),


]+static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
admin.site.site_header = 'ERP BIT'
