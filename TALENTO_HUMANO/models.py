from django.db import models
# Create your models here.
from CONFIGURACION.models import *

listEmpleados = ['nombre','apellido', 'ruc','email', 'fechaNacimiento','sexo','cargas','profesion','direccion','observaciones',
                 'fechaIngreso','fechaSalida', 'parroquia', 'estado']
class Empleado(models.Model):
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, blank=True, null=True)
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    ruc = models.CharField(max_length=13)
    email = models.EmailField(max_length=120)
    fechaNacimiento = models.DateField()
    sexo = models.CharField(max_length=20, blank=True, null=True, choices=(('M', 'Masculino'), ('F', 'Femenino')))
    cargas = models.CharField(max_length=2)
    profesion = models.CharField(max_length=100, blank=True, null=True,)
    telefono = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=200)
    observaciones = models.CharField(max_length=300, blank=True, null=True)
    fechaIngreso = models.DateField(blank=True, null=True)
    fechaSalida = models.DateField(blank=True, null=True)
    parroquia = models.ForeignKey(Lugares, on_delete=models.CASCADE, blank=True, null=True,)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return "%s | %s %s"%(self.ruc,self.nombre,self.apellido)

listAnios = ['anio','sueldoBasico','diasLaborables','diasMensuales','activado']
class Anio(models.Model):
    anio = models.CharField(max_length=4)
    empresa=models.ForeignKey(DatosEmpresa,on_delete=models.CASCADE,null=True,blank=True)
    sueldoBasico=models.DecimalField(max_digits=9, decimal_places=2,default=368.00)
    diasLaborables=models.IntegerField(default=360)
    diasMensuales=models.IntegerField(default=30)
    diasSemanales=models.IntegerField(default=5)
    horasmensuales=models.IntegerField(default=200)
    horassemanales=models.IntegerField(default=40)
    horasdiarias=models.IntegerField(default=8)
    activado=models.BooleanField(default=True)

    def __str__(self):
        return  self.anio

listFormaPagos = ['formaPago']
class FormaPago(models.Model):
    formaPago = models.CharField(max_length=60, default="EFECTIVO")

    def save(self):
        self.formaPago=self.formaPago.upper()
        super(FormaPago,self).save()

    def __str__(self):
        return self.formaPago

listRolPagos = ['empresa','numeroRol','fechaRol','PeridoRol']
class RolPagos(models.Model):
    empresa = models.ForeignKey(DatosEmpresa, blank=True, null=True, on_delete=models.CASCADE)
    numeroRol = models.CharField(max_length=10)
    fechaRol = models.DateField(auto_now_add=True)
    PeridoRol = models.CharField(max_length=20)

    def __str__(self):
        return self.numeroRol

listSueldos=['annio','empleado','sueldo','diasTrabajados','formaPago','estado']
class Sueldos(models.Model):
    empleado=models.ForeignKey(Empleado,on_delete=models.CASCADE)
    cargo=models.ForeignKey(Cargos,on_delete=models.CASCADE,null=True,blank=True)
    annio=models.ForeignKey(Anio,on_delete=models.CASCADE)
    sueldo = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    diasTrabajados = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    horasdiarias = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    totalHoras=models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    formaPago = models.ForeignKey(FormaPago, blank=True, null=True, on_delete=models.CASCADE)
    valor_hora=models.DecimalField(default=0.00, max_digits=9, decimal_places=6)
    estado=models.BooleanField(default=True)
    beneficio=models.BooleanField(default=False)

    def save(self):
        horas=float(self.diasTrabajados) * float(self.horasdiarias)
        valor=float(str(self.sueldo).replace("_","0"))/float(horas)
        self.valor_hora=valor
        self.totalHoras=horas
        super(Sueldos, self).save()

    def __str__(self):
        return "%s %s: %s"%(self.empleado,self.annio,self.sueldo)

listRemuneracion=['periodo','sueldo','xiiisueldo','xivsueldo','fondosreserva','vacaciones','otrosingresos','totalIngresos','aporteiess','prestamosiess','impuestoalarenta','anticiposueldo','descuento','otrosegresos','totalEgresos','total']
class Remuneraciones(models.Model):
    rol=models.ForeignKey(RolPagos,on_delete=models.CASCADE)
    sueldo=models.ForeignKey(Sueldos,on_delete=models.CASCADE)
    periodo=models.CharField(max_length=30,null=True,blank=True)
    dias=models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    fecha=models.DateField(auto_now_add=True,null=True,blank=True)
    sueldoInicial=models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    mes=models.CharField(max_length=2,default="00")
    xiiisueldo=models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    xivsueldo = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    fondosreserva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    vacaciones = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    otrosingresos = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    horasextras = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    totalIngresos = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    aporteiess = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iece=models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    prestamosiess=models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    impuestoalarenta = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    anticiposueldo = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    descuento = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    multas = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    otrosegresos = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    totalEgresos=models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total=models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def save(self):
        ingresos=float(self.horasextras)+float(self.sueldo.sueldo)+float(self.xiiisueldo)+float(self.xivsueldo)+float(self.fondosreserva)+float(self.vacaciones)+float(self.otrosingresos)
        self.totalIngresos=ingresos
        egresos=float(self.multas)+float(self.iece)+float(self.aporteiess)+float(self.prestamosiess)+float(self.impuestoalarenta)+float(self.anticiposueldo)+float(self.descuento)+float(self.otrosegresos)
        self.totalEgresos=egresos
        self.total=ingresos-egresos
        super(Remuneraciones,self).save()

    def __str__(self):
        return "%s"%self.fecha

listIngresosEgresos=['prioridad','tipo','nombre','campo','formula','atributo','estado','es_calculable']
class IngresosEgresos(models.Model):
    tipo=models.CharField(max_length=1, choices=(('I',"INGRESO"),('E','EGRESO')))
    nombre=models.CharField(max_length=60)
    formula=models.CharField(max_length=150,null=True,blank=True,default="0")
    campo=models.CharField(max_length=60,null=True,blank=True)
    atributo=models.CharField(max_length=60,default='',null=True,blank=True)
    estado=models.BooleanField(default=True)
    prioridad=models.IntegerField(default=0)
    decimales=models.IntegerField(default=2)
    tipo_campo=models.CharField(max_length=20,choices=(('text','text'),('number','number')),default='number')
    es_calculable=models.BooleanField(default=True)


    def save(self):
        self.nombre=self.nombre.upper()
        self.campo=self.nombre.replace(" ",'').lower()
        super(IngresosEgresos,self).save()