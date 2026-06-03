#importacion de librerias
import random
from datetime import *
import faker
from ddlc import *
fk=faker.Faker("es_ES")

#Tupla global de tipos de sangre
tipoSangre=("O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-")

#definicion de funciones
def sacarTipoSangre(metodo, ptipo, ptupla):
    """
    funcion: saca el tipo de sangre de la tupla o saca el numero del tipo de sangre
    entradas:
    -ptipo: tipo de sangre
    -ptupla: tupla con tipos de  sangre
    salidas:
    ptupla[ptipo-1]: tipo de sangre
    """
    if metodo=="TP": #tipo de sangre
        return ptupla[ptipo-1]
    if metodo=="NTP": #numero del tipo de sangre
        for i in range(len(ptupla)):
            if ptupla[i]==ptipo:
                return[i]
        return
    return


def generarNombreGenero():
    """
    funcion: genera un nombre totalmente aleatorio y su genero
    entradas: no hay
    salidas: 
    -tuple((fk.name_male()).split()) (tupla): nombre generado guardado en tupla
    -genero(booleano): el genero del nombre
    """
    genero=random.choice([True, False])
    if genero:
        nombre=fk.first_name_male().split()
        nombre.append(fk.last_name())
        nombre.append(fk.last_name())
        return nombre, genero
    nombre=fk.first_name_female().split()
    nombre.append(fk.last_name())
    nombre.append(fk.last_name())
    return nombre, genero

def validarDonante(pmatriz,pcedula):
    """
    funcion: valdiar que el paciente no esté repetido
    entrada:
    -pmatriz: matriz con pacientes
    -pcedula: cedula del paciente
    """
    for i, persona in enumerate(pmatriz):
        if persona[1] == pcedula:
            return True, i

    return False, -1


def generarCedula(pdonantes):
    """
    funcion: genera una cedula aleatoria con estadistica de nacimientos
    entrada: pdonantes: matriz de donantes
    salidas: cedula(string): cedula armada
    """
    prob=random.randint(1,100)
    if prob>=1 and prob<=40:
        cedula="1"
    elif prob>40 and prob<=60:
        cedula="2"
    elif prob>60 and prob<=72:
        cedula="3"
    elif prob>72 and prob<=79:
        cedula="4"
    elif prob>79 and prob<=85:
        cedula="5"
    elif prob>85 and prob<=92:
        cedula="6"
    elif prob>92 and prob<=97:
        cedula="7"
    elif prob==98:
        cedula="8"
    else:
        cedula="9"
    for i in range(8):
        cedula+=str(random.randint(0,9))
    if pdonantes==[]:
        return int(cedula)
    if validarDonante(pdonantes, cedula)[0]:
        generarCedula(pdonantes)
    return int(cedula)

def generarTipoSangre():
    """
    funcion: genera un tipo aleatoria con estadistica
    entrada: no hay
    salidas: int: tipo de sangre
    """
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
    """
    funcion: genera el genero aleatoriamente
    entrada: no hay
    salida: bool(random.randint(0,1)): genero aleatorio
    """
    return bool(random.choice([True, False]))

def generarFechaN():
    """
    funcion: genera una fecha aleatoria
    entradas: no hay
    salidas: (dia,mes,anno): tupla con fecha separada en dia, mes y año
    """
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
    """
    funcion: gener aun peso aleatorio entre 51 y 119 kg
    entradas: no hay
    salidas: random.randint(51,119) numero aleatorio entre 51 y 119
    """
    return random.randint(51,119)

def generarCorreo(pnombre):
    """
    funcion genera un correo con formato aleatorio dependiendo del nombre de la persona
    entrada:
    -pnombre: nombre de la persona a la que se le generará el nombre
    salidas:
    -correo: correo construido aleatoriamente
    """
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
    """
    funcion: genera un numero de telefono aleatorio
    entradas: no hay
    salidas:
    -num: numero construido despues de generarse aleatoriamente
    """
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
    """
    genera un estado aleatorio con 75% de probabilidad de ser 1
    entradas: no hay
    salidas: int: 1 o 0
    """
    prob=random.randint(0,100)
    if prob>=0 and prob<=75:
        return 1
    return 0

def generarJustificacion():
    """
    funcion: genera alatoriamente una justificacion en caso de que su estado aleatorio hubiera sido 0
    entradas: no hay
    salidas:
    -random.randint(1,7): numero aleatorio entre 1 y 7
    """
    return random.randint(1,7)

def generarDonantes(pdonantes,pbaseDatos):
    donantes=[]
    for i in range(pdonantes):
        nombre, sexo = generarNombreGenero()
        cedula=generarCedula(pbaseDatos)
        tipoSangre=generarTipoSangre()
        fechaN=generarFechaN()
        peso=generarPeso()
        correo=generarCorreo(nombre)
        telefono=generarTelefono()
        estado=generarEstado()
        if bool(estado):
            justific=0
        else:
            justific=generarJustificacion()
        donantes.append([tuple(nombre),cedula,tipoSangre,sexo,fechaN,float(peso),correo,telefono,estado,justific])
    return donantes