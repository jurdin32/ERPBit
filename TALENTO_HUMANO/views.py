import datetime

from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.utils.dateparse import parse_date
from django.shortcuts import render

# Create your views here.
from CONFIGURACION.models import Lugares, Departamento, DatosEmpresa, Reportes, Cargos
from CONFIGURACION.views import funciones_usuario
from INVENTARIO.reportes import render_to_pdf
from TALENTO_HUMANO.models import *


#
# Vista para presentar todos los empledos
#
from USERS.models import myUsuario

def EmpleadoView(request):
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    contexto = {
        'empleados': Empleado.objects.filter(departamento__empresa=user.empresa),
        'empresa': user.empresa,
        'usuario': request.user,
        'paises': Lugares.objects.all(),
        'departamentos' : Departamento.objects.filter(empresa=user.empresa),
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all(),
        'user2': user.is_admin,
    }
    return render(request, 'Talento_Humano/empleados.html', contexto)

#
# Vista para Guardar empleados
#
def RegistroEmpleadoView(request):
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    error = mensaje = ''
    if request.POST:

        nombre =  request.POST['nombre']
        apellido = request.POST['apellido']
        ruc = request.POST['ruc']
        email = request.POST['email']
        fechaNacimiento = parse_date(request.POST['fechaNacimiento'])
        sexo = request.POST['sexo']
        cargas = request.POST['cargas']
        profesion = request.POST['profesion']
        telefono = request.POST['telefono']
        direccion = request.POST['direccion']
        observaciones = request.POST['observaciones']
        departamento = request.POST['departamento']
        fechaIngreso = parse_date(request.POST['fechaIngreso'])
        fechaSalida = parse_date(request.POST['fechaSalida'])
        parroquia = request.POST['parroquia']
        estado = request.POST['estado']

        if int(estado)==1:
            estado = True
        else:
            estado = False
        if len(request.POST['verificar']) <= 0:
            empleados = Empleado(nombre=nombre, apellido=apellido, ruc=ruc, email=email, fechaNacimiento=fechaNacimiento, sexo=sexo,
                                cargas=cargas, profesion=profesion, telefono=telefono, direccion=direccion, observaciones=observaciones,
                                departamento_id=departamento, fechaIngreso=fechaIngreso, fechaSalida=fechaSalida, parroquia_id=parroquia,
                                estado=estado)

            empleados.save()
            mensaje="El empleado se ha registrado exitosamente..!!"
        else:
            error="Es posible que la cedula que intenta registrar este incorrecta, Reintente..!!"

    contexto = {
        'paises': Lugares.objects.filter(lugar=None),
        'departamentos' : Departamento.objects.filter(empresa=user.empresa),
        'empresa': user.empresa,
        'usuario': request.user,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all(),
        'user2': user.is_admin,
    }

    return render(request, 'Talento_Humano/registroEmpleados.html',contexto)

def EditarEmpleadoView(request, id):
    empleado = Empleado.objects.get(id=id)
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    mensaje=""
    if request.POST:
        empleado.nombre = request.POST['nombre']
        empleado.apellido = request.POST['apellido']
        empleado.ruc = request.POST['ruc']
        empleado.email = request.POST['email']
        empleado.fechaNacimiento = parse_date(request.POST['fechaNacimiento'])
        empleado.sexo = request.POST['sexo']
        empleado.cargas = request.POST['cargas']
        empleado.profesion = request.POST['profesion']
        empleado.telefono = request.POST['telefono']
        empleado.direccion = request.POST['direccion']
        empleado.observaciones =request.POST['observaciones']
        empleado.departamento_id = request.POST['departamento']
        empleado.fechaIngreso = parse_date(request.POST['fechaIngreso'])
        empleado.fechaSalida = parse_date(request.POST['fechaSalida'])
        empleado.parroquia_id = request.POST['parroquia']
        empleado.estado = request.POST['estado']

        if int(request.POST['estado'])== 1:
            empleado.estado = True
        else:
            empleado.estado = False

        empleado.save()
        mensaje="El empleado se ha modificado exitosamente..!!"

    contexto = {
        'empleado':empleado,
        'departamentos': Departamento.objects.all(),
        'paises': Lugares.objects.filter(lugar=None),
        'usuario':request.user,
        'empresa':user.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all(),
        'mensaje':mensaje,
        'user2': user.is_admin,
    }
    return render(request, 'Talento_Humano/registroEmpleados.html', contexto)

