import math

def verificar_cedula(cedula=""):
    if len(cedula)<9:
        return False
    elif len(cedula)>9 and len(cedula)<=13:
        ultimo_digito = int(cedula[9])
        suma=0
        cont = 2
        lista= list(cedula[0:9])
        print(lista)
        for i in lista:
            print(i,"*",cont,"=",int(i)*cont)
            valor=int(i)*cont
            if valor>9:
                suma+=valor-9
            else:
                suma+=valor
            if cont==2:
                cont=1
            else:
                cont=2
    if (math.ceil((suma / 10)) * 10 - suma) == int(ultimo_digito):
        return True

    else:
        return False
    # print (suma)

# print(verificar_cedula('0992876689001'))