def claveAcceso(fecha, tipoComprobante, ruc, ambiente, codEstablecimiento,codigoSucursal, secuencial, codigoNum, tipoEmision="1"):
    union = fecha + tipoComprobante + ruc + ambiente + codEstablecimiento + codigoSucursal + secuencial + codigoNum + tipoEmision
    print(union)
    lista = [i for i in union]
    n = len(lista)
    print("Cantidad: ", n)
    digito = 0
    pibot = 2
    for i in range(n):
        n = n - 1
        digito += int(lista[n]) * pibot
        pibot = pibot + 1
        if pibot > 7:
            pibot = 2
    digito = 11 - (digito % 11)
    if digito == 10:
        digito = 1
    elif digito == 11:
        digito = 0
    union = union + str(digito)
    print("tamanio de la clave de acceso: ",len(union))
    return union 


# print(claveAcceso('20062019','01','0704548536001','2','001','001','000000351','00000000','1'))
print(claveAcceso('01082019','01','0704548536001','2','001','001','000000481','00000000','1'))