def DeshabilitarEmpleadoView(request, id):
    empleado = Empleado.objects.get(id=id)
    empleado.estado = False
    empleado.save()
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    contexto = {
        'empleados': Empleado.objects.filter(departamento__empresa=user.empresa),
        'empresa': user.empresa,
        'usuario': request.user,
        'paises': Lugares.objects.all(),
        'departamentos': Departamento.objects.filter(empresa=user.empresa),
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all(),
        'mensaje':"El Empleado ha sido deshabilitado..!!",
        'user2': user.is_admin,
    }
    return render(request, 'Talento_Humano/empleados.html', contexto)

def suedosEmpleado(request):
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    contexto={
        'empleados': Empleado.objects.filter(estado=True,departamento__empresa=user.empresa),
        'usuario': request.user,
        'empresa':user.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all(),
        'user2': user.is_admin,
    }
    return render(request,'Talento_Humano/SueldosySalarios.html',contexto)

def desabilitarSueldo(request,id_sueldo):
    sueldo=Sueldos.objects.get(id=id_sueldo)
    sueldo.estado=False
    sueldo.save()
    return HttpResponseRedirect('/telento_humano/empleado/sueldo/')

def desabilitarSueldoTroll(request):
    return HttpResponseRedirect('/telento_humano/empleado/sueldo/')

def CrearSueldo(request,id_empleado):
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    if request.POST:
        beneficio=False
        for sueldo in Sueldos.objects.filter(empleado_id=id_empleado,estado=True):
            sueldo.estado=False
            sueldo.save()
        if 'beneficio' in request.POST:
            beneficio=True
        sueldos=Sueldos(empleado_id=id_empleado,
                       annio_id=request.POST['anio'],
                       sueldo=request.POST['sueldo'],
                       cargo_id=request.POST['cargo'],
                       diasTrabajados=request.POST['dias'],
                        horasdiarias=request.POST['horasdiarias'],
                        totalHoras=request.POST['totalhoras'],
                       formaPago_id=request.POST['fpago'],beneficio=beneficio)
        sueldos.save()
        print (request.POST)
    contexto={
        'sueldos':Sueldos.objects.filter(empleado_id=id_empleado),
        'usuario':request.user,
        'empleado': Empleado.objects.get(id=id_empleado),
        'annios':Anio.objects.filter(empresa=user.empresa),
        'pagos':FormaPago.objects.all(),
        'cargos':Cargos.objects.filter(estado=True,departamento__empresa=user.empresa),
        'departamentos':Departamento.objects.filter(estado=True,empresa=user.empresa).order_by('nombre'),
        'empresa':user.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all(),
        'user2': user.is_admin,
    }
    return render(request, 'Talento_Humano/SueldosRegistro.html', contexto)

def editarSueldo(request,id_empleado,sueldot):
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    mensaje=""
    if request.POST:
        beneficio=False
        if 'beneficio' in request.POST:
            beneficio=True
            for sueldo in Sueldos.objects.filter(empleado_id=id_empleado, estado=True):
                sueldo.estado = False
                sueldo.save()

        sueldos=Sueldos.objects.get(id=sueldot)
        sueldos.beneficio=beneficio
        sueldos.estado=True
        sueldos.cargo=Cargos.objects.get(id=request.POST['cargo'])
        sueldos.sueldo=request.POST['sueldo'].replace(',','.')
        sueldos.annio=Anio.objects.get(id=request.POST['anio'])
        sueldos.diasTrabajados=request.POST['dias'].replace(',','.')
        sueldos.horasdiarias=request.POST['horasdiarias'].replace(',','.')
        sueldos.totalHoras=request.POST['totalhoras'].replace(',','.')
        sueldos.formaPago=FormaPago.objects.get(id=request.POST['fpago'])
        sueldos.save()
        mensaje="Este sueldo se ha modificado exitosamente..!!"
    contexto = {
        'sueldos': Sueldos.objects.filter(empleado_id=id_empleado).order_by('annio'),
        'usuario': request.user,
        'empleado': Empleado.objects.get(id=id_empleado),
        'annios': Anio.objects.all().order_by('anio'),
        'pagos': FormaPago.objects.all(),
        'cargos': Cargos.objects.filter(estado=True),
        'sueldo':Sueldos.objects.get(id=sueldot),
        'departamentos': Departamento.objects.filter(estado=True).order_by('nombre'),
        'empresa':user.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by("prioridad"),
        'mensaje':mensaje,
        'user2': user.is_admin,
    }
    return render(request,'Talento_Humano/SueldosRegistro.html', contexto)

