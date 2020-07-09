# -*- coding: utf-8 -*-
import zeep as zeep
from dicttoxml import dicttoxml
import os
import subprocess
from pathlib import Path

from django.http import HttpResponseRedirect

from DOCUMENTOS_ELECTRONICOS.models import DatosDocumentos, Factura, GuiaRemision
from DOCUMENTOS_ELECTRONICOS.tasks import enviarPDF
from ERPBit.settings import BASE_DIR

def documentosXML(documento={},impuestos="",detalles="",factura=None):
    xml = dicttoxml(documento,root=False,attr_type=False)
    clave = factura.clave_acceso
    string = str(xml).replace("b'","").replace("'","").replace("<factura>","<factura id='comprobante' version='1.0.0'>").replace("%s",impuestos).replace("xt",detalles)
    # string = str(xml).replace("b'","").replace("'","").replace("<factura>","<factura id='comprobante' version='1.0.0'>").replace("xt",detalles)

    ruta=os.path.join(BASE_DIR, 'media/Facturacion/xml/'+clave+".xml")
    print(impuestos)
    if not os.path.isfile(os.path.join(BASE_DIR, 'media/Facturacion/xml/firmado/'+clave+".xml")):
        archivo=open(ruta,"w")
        archivo.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'+string)
        archivo.close()
        firmadoDocumentos(factura, 'media/Facturacion/xml/firmado')
    else:
        archivo = open(os.path.join(BASE_DIR, 'media/Facturacion/xml/firmado/'+clave+".xml"), "r")
        string=archivo.readlines()
        archivo.close()
    print(string)
    enviar_sri(clave,'media/Facturacion/xml/firmado/',factura.ambiente)
    return string


def GuiaRemisionXML(documento={},detalles="",guia=None):
    xml = dicttoxml(documento,root=False,attr_type=False)
    string = str(xml).replace("b'","").replace("'","").replace("<guia>","<guiaRemision id='comprobante' version='1.0.0'>").replace("</guia>","</guiaRemision>").replace("xt",detalles)
    ruta=os.path.join(BASE_DIR, 'media/Facturacion/xml/'+guia.clave_acceso+".xml")
    clave=guia.clave_acceso
    print("-----> Creando xml..!!!")
    if not os.path.isfile(os.path.join(BASE_DIR, 'media/Facturacion/xml/firmado/'+clave+".xml")):
        archivo=open(ruta,"w")
        archivo.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'+string)
        archivo.close()
        print("-----> Firmando xml..!!!")
        firmadoDocumentos(guia, 'media/Facturacion/xml/guias/firmado')
    else:
        archivo = open(os.path.join(BASE_DIR, 'media/Facturacion/xml/guias/firmado/'+clave+".xml"), "r")
        string=archivo.readlines()
        archivo.close()
    print(string)
    enviar_sri(clave,'media/Facturacion/xml/guias/firmado/',guia.ambiente)
    return string


def documentosRetencionXML(documento={},detalles="",retencion=None):
    xml = dicttoxml(documento,root=False,attr_type=False)
    clave = retencion.clave_acceso
    string = str(xml).replace("b'","").replace("'","").replace("<retencion>","<comprobanteRetencion id='comprobante' version='1.0.0'>").replace("</retencion>","</comprobanteRetencion>").replace("xs",detalles)
    ruta=os.path.join(BASE_DIR, 'media/Facturacion/xml/'+clave+".xml")

    if not os.path.isfile(os.path.join(BASE_DIR, 'media/Facturacion/xml/firmado/'+clave+".xml")):
        archivo=open(ruta,"w")
        archivo.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'+string)
        archivo.close()
        firmadoDocumentos(retencion, 'media/Facturacion/xml/retencion/firmado')
    else:
        archivo = open(os.path.join(BASE_DIR, 'media/Facturacion/xml/retencion/firmado/'+clave+".xml"), "r")
        string=archivo.readlines()
        archivo.close()
    print(string)
    enviar_sri(clave,'media/Facturacion/xml/retencion/firmado/',retencion.ambiente)
    return string


