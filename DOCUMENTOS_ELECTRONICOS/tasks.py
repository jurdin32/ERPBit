# -*- coding: utf-8 -*-
from celery import task

from ERPBit.settings import BASE_DIR
from Shurtcodes.emailes import send_email
import os


@task
def enviarPDF(factura):
    try:
        subject="DOCUMENTO ELECTRÓNICO"
        message="Su factura electrónica, se ha emitido, acontinuación el detalle de los archivos, podrá descargar desde la siguiente dirección: https://app.bit-ec.com/noticias/consultas"
        from_email="ventas@bit-ec.com"
        clave=str(factura.clave_acceso)
        email=str(factura.cliente.email)
        print(clave,email)
        to_email = [email]
        if factura.tipo=="FACTURA":
            rutaXML =os.path.normpath(os.path.join(BASE_DIR, 'media/Facturacion/xml/firmado/'+clave+'.xml'))
            rutaPDF = os.path.normpath(os.path.join(BASE_DIR, 'media/Facturacion/xml/firmado/'+clave+'.pdf'))
            attachment = [rutaXML,rutaPDF,]
            print("paths: ",rutaPDF,rutaXML)
        else:
            rutaPDF = os.path.normpath(os.path.join(BASE_DIR, 'media/proformas/' + factura.secuencial +'.pdf'))
            message = "Su Proforma electrónica, esta disponible, acontinuación el detalle de los archivos"
            attachment = [rutaPDF,]
        send_email(subject, message, from_email, to_email=to_email, attachment=attachment)
    except Exception as error:
        print("Error ocurrido al enviar el mensaje",error)