def actDesacSueldo(request,empleado,id):
    mensaje=""
    for sueldo in Sueldos.objects.filter(empleado_id=empleado, estado=True):
        if not sueldo.id==id:
            sueldo.estado = False
            sueldo.save()

    sueldo=Sueldos.objects.get(id=id)
    print(sueldo.estado)
    if sueldo.estado:
        sueldo.estado=False
        mensaje="Este Sueldo ha sido Desactivado..!!"
    else:
        sueldo.estado = True
        mensaje=("Este Sueldo ha sido Activado..!!")
    sueldo.save()
    print("ha entrado por aqui ..!!")
    user=myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    contexto = {
        'sueldos': Sueldos.objects.filter(empleado_id=empleado),
        'usuario': request.user,
        'empleado': Empleado.objects.get(id=empleado),
        'annios': Anio.objects.filter(empresa=user.empresa),
        'pagos': FormaPago.objects.all(),
        'cargos': Cargos.objects.filter(estado=True, departamento__empresa=user.empresa),
        'departamentos': Departamento.objects.filter(estado=True, empresa=user.empresa).order_by('nombre'),
        'empresa': user.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'mensaje':mensaje,
        'user2': user.is_admin,
    }
    return render(request, 'Talento_Humano/SueldosRegistro.html', contexto)


def RolPagosView(request):
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    contexto={
        'empleados':Empleado.objects.filter(estado=True,departamento__empresa=user.empresa),
        'usuario':request.user,
        'empresa':user.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by('prioridad'),
        'user2': user.is_admin,
    }
    return render(request, 'Talento_Humano/configuracionRolPagos.html', contexto)