def firmadoDocumentos(fact,salida):
    clave=fact.clave_acceso
    datos=DatosDocumentos.objects.get(empresa=fact.empresa,estado=True)
    ruta = os.path.join(BASE_DIR, 'media/Facturacion/xml/'+clave+".xml")
    cert=os.path.join(BASE_DIR, 'media/'+str(datos.firmaElectronica))
    print(datos.firmaElectronica,datos.claveFirma)
    java = os.path.join(BASE_DIR, 'static/Java/comprobantes.jar')
    #intenta hacerlo con Windows
    javapath=os.path.join(BASE_DIR, 'static/Java/jdk1.7.0_80/bin/java.exe')
    firmado=os.path.join(BASE_DIR,salida)
    args=[java,ruta,cert,datos.claveFirma,firmado,clave+".xml"]
    subprocess.call([javapath, '-jar']+list(args))
    print("Windows..!")
    print("El documento se firmo, con archivo windows: ", clave)
    try:
        #intentando con linux
        print("Se intentara con el jdk de linux")
        javapath = os.path.join(BASE_DIR, 'static/Java/Linux/jdk1.7.0_80/bin/java')
        firmado = os.path.join(BASE_DIR, salida)
        args = [java, ruta, cert, datos.claveFirma, firmado, clave + ".xml"]
        subprocess.call([javapath, '-jar'] + list(args))
        print("Linux..!")
        print("El documento se firmo, con archivo linux: ", clave)
    except:
        print("no hay error..!!")


#corregir
def enviar_sri(clave,path,ambiente):
    url=""
    print("Informacion: ",clave,path,ambiente)
    if int(ambiente)==1: #ambiente de pruebas
        print('Ambiente de pruebas')
        url='https://celcer.sri.gob.ec/comprobantes-electronicos-ws/RecepcionComprobantesOffline?wsdl' #ruta al servidor de pruebas
    elif int(ambiente)==2:
        print('Ambiente de produccion')
        url='https://cel.sri.gob.ec/comprobantes-electronicos-ws/RecepcionComprobantesOffline?wsdl'

    firmado=os.path.join(BASE_DIR, path+clave+'.xml')
    print ("Ruta del archivo firmado..!",Path(firmado))

    respuestas=os.path.join(BASE_DIR, 'media/Facturacion/xml/response/resp-'+clave+'.json')

    comprobante=open(Path(firmado), "rb") #apertura del archivo xml
    xmlBytes = comprobante.read()# creando mapa de bits del comprobante
    client = zeep.Client(wsdl=url)#creando una instancia de zeep cliente
    print("Inicia el proceso de envio..!!")
    result=client.service.validarComprobante(xmlBytes)
    jsonarchivo=open(respuestas,"w")
    jsonarchivo.write(str(result))
    jsonarchivo.close()
    print("Respuesta: ",result)# respuesta del servidor
    factura=None
    try:
        factura=Factura.objects.get(clave_acceso=clave)
        print("Es una factura: ",factura.clave_acceso)

        if int(factura.ambiente) == 2:
            print("Enviando por correo electronico..!!: ", factura.cliente.email)
            enviarPDF.delay(factura)
    except:
        print("no es factura")

    guia=None
    try:
        guia=GuiaRemision.objects.get(clave_acceso=clave)
        print("Es una guia o una retencion: ",guia.clave_acceso)

        if int(guia.ambiente) == 2:
            print("Enviando por correo electronico..!!: ", guia.factura.cliente.email)
            enviarPDF.delay(factura)
    except:
        print("no es guia")




def json_sri(clave,ambiente,path):
    url = ""
    ruta = os.path.join(BASE_DIR, path)
    print (ruta)
    if int(ambiente)==1:
        print("Ambiente de pruebas")
        url = 'https://celcer.sri.gob.ec/comprobantes-electronicos-ws/AutorizacionComprobantesOffline?wsdl'
    elif int(ambiente)==2:
        print("Ambiente de Produccion")
        url = 'https://cel.sri.gob.ec/comprobantes-electronicos-ws/AutorizacionComprobantesOffline?wsdl'
    client = zeep.Client(wsdl=url)
    respuesta=client.service.autorizacionComprobante(clave)
    print(respuesta)
    archivo=open(ruta,"w")
    archivo.write(str(respuesta))
    archivo.close()
    return respuesta


