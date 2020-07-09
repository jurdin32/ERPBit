from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.http import HttpResponse
import os
from ERPBit.settings import BASE_DIR


def render_to_pdf_factura(template_src,context_dict={},factura=None):
    ruta=''
    if factura.tipo=="FACTURA":
        ruta = os.path.join(BASE_DIR, 'media/Facturacion/xml/firmado/' + factura.clave_acceso + ".pdf")
    else:
        ruta = os.path.join(BASE_DIR, 'media/proformas/' + factura.secuencial + ".pdf")
    template=get_template(template_src)
    html=template.render(context_dict)
    result=BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf8")), result)
    archivo=open(ruta,"w+b")
    archivo.write(result.getvalue())
    archivo.close()
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type="application/pdf")
    return None


def render_to_pdf(template_src,context_dict={},objeto=None):
    template=get_template(template_src)
    html=template.render(context_dict)
    result=BytesIO()
    pdf=pisa.pisaDocument(BytesIO(html.encode("utf8")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type="application/pdf")
    return None