def RolPagosEmpleado(request,id_empleado):
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    sueldos = Sueldos.objects.get(empleado_id=id_empleado,estado=True)
    anio = Anio.objects.get(activado=True,empresa=user.empresa).anio
    mensaje=error=""
    rol=None
    remuner=None
    if request.POST:
        roles=RolPagos.objects.filter(empresa=user.empresa)
        try:
            rol=RolPagos.objects.get(PeridoRol=request.POST['periodo']+"/"+str(anio),empresa=user.empresa)

        except RolPagos.DoesNotExist:
            rol=RolPagos(empresa=user.empresa,numeroRol=0,PeridoRol=request.POST['periodo']+"/"+str(anio))
            rol.save()
            rol.numeroRol=str.zfill(str(roles.count()),4)
            rol.save()
        try:
            remuner = Remuneraciones.objects.get(periodo=request.POST['periodo'] + "/" + str(anio),sueldo__empleado_id=id_empleado)
            error="Este empleado ya tiene registrado este periodo..!!"
        except Remuneraciones.DoesNotExist:
            remuneracion=Remuneraciones(
                rol=rol,sueldo=sueldos,periodo=request.POST['periodo']+"/"+str(anio),dias=request.POST['diaslaborados'],
                sueldoInicial=sueldos.sueldo,mes=request.POST['periodo'],xiiisueldo=request.POST['xiiisueldo'],
                horasextras=request.POST['ingresoporhorasextras'],multas=request.POST['multas'],
                xivsueldo=request.POST['xivsueldo'],fondosreserva=request.POST['fondosdereserva'],vacaciones=request.POST['vacaciones'],
                otrosingresos=request.POST['otrosingresos'],totalIngresos=request.POST['totalingresos'],aporteiess=request.POST['aportesiess'],
                iece=request.POST['iece'],prestamosiess=request.POST['prestamosaliess'],impuestoalarenta=request.POST['impuestoalarenta'],
                anticiposueldo=request.POST['anticipodesueldos'],descuento=request.POST['descuentos'],otrosegresos=request.POST['otrosegresos'],
                totalEgresos=request.POST['totalegresos'],total=request.POST['total']
            )
            remuneracion.save()
            mensaje="Se ha creado el Rol del Empleado %s %s"%(remuneracion.sueldo.empleado.nombre,remuneracion.sueldo.empleado.apellido)

    remuneraciones=Remuneraciones.objects.filter(sueldo__empleado_id=id_empleado).order_by('periodo')
    try:
        periodo=remuneraciones.last().periodo.split("/")
        mes=''
        print(periodo)
        if int(periodo[0])<=11:
            mes=str.zfill(str(int(periodo[0])+1),2)
        else:
            mes='01'
    except:
        mes='01'
    print(mes)
    contexto={
        'usuario':request.user,
        'sueldo':sueldos,
        'remuneraciones':remuneraciones,
        'empleado':Empleado.objects.get(id=id_empleado),
        'campos':IngresosEgresos.objects.all().order_by('prioridad'),
        'mes':mes,
        'empresa':user.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by("prioridad"),
        'mensaje':mensaje,
        'error':error,
        'user2': user.is_admin,
    }
    return render(request, 'Talento_Humano/configuracionRol.html',contexto)


def eliminarRol(request,id,id_emp):
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    sueldos = Sueldos.objects.get(empleado_id=id_emp, estado=True)
    mensaje = error = ""
    remuneraciones = Remuneraciones.objects.filter(sueldo__empleado_id=id_emp).order_by('periodo')
    try:
        periodo=remuneraciones.last().periodo.split("/")
        mes=''
        print(periodo)
        if int(periodo[0])<=11:
            mes=str.zfill(str(int(periodo[0])+1),2)
        else:
            mes='01'
    except:
        mes='01'

    try:
        remuneracion=Remuneraciones.objects.get(id=id)
        remuneracion.delete()
        mensaje="La remuneracion se ha eliminado..!!"
    except:
        error="El registro no existe..!!"
    contexto = {
        'usuario': request.user,
        'sueldo': sueldos,
        'remuneraciones': remuneraciones,
        'empleado': Empleado.objects.get(id=id_emp),
        'campos': IngresosEgresos.objects.all().order_by('prioridad'),
        'mes': mes,
        'empresa': user.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by("prioridad"),
        'mensaje': mensaje,
        'error': error,
        'user2': user.is_admin,
    }
    return render(request, 'Talento_Humano/configuracionRol.html', contexto)

def rolIndividual(request,rem):
    remuneracion=Remuneraciones.objects.get(id=rem)
    user=myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    contexto={
        'usuario': request.user,
        'remuneracion':remuneracion,
        'reporte':Reportes.objects.filter(empresa=user.empresa).last(),
        'empresa':user.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by("prioridad"),
        'user2': user.is_admin,
    }
    #return render(request,'Talento_Humano/rolIndividual.html', contexto)
    return render_to_pdf('Talento_Humano/rolIndividual.html',contexto)

def rolConsolidado(request):
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    try:
        Anio.objects.get(anio=datetime.datetime.now().year,empresa=user.empresa)
    except Exception as error:
        print(error)
        Anio(empresa=user.empresa,anio=datetime.datetime.now().year,activado=True).save()

    contexto={
        'usuario': request.user,
        'annios':Anio.objects.filter(empresa=user.empresa).order_by('anio'),
        'empresa':user.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by("prioridad"),
        'user2': user.is_admin,
    }
    return render(request,'Talento_Humano/rolConsolidado.html',contexto)

