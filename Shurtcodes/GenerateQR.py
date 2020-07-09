# -*- coding: utf-8 -*-
import qrcode
def CreateQR(path_out,textCreate):
    try:
        img = qrcode.make(textCreate)
        f = open(path_out+".png", "wb")
        img.save(f)
        f.close()
        print("mensaje: ","Proceso finalizado correctamente..!!")
    except Exception as error:
        print("Error: ",error)

CreateQR("qr_gen","http://colexin.bit-ec.com/")
