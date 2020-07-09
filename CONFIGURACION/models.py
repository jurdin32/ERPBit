from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe
# Create your models here.

listLugares = ['id','lugar','nombre']
class Lugares(models.Model):
    lugar = models.ForeignKey('self' , on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=60)
    pais =  models.BooleanField(default=False)
    provincia = models.BooleanField(default=False)
    ciudad = models.BooleanField(default=False)
    parroquia= models.BooleanField(default=False)

    def save(self, force_insert=False, force_update=False, using=None,update_fields=None):
        self.nombre=self.nombre.upper()
        super(Lugares,self).save()

    def __str__(self):
        return "%s"%(self.nombre)

    class Meta:
        verbose_name_plural = "0. Paises, Provincias, Ciudades, Parroquias"


listDatosEmpresa = ['id','razonSocial','nombreComercial','ruc','direccionMatriz','telefono', 'email', 'logo']
class DatosEmpresa(models.Model):
    usuario=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True,unique=True)
    razonSocial = models.CharField(max_length=100,null=True,blank=True)
    nombreComercial = models.CharField(max_length=100,null=True,blank=True)
    ruc = models.CharField(max_length=13,null=True,blank=True)
    obligado_llevar_contabilidad=models.BooleanField(default=False)
    contribuyenteEspecial=models.BooleanField(default=False)
    contribuyenteEspecialNumero=models.CharField(max_length=10,null=True,blank=True)
    parroquia=models.ForeignKey(Lugares,on_delete=models.CASCADE,null=True,blank=True)
    direccionMatriz = models.CharField(max_length=100,null=True,blank=True)
    telefono = models.CharField(max_length=10,null=True,blank=True)
    convencional = models.CharField(max_length=10,null=True,blank=True)
    email = models.EmailField(max_length=60,null=True,blank=True)
    logo = models.ImageField(upload_to='Logo', null=True, blank=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return "%s | %s"%(self.razonSocial,self.nombreComercial)
    # class Meta:
        verbose_name_plural = "1. Datos de la Empresa"




listDepartamentos = ['id','nombre','descripcion', 'estado']
class Departamento(models.Model):
    empresa = models.ForeignKey(DatosEmpresa, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    estado = models.BooleanField(default=True)

    def __str__(self):
        if self.empresa:
            return self.empresa.nombreComercial
        else:
            return ""

    class Meta:
        verbose_name_plural = "2. Departamentos de la Empresa"

listCargos=['empresa','id','departamento','cargo','descripcion','estado']
class Cargos(models.Model):
    empresa = models.ForeignKey(DatosEmpresa, on_delete=models.CASCADE, null=True, blank=True)
    departamento=models.ForeignKey(Departamento,on_delete=models.CASCADE)
    cargo=models.CharField(max_length=100)
    descripcion = models.TextField()
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.cargo

    class Meta:
        verbose_name_plural = "3. Cargos del Departamento"

ListGrupos = ['id','empresa','nombre','descripcion','estado']
class Grupo(models.Model):
    empresa=models.ForeignKey(DatosEmpresa,on_delete=models.CASCADE,null=True,blank=True)
    nombre = models.CharField(max_length=100)
    descripcion=models.TextField(null=True,blank=True)
    estado=models.BooleanField(default=True)

    def __str__(self):
        return "%s | %s | %s"%(self.empresa.usuario.username,self.nombre,self.empresa)

    class Meta:
        verbose_name_plural = "4. Grupos Organizacionales"

listFunciones=['id','nombre','activo']
class Funciones(models.Model):
    nombre=models.CharField(max_length=60)
    activo=models.BooleanField(default=True)
    icono=models.CharField(max_length=120, null=True,blank=True)
    descripcion=models.TextField(null=True,blank=True)

    def save(self):
        self.nombre=self.nombre.upper()
        super(Funciones, self).save()

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "5. Funciones del Sistema"

listItems=['funcion','prioridad','nombre','activo']
class Items(models.Model):
    funcion =  models.ForeignKey(Funciones, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=60)
    enlace=models.CharField(max_length=120,null=True,blank=True)
    prioridad=models.IntegerField(default=0)
    nuevo=models.BooleanField(default=False)
    activo = models.BooleanField(default=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.prioridad==0:
            self.prioridad=Items.objects.filter(funcion=self.funcion).count()+1
        super(Items, self).save()


    def __str__(self):
        return "%s | %s"%(self.funcion.nombre,self.nombre)

listPermiso=['id','grupo','item', 'funcion']
class Permiso(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE,null=True,blank=True)
    item = models.ForeignKey(Items, on_delete= models.CASCADE, null=True, blank=True)


    def funcion(self):
        return self.item.funcion.nombre

    def __str__(self):
        return self.item.nombre

    class Meta:
        verbose_name_plural = "6. Permisos"

listReportes=['empresa','texto','fondo','lineas','encabezado_fondo','texto_encabezado','ruta_imagenes']
class Reportes(models.Model):
    empresa=models.ForeignKey(DatosEmpresa,on_delete=models.CASCADE,null=True,blank=True)
    color_texto=models.CharField(max_length=50, default="#000000")
    color_fondo=models.CharField(max_length=50, default="#FFFFFF")
    color_lineas=models.CharField(max_length=50,default="#0B3B2E")
    color_encabezados_tablas=models.CharField(max_length=50,default="#0B3B2E")
    color_encabezados_tablas_texto = models.CharField(max_length=50, default="#0B3B2E")
    encabezado=models.ImageField(upload_to='reportes/encabezado',null=True,blank=True)
    ruta_imagenes=models.CharField(max_length=120, default="http://localhost:8000/")

    def texto(self):
        return mark_safe('<div style="width: 80px; height: 10px;background-color:%s"></div>'%self.color_texto)

    def fondo(self):
        return mark_safe('<div style="width: 80px; height: 10px;background-color:%s"></div>'%self.color_fondo)

    def lineas(self):
        return mark_safe('<div style="width: 80px; height: 10px;background-color:%s"></div>'%self.color_lineas)

    def encabezado_fondo(self):
        return mark_safe('<div style="width: 80px; height: 10px;background-color:%s"></div>' % self.color_encabezados_tablas)

    def texto_encabezado(self):
        return mark_safe('<div style="width: 80px; height: 10px;background-color:%s"></div>' % self.color_encabezados_tablas_texto)

    texto.short_description="Color del Texto"
    fondo.short_description = "Color del Fondo"
    lineas.short_description = "Color de las Líneas"
    encabezado_fondo.short_description="Color del Fondo para el Encabezado"
    texto_encabezado.short_description="Color del Texto en el Encabezado"

    def __str__(self):
        return self.empresa.nombreComercial

    class Meta:
        verbose_name_plural = "7. Configuraciones del Reporte"


listHelper=['titulo','imagenes','descripciones','horaFecha']
class Helpers(models.Model):
    titulo=models.CharField(max_length=150,help_text="Titulos")
    imagen=models.ImageField(upload_to="helpers")
    descripcion=RichTextField(null=True,blank=True)
    horaFecha=models.DateTimeField(auto_now=True)

    def imagenes(self):
        return mark_safe("""<img src="/media/%s" style="width: 100px">"""%self.imagen)

    def descripciones(self):
        return mark_safe(self.descripcion)

    def __str__(self):
        return self.titulo

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.titulo = str.upper(self.titulo)
        super(Helpers, self).save()

class HelpersDetalles(models.Model):
    helper=models.ForeignKey(Helpers, on_delete=models.CASCADE,null=True,blank=True)
    tituloGeneral=models.CharField(max_length=150, null=True,blank=True)
    detalles=RichTextField()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.tituloGeneral=str.upper(self.tituloGeneral)
        super(HelpersDetalles, self).save()
