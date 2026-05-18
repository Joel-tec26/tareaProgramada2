baseDatos=[]
from funcionesAlexis import *

def generarDonantesAux(pbaseDatos):
    try:
        donantes=int(input("Escriaba cuantos donantes quiere generar: "))
    except:
        print("debe escribir un valor numerico")
        input("presione ENTER para continuar")
        return
    if donantes<=0:
        print("debe escribir solo un número positivo")
        input("presione ENTER para continuar")
        return
    for i in generarDonantes(donantes):
        pbaseDatos.append(i)
    return pbaseDatos


baseDatos=generarDonantesAux(baseDatos)
print(baseDatos)