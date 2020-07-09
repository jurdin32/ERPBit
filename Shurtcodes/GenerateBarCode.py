# -*- coding: utf-8 -*-
import barcode
from barcode.writer import ImageWriter

def CreateBarCode(code,path_out,codigo):
    try:
        source = barcode.get(code, codigo, writer=ImageWriter())
        filename = source.save(path_out+"\\"+codigo)
        print("Archivo generado: ",filename)
        print("Proceso Completado con exito")
    except Exception as error:
        print("Error:",error)

CreateBarCode("code128","C:\\Users\\Lenovo\\Google Drive\\Proyectos_Drive\\ERPBit\\Shurtcodes","0000000000000000000000000000000000")