def rolConsolidadoAnnio(request,id):
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    contexto={
        'usuario': request.user,
        'annio':Anio.objects.get(id=id),
        'annios': Anio.objects.filter(empresa=user.empresa).order_by('anio'),
        'sueldos': Sueldos.objects.filter(annio_id=id),
        'empresa':user.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by("prioridad"),
        'user2': user.is_admin,
    }
    return render(request,'Talento_Humano/rolConsolidado.html',contexto)

def rolConsolidadoSueldos(request,id,f1):
    slug=f1.replace("-","/")
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    anio=Anio.objects.get(id=id)
    contexto={
        'usuario':request.user,
        'annio':anio,
        'annios': Anio.objects.filter(empresa=user.empresa).order_by('anio'),
        'sueldos':Sueldos.objects.filter(annio_id=id),
        'remuneraciones':Remuneraciones.objects.filter(periodo=slug,sueldo__annio=anio),
        'slug':f1,
        'empresa':user.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by("prioridad"),
        'user2': user.is_admin,
    }
    return render(request,'Talento_Humano/rolConsolidado.html',contexto)

def rolConsolidadoMensual(request,idAnio,f1):
    anio=Anio.objects.get(id=idAnio)
    user=myUsuario.objects.get(usuario=request.user)

    remuneraciones=Remuneraciones.objects.filter(periodo=f1.replace("-","/"),sueldo__annio=anio)
    contexto={
        'reporte':Reportes.objects.filter(empresa=user.empresa).last(),
        'slug':f1.replace("-","/"),
        'remuneraciones': remuneraciones.order_by('periodo'),
        'remuneracion':remuneraciones.first(),
        'sumaIngresos':remuneraciones.aggregate(Sum("totalIngresos"))['totalIngresos__sum'],
        'sumaEgresos': remuneraciones.aggregate(Sum("totalEgresos"))['totalEgresos__sum'],
        'totales':remuneraciones.aggregate(Sum("total"))['total__sum'],
        'user2': user.is_admin,
    }
    return render_to_pdf('Talento_Humano/rolConsolidadomensual.html',contexto)
    # return render(request,'Talento_Humano/rolConsolidadomensual.html',contexto)

def CargosView(request,id=0):
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    mensaje=""
    if id>0:
        cargo=Cargos.objects.get(id=id)
        cargo.estado=False
        cargo.save()
        mensaje="El registro fue desactivado..!!"
    contexto = {
        'usuario': request.user,
        'empresa': user.empresa,
        'permisos': permisos,
        'funciones': funciones_usuario(permisos),
        'items': Items.objects.all().order_by("prioridad"),
        'cargos':Cargos.objects.filter(departamento__empresa=user.empresa),
        'mensaje':mensaje,
        'user2': user.is_admin,
    }
    return render(request, 'Talento_Humano/cargos.html', contexto)

def crearCargos(request,id=0):
    user = myUsuario.objects.get(usuario=request.user)
    permisos = Permiso.objects.filter(grupo=user.grupo)
    mensaje=""
    cargo=None
    if id>0:
        cargo = Cargos.objects.get(id=id)
    if request.POST:
        if id==0:
            cargo=Cargos(departamento_id=request.POST['departamento'],cargo=request.POST['nombre'],descripcion=request.POST['descripcion'])
            cargo.save()
            mensaje="El registro se ha creado exitosamente..!!"
        else:
            cargo.departamento_id=request.POST['departamento']
            cargo.cargo=request.POST['nombre']
            cargo.descripcion=request.POST['descripcion']
            if request.POST['estado']=="1":
                cargo.estado=True
            else:
                cargo.estado = False
            cargo.save()
            mensaje = "El registro se ha modificado exitosamente..!!"
    contexto = {
        'usuario': request.user,
        'empresa': user.empresa,
        'permisos': permisos,
        'funciones':funciones_usuario(permisos),
        'items': Items.objects.all().order_by("prioridad"),
        'departamentos':Departamento.objects.filter(empresa=user.empresa),
        'mensaje':mensaje,
        'cargo':cargo,
        'user2': user.is_admin,
    }
    return render(request, 'Talento_Humano/registroCargo.html', contexto)