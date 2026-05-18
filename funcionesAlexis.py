#importacion de librerias
import random
from datetime import *

#Tupla global de tipos de sangre
tipoSangre=("O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-")

#definicion de funciones
def generarNombre():
    nombres=open("nombres.txt", encoding="utf8")
    apellidos=open("apellidos.txt", encoding="utf8")
    apellidoRan=random.randint(0,234)
    apellido2Ran=random.randint(0,112)
    nombreRan=random.randint(0,112)
    nombre=[nombres.readline(nombreRan).strip(), apellidos.readline(apellidoRan).strip(), apellidos.readline(apellido2Ran).strip()]
    nombres.close()
    apellidos.close()
    return nombre

def generarCedula():
    prob=random.randint(1,100)
    if prob>=0 and prob<=40:
        cedula="1 "
    elif prob>40 and prob<=60:
        cedula="2 "
    elif prob>60 and prob<=72:
        cedula="3 "
    elif prob>72 and prob<=79:
        cedula="4 "
    elif prob>79 and prob<=85:
        cedula="5 "
    elif prob>85 and prob<=92:
        cedula="6 "
    elif prob>92 and prob<=97:
        cedula="7 "
    elif prob==98:
        cedula="8 "
    else:
        cedula="9"
    for i in range(8):
        cedula+=str(random.randint(0,9))
        if i==3:
            cedula+=" "
    return cedula

def generarTipoSangre():
    prob=random.randint(1,100)
    if prob>=0 and prob<=37: #O+
        return 0
    elif prob>37 and prob<=73: #A+
        return 2
    elif prob>73 and prob<=81: #B+
        return 4
    elif prob>81 and prob<=88: #O-
        return 1
    elif prob>88 and prob<=93: #A-
        return 3
    elif prob>93 and prob<=96: #AB+
        return 6
    elif prob>96 and prob<=98: #B-
        return 5
    else:                      #AB-
        return 7
    
def generarSexo():
    return bool(random.randint(0,1))

def generarFechaN():
    annoActual=int(datetime.now().strftime("%Y"))
    anno=random.randint(annoActual-65, annoActual-18)
    mes=random.randint(1,12)
    if mes==1 or mes==3 or mes==5 or mes==7 or mes==8 or mes==10 or mes==12:
        dia=random.randint(1,31)
    elif mes==2:
        if anno%4==0 and anno%100!=0:
            dia=random.randint(1,29)
        else:
            dia=random.randint(1,28)
    else:
        dia=random.randint(1,30)
    return (dia,mes,anno)

def generarPeso():
    return random.randint(51,119)

def generarCorreo(pnombre):
    correo=""
    probTipo=random.randint(1,4)
    probCorreo=random.randint(0,1)
    probNum=random.randint(0,1)
    if probCorreo:
        if probNum:
            correo+=pnombre[0][0]+pnombre[1]+str(random.randint(1,9))+str(random.randint(1,9))
        else:
            correo+=pnombre[0][0]+pnombre[1]
    else:
        if probNum:
            correo+=pnombre[0]+str(random.randint(1,9))+str(random.randint(1,9))
        else:
            correo+=pnombre[0]
    match probTipo:
        case 1:
            correo+="@costarricense.cr"
        case 2:
            correo+="@racsa.go.cr"
        case 3:
            correo+="@ccss.sa.cr "
        case 4:
            correo+="@gmail.com "   
    return correo

def generarTelefono():
    num=str(random.randint(2,9))
    while True:
        if num!="3" and num!="5":
            for i in range(7):
                num+=str(random.randint(0,9))
                if i==2:
                    num+="-"
            break
        else:
            num=str(random.randint(2,9))
    return num

def generarEstado():
    prob=random.randint(0,100)
    if prob>=0 and prob<=75:
        return 1
    return 0

def generarJustificacion():
    return random.randint(1,7)

def generarDonantes(pdonantes):
    donantes=[]
    for i in range(pdonantes):
        nombre=generarNombre()
        cedula=generarCedula()
        tipoSangre=generarTipoSangre()
        sexo=generarSexo()
        fechaN=generarFechaN()
        peso=generarPeso()
        correo=generarCorreo(nombre)
        telefono=generarTelefono()
        estado=generarEstado()
        if bool(estado):
            justific=0
        else:
            justific=generarJustificacion()
        donantes.append([nombre,cedula,tipoSangre,sexo,fechaN,peso,correo,telefono,estado,justific])
    return donantes