# creado por: Alexis Torres y Joel Porras
# fecha de creacion: 2/06/2026
# ultima modificación: 
# version: 3.14

# imporaticion de librerias
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk
import webbrowser
import random
from datetime import *
import faker
fk=faker.Faker("es_ES")
from manejoArchivos import *

# variables globales
provinciasDiccionario = {
    "1": ["San José", ["El Banco Nacional de sangre", "Hospital México", "Hospital San Juan de Dios"]],
    "2": ["Alajuela", ["Hospital San Rafael de Alajuela", "Hospital de San Ramón", "Hospital del Cantón Norteño"]],
    "3": ["Cartago", ["Hospital Max Peralta"]],
    "4": ["Heredia", ["Hospital San Vicente de Paúl"]],
    "5": ["Guanacaste", ["Hospital La Anexión en Nicoya", "Hospital Enrique Baltodano de Liberia"]],
    "6": ["Puntarenas", ["Hospital Monseñor Sanabria"]],
    "7": ["Limón", ["Hospital Tony Facio", "Hospital de Guápiles"]],
    "8": ["Naturalizado", ["Sede Central de Donación"]]}

archivoDonadores = "donadores.dat"
tipoSangre = ("O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-")

# definicion de funciones
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
                return i
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
    for i in range(len(pmatriz)):
        if pmatriz[i][1] == pcedula:
            return True, i
    return False, len(pmatriz)


def generarCedula(pdonantes):
    """
    funcion: genera una cedula aleatoria con estadistica de nacimientos
    entrada: pdonantes: matriz de donantes
    salidas: cedula(string): cedula armada
    """
    prob=random.randint(1,100)
    if prob>=1 and prob<=40:
        cedula="1-"
    elif prob>40 and prob<=60:
        cedula="2-"
    elif prob>60 and prob<=72:
        cedula="3-"
    elif prob>72 and prob<=79:
        cedula="4-"
    elif prob>79 and prob<=85:
        cedula="5-"
    elif prob>85 and prob<=92:
        cedula="6-"
    elif prob>92 and prob<=97:
        cedula="7-"
    elif prob==98:
        cedula="8-"
    else:
        cedula="9-"
    for i in range(8):
        cedula+=str(random.randint(0,9))
        if i==3:
            cedula+="-"
    if pdonantes==[]:
        return cedula
    if validarDonante(pdonantes, cedula)[0]:
        return generarCedula(pdonantes)

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
            correo+="@ccss.sa.cr"
        case 4:
            correo+="@gmail.com"   
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

def generarDonantes(pdonantes, pbaseDatos):
    """
    funcion: Genera una lista de donantes con datos aleatorios en el mismo
    formato que un registro insertado manualmente.
    entradas:
    - pdonantes (int): cantidad de donantes a generar.
    - pbaseDatos (list): matriz actual de donadores, usada para evitar
      cédulas duplicadas.
    salidas:
    - donantes (list): lista de registros generados, donde cada registro
      es una lista con la siguiente estructura:
        [0] nombre     (list)  : lista con nombre(s) y apellidos.
        [1] cedulaInt  (int)   : cédula sin guiones como entero.
        [2] tipoSangre (int)   : índice del tipo de sangre (0-7).
        [3] sexo       (bool)  : True = masculino, False = femenino.
        [4] fechaN     (tuple) : fecha de nacimiento como (dia, mes, anno).
        [5] peso       (float) : peso en kilogramos.
        [6] correo     (str)   : correo electrónico.
        [7] telefono   (str)   : número de teléfono.
        [8] estado     (int)   : 1 = activo, 0 = inactivo.
        [9] justific   (int)   : causa de rechazo (1-7), o 0 si activo.
    """
    donantes = []
    for i in range(pdonantes):
        nombre, sexo = generarNombreGenero()
        cedula = generarCedula(pbaseDatos)
        tipoSangreGen = generarTipoSangre()
        fechaN = generarFechaN()
        peso = generarPeso()
        correo = generarCorreo(nombre)
        telefono = generarTelefono()
        estado = generarEstado()
        justific = 0 if bool(estado) else generarJustificacion()
        cedulaInt = int(cedula.replace("-", ""))
        donantes.append([
            nombre,
            cedulaInt,
            tipoSangreGen,
            sexo,
            fechaN,
            float(peso),
            correo,
            telefono,
            estado,
            justific
        ])
    return donantes

# joel

# procesar

def buscarDonador(cedulaTarget, matrizABuscar):
    """
    funcion: Buscar un donador mediante búsqueda binaria.
    entradas:
    - cedulaTarget: cédula a buscar.
    - matrizABuscar: matriz ordenada de donadores.
    salidas:
    - Tupla con el resultado de la búsqueda y la posición encontrada o de inserción.
    """
    cedulaInt = int(cedulaTarget.replace("-", ""))
    izquierda = 0
    derecha = len(matrizABuscar) - 1
    
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        cedulaMedio = int(str(matrizABuscar[medio][1]).replace("-", ""))
        
        if cedulaMedio == cedulaInt:
            return True, medio
        elif cedulaMedio < cedulaInt:
            izquierda = medio + 1
        else:
            derecha = medio - 1
            
    return False, izquierda

def calcularEdad(fechaNacimientoStr):
    """
    funcion: Calcular la edad a partir de una fecha de nacimiento.
    entradas:
    - fechaNacimientoStr: fecha en formato DD/MM/AAAA.
    salidas:
    - Edad calculada en años.
    """
    hoy = datetime.now()
    fechaNac = datetime.strptime(fechaNacimientoStr, "%d/%m/%Y")
    return hoy.year - fechaNac.year - ((hoy.month, hoy.day) < (fechaNac.month, fechaNac.day))

def obtenerMensajeEdad(fechaNacimientoStr):
    """
    funcion: Generar un mensaje según la edad del posible donador.
    entradas:
    - fechaNacimientoStr: fecha en formato DD/MM/AAAA.
    salidas:
    - Mensaje indicando si puede donar sangre.
    """
    if calcularEdad(fechaNacimientoStr) >= 18:
        return "Dado su fecha de nacimiento usted ya puede ser donador."
    return "Dado su fecha de nacimiento usted aún no puede ser donador."

def obtenerLugarDonacion(cedula, pprovincias):
    """
    funcion: Obtener los lugares sugeridos para donar según la provincia.
    entradas:
    - cedula: cédula de la persona.
    - pprovincias: diccionario con provincias y hospitales.
    salidas:
    - Mensaje con los lugares de donación recomendados.
    """
    primerDigito = cedula[0]
    if primerDigito == "8":
        return "Casos especiales de las cédulas que donen en San José. Centro asignado Sede Central de Donación."
    if primerDigito in pprovincias:
        provincia = pprovincias[primerDigito][0]
        hospitales = " o ".join(pprovincias[primerDigito][1])
        return f"Dado que usted nació en la provincia de {provincia}, usted podría donar en {hospitales}."
    return "Provincia no encontrada."

def obtenerMensajePeso(pesoStr):
    """
    funcion: Generar un mensaje según el peso ingresado.
    entradas:
    - pesoStr: peso de la persona.
    salidas:
    - Mensaje relacionado con la aptitud para donar.
    """
    peso = float(pesoStr)
    if peso <= 50:
        return "Usted debe pesar más de 50 kgms para poder ser donador."
    if 50 < peso <= 110:
        return "Usted posee un peso adecuado, correcto para ser donador de sangre."
    return "Dado su sobre peso, no es posible donar sangre."

def obtenerInformacionResaltadaSangre(tipoSangreStr):
    """
    funcion: Brindar información y recomendaciones según el tipo de sangre.
    entradas:
    - tipoSangreStr: tipo de sangre del donador.
    salidas:
    - Mensaje con recomendaciones de donación.
    """
    tipoSangreStr = tipoSangreStr.upper()
    recomendaciones = {
        "A+": "se les recomienda que donen sangre entera y plaquetas.",
        "A-": "se les recomienda que donen sangre entera y glóbulos rojos dobles.",
        "B+": "pueden lograr el mayor impacto con donaciones de sangre entera y de glóbulos rojos dobles.",
        "B-": "se les recomienda que donen sangre entera o plaquetas.",
        "O+": "se les recomienda donar glóbulos rojos dobles y sangre entera.",
        "O-": "se les recomienda donar glóbulos rojos dobles y sangre entera.",
        "AB+": "se les recomienda hacer donaciones de plaquetas y de plasma.",
        "AB-": "se les recomienda donar plaquetas y plasma."
    }
    baseMensaje = f"Conoce tu tipo de sangre {tipoSangreStr}: A los donantes con este tipo {recomendaciones.get(tipoSangreStr, '')}"
    if tipoSangreStr in ["A+", "A-"]:
        baseMensaje += "\n\nAdemás, se le sugiere ver el video de Particularidades de la sangre tipo A: Responde diferente al estrés según la ciencia."
        
    return baseMensaje

# reportes
#1
def procesarReportePorProvinciaHtml(idProvinciaSeleccionada, pdonadores, pprovincias):
    """
    funcion:
    Genera un reporte HTML con los donadores pertenecientes a una provincia específica.
    entradas:
    - idProvinciaSeleccionada: identificador de la provincia.
    - pdonadores: matriz con los registros de donadores.
    - pprovincias: diccionario con las provincias.
    salidas:
    - Archivo HTML generado y abierto en el navegador.
    """
    fechaHoraActual = datetime.now().strftime("%d/%m/%Y %I:%M %p")
    nombreProvinciaSeleccionada = pprovincias.get(idProvinciaSeleccionada, ["Desconocida"])[0]
    filasHtml = ""
    contadorFilas = 0
    for donador in pdonadores:
        cedula = str(donador[1])
        idProvinciaDonador = cedula[0]
        if idProvinciaDonador == idProvinciaSeleccionada:
            contadorFilas += 1
            cedula = donador[1]
            idProvinciaDonador = str(cedula)[0]
            nombreCompleto = " ".join(donador[0])
            lugarDonacion = obtenerLugarDonacionCorto(str(donador[1]), pprovincias)
            tipoSangreStr = tipoSangre[donador[2]]
            estado = "Activo" if donador[8] == 1 else "Inactivo"
            filasHtml += f"""        <tr>
            <td>{cedula}</td>
            <td>{nombreCompleto}</td>
            <td>{tipoSangreStr}</td>
            <td>{lugarDonacion}</td>
            <td>{estado}</td>
        </tr>\n"""

    if contadorFilas == 0:
        messagebox.showinfo("Información", f"No se encontraron donadores registrados en la provincia de: {nombreProvinciaSeleccionada}.")
        return
    htmlCompleto = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Reporte - Provincia {nombreProvinciaSeleccionada}</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; background-color: #f4f7f6; }}
        h1 {{ color: #c0392b; text-align: center; margin-bottom: 5px; }}
        .fecha-reporte {{ text-align: center; color: #7f8c8d; font-style: italic; margin-bottom: 25px; }}
        .info {{ font-weight: bold; margin-bottom: 15px; color: #555; }}
        table {{ width: 100%; border-collapse: collapse; background-color: #ffffff; }}
        th, td {{ border: 1px solid #dbdbdb; text-align: left; padding: 12px; }}
        th {{ background-color: #c0392b; color: white; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
    </style>
</head>
<body>
    <h1>Donadores en la Provincia de {nombreProvinciaSeleccionada}</h1>
    <div class="fecha-reporte">Reporte generado el: {fechaHoraActual}</div>
    
    <div class="info">Total de registros encontrados: {contadorFilas}</div>
    <table>
        <thead>
            <tr>
                <th>Cédula</th>
                <th>Nombre Completo</th>
                <th>Tipo de Sangre</th>
                <th>Lugar de Donación</th>
                <th>Estado</th>
            </tr>
        </thead>
        <tbody>
{filasHtml}        </tbody>
    </table>
</body>
</html>
"""
    nombreArchivo = f"reporteDonadores{nombreProvinciaSeleccionada.upper().replace(' ', '')}.html"
    with open(nombreArchivo, "w", encoding="utf-8") as archivo:
        archivo.write(htmlCompleto)
    webbrowser.open(nombreArchivo)

#2
def procesarReportePorRangoEdadHtml(pdonadores, pEdadInicial, pEdadFinal):
    """
    funcion: Genera un reporte HTML con donadores cuya edad esté dentro del rango indicado.
    entradas:
    - pdonadores: matriz de donadores.
    - pEdadInicial: edad mínima del rango.
    - pEdadFinal: edad máxima del rango.
    salidas:
    - True si el reporte fue generado correctamente, False en caso contrario.
    """
    fechaHoraActual = datetime.now().strftime("%d/%m/%Y %I:%M %p")
    formatoFechaArchivo = datetime.now().strftime("%d_%m_%Y_%I_%M_%p")
    filasHtml = ""
    contadorFilas = 0

    for donador in pdonadores:
        tuplaFecha = donador[4]
        fechaNacStr = f"{tuplaFecha[0]:02d}/{tuplaFecha[1]:02d}/{tuplaFecha[2]}"
        edad = calcularEdadExacta(fechaNacStr)

        if pEdadInicial <= edad <= pEdadFinal:
            contadorFilas += 1
            cedula = donador[1]
            nombreCompleto = " ".join(donador[0])
            telefono = donador[7]
            correo = donador[6]
            filasHtml += f"""        <tr>
            <td>{cedula}</td>
            <td>{nombreCompleto}</td>
            <td>{fechaNacStr}</td>
            <td>{edad} años</td>
            <td>{telefono}</td>
            <td>{correo}</td>
        </tr>\n"""

    if contadorFilas == 0:
        messagebox.showinfo("Información",
            f"No se encontraron donadores con edad entre {pEdadInicial} y {pEdadFinal} años.")
        return False

    tituloRango = (f"Edad: {pEdadInicial} años" if pEdadInicial == pEdadFinal
                   else f"Edades entre {pEdadInicial} y {pEdadFinal} años")

    htmlCompleto = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Reporte por Rango de Edad</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; background-color: #f4f7f6; }}
        h1 {{ color: #2c3e50; text-align: center; margin-bottom: 5px; }}
        h2 {{ color: #7f8c8d; text-align: center; font-weight: normal; margin-top: 0; }}
        .fecha-reporte {{ text-align: center; color: #7f8c8d; font-style: italic; margin-bottom: 25px; }}
        .info {{ font-weight: bold; margin-bottom: 15px; color: #555; }}
        table {{ width: 100%; border-collapse: collapse; background-color: #ffffff; }}
        th, td {{ border: 1px solid #dbdbdb; text-align: left; padding: 12px; }}
        th {{ background-color: #2c3e50; color: white; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
    </style>
</head>
<body>
    <h1>Reporte por Rango de Edad</h1>
    <h2>{tituloRango}</h2>
    <div class="fecha-reporte">Reporte generado el: {fechaHoraActual}</div>
    <div class="info">Total de registros encontrados: {contadorFilas}</div>
    <table>
        <thead>
            <tr>
                <th>Cédula</th>
                <th>Nombre Completo</th>
                <th>Fecha de Nacimiento</th>
                <th>Edad</th>
                <th>Teléfono</th>
                <th>Correo</th>
            </tr>
        </thead>
        <tbody>
{filasHtml}        </tbody>
    </table>
</body>
</html>
"""
    nombreArchivo = f"reporteRangoEdad_{pEdadInicial}a{pEdadFinal}_{formatoFechaArchivo}.html"
    try:
        with open(nombreArchivo, "w", encoding="utf-8") as archivo:
            archivo.write(htmlCompleto)
        webbrowser.open(nombreArchivo)
        return True
    except Exception:
        return False

#3
def obtenerLugarDonacionCorto(cedula, pprovincias):
    """
    funcion: Obtener los lugares de donación como texto corto para usar en reportes.
    entradas:
    - cedula (str/int): cédula de la persona, se convierte a string
      automáticamente si se recibe como entero.
    - pprovincias (dict): diccionario de provincias con la estructura
      { "clave": [nombre_provincia, [lista_de_centros]] }.
    salidas:
    - lugares (str): nombres de los centros de donación separados por " / ".
      Si la cédula inicia con "8" retorna "Sede Central de Donación".
      Si la provincia no existe retorna "No encontrado."
    """
    primerDigito = str(cedula)[0]
    if primerDigito == "8":
        return "Sede Central de Donación"
    if primerDigito in pprovincias:
        return " / ".join(pprovincias[primerDigito][1])
    return "No encontrado."

def procesarReporteTipoSangreProvinciaHtml(pdonadores, pclaveProvincia, pnombreProvincia, ptipoSangre):
    """
    funcion:
    Genera un reporte HTML de donadores activos filtrados por provincia y tipo de sangre.
    entradas:
    - pdonadores: matriz con los registros de donadores.
    - pclaveProvincia: identificador de la provincia.
    - pnombreProvincia: nombre de la provincia.
    - ptipoSangre: tipo de sangre a consultar.
    salidas:
    - Archivo HTML generado y abierto en el navegador.
    """
    fechaHoraActual = datetime.now().strftime("%d/%m/%Y %I:%M %p")
    filasHtml = ""
    contadorFilas = 0
    for donador in pdonadores:
        cedula = str(donador[1])
        tipoSangreDonador = tipoSangre[donador[2]]
        estado = donador[8] 
        if estado == 1 and cedula[0] == pclaveProvincia and tipoSangreDonador == ptipoSangre:
            contadorFilas += 1
            nombreCompleto = " ".join(donador[0])
            lugarDonacion = obtenerLugarDonacionCorto(cedula, provinciasDiccionario)
            filasHtml += f"""        <tr>
            <td>{cedula}</td>
            <td>{nombreCompleto}</td>
            <td style="color: #e74c3c; font-weight: bold;">{tipoSangreDonador}</td>
            <td>{lugarDonacion}</td>
        </tr>\n"""
    if contadorFilas == 0:
        messagebox.showinfo("Información", f"No se encontraron donadores activos con tipo de sangre {ptipoSangre} en {pnombreProvincia}.")
        return
    htmlCompleto = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Reporte - Tipo de Sangre por Provincia</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; background-color: #fdfefe; }}
        h1 {{ color: #c0392b; text-align: center; margin-bottom: 5px; }}
        h2 {{ color: #2c3e50; text-align: center; margin-top: 0px; font-weight: normal; }}
        .fecha-reporte {{ text-align: center; color: #7f8c8d; font-style: italic; margin-bottom: 25px; }}
        .info {{ font-weight: bold; margin-bottom: 15px; color: #333; font-size: 1.1em; }}
        table {{ width: 100%; border-collapse: collapse; background-color: #ffffff; }}
        th, td {{ border: 1px solid #bdc3c7; text-align: left; padding: 12px; }}
        th {{ background-color: #e74c3c; color: white; }}
        tr:nth-child(even) {{ background-color: #f9ecec; }}
    </style>
</head>
<body>
    <h1>Reporte de Donadores</h1>
    <h2>Tipo de Sangre: <b>{ptipoSangre}</b> | Provincia: <b>{pnombreProvincia}</b></h2>
    <div class="fecha-reporte">Reporte generado el: {fechaHoraActual}</div>
    
    <div class="info">Total de donadores encontrados: {contadorFilas}</div>
    <table>
        <thead>
            <tr>
                <th>Cédula</th>
                <th>Nombre Completo</th>
                <th>Tipo de Sangre</th>
                <th>Lugar de Donación</th>
            </tr>
        </thead>
        <tbody>
{filasHtml}        </tbody>
    </table>
</body>
</html>
"""
    formatoFechaArchivo = datetime.now().strftime("%d_%m_%Y_%I_%M_%p")
    nombreArchivo = f"reporte{ptipoSangre.replace('+', 'pos').replace('-', 'neg')}{pnombreProvincia}{formatoFechaArchivo}.html"
    with open(nombreArchivo, "w", encoding="utf-8") as archivo:
        archivo.write(htmlCompleto)
    webbrowser.open(nombreArchivo)

# 4

def procesarReporteGeneralDonadoresHtml(pdonadores, pprovinciasDiccionario):
    """
    funcion:
    Genera un reporte HTML con todos los donadores ACTIVOS agrupados por provincia.
    entradas:
    - pdonadores: matriz con los registros de donadores.
    - pprovinciasDiccionario: diccionario de provincias.
    salidas:
    - True si el reporte fue generado correctamente.
    - False si ocurrió un error.
    """
    fechaHoraActual = datetime.now().strftime("%d/%m/%Y %I:%M %p")
    formatoFechaArchivo = datetime.now().strftime("%d_%m_%Y_%I_%M_%p")
    filasHtml = ""
    contadorTotal = 0
    for claveProvincia in sorted(pprovinciasDiccionario.keys()):
        nombreProvincia = pprovinciasDiccionario[claveProvincia][0]
        filasProvincia = ""
        contadorProvincia = 0
        for donador in pdonadores:
            cedula = str(donador[1])
            estado = donador[8]
            if estado == 1 and cedula[0] == claveProvincia:
                contadorProvincia += 1
                contadorTotal += 1
                nombreCompleto = " ".join(donador[0])
                tipoSangreStr = tipoSangre[donador[2]]
                sexo = "Masculino" if donador[3] == True else "Femenino"
                tuplaFecha = donador[4]
                fechaNac = f"{tuplaFecha[0]:02d}/{tuplaFecha[1]:02d}/{tuplaFecha[2]}"
                peso = donador[5]
                telefono = donador[7]
                correo = donador[6]
                filasProvincia += f"""        <tr>
            <td>{cedula}</td>
            <td>{nombreCompleto}</td>
            <td style="color: #e74c3c; font-weight: bold;">{tipoSangreStr}</td>
            <td>{fechaNac}</td>
            <td>{peso} kg</td>
            <td>{sexo}</td>
            <td>{telefono}</td>
            <td>{correo}</td>
        </tr>\n"""

        if contadorProvincia > 0:
            filasHtml += f"""        <tr style="background-color: #2c3e50; color: white; font-weight: bold;">
            <td colspan="8" style="text-align: center;">PROVINCIA: {nombreProvincia.upper()} ({contadorProvincia} activos)</td>
        </tr>\n"""
            filasHtml += filasProvincia

    if contadorTotal == 0:
        messagebox.showinfo("Información", "No se encontraron donadores activos registrados en ninguna provincia.")
        return False

    htmlCompleto = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Lista Completa de Donadores</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; background-color: #fdfefe; }}
        h1 {{ color: #c0392b; text-align: center; margin-bottom: 5px; }}
        h2 {{ color: #2c3e50; text-align: center; margin-top: 0px; font-weight: normal; }}
        .fecha-reporte {{ text-align: center; color: #7f8c8d; font-style: italic; margin-bottom: 25px; }}
        .info {{ font-weight: bold; margin-bottom: 15px; color: #333; font-size: 1.1em; }}
        table {{ width: 100%; border-collapse: collapse; background-color: #ffffff; }}
        th, td {{ border: 1px solid #bdc3c7; text-align: left; padding: 10px; font-size: 0.9em; }}
        th {{ background-color: #e74c3c; color: white; }}
        tr:nth-child(even) {{ background-color: #f9ecec; }}
    </style>
</head>
<body>
    <h1>Lista Completa de Donadores Activos</h1>
    <h2>Ordenados por Provincia — Día Mundial del Donante de Sangre</h2>
    <div class="fecha-reporte">Reporte generado el: {fechaHoraActual}</div>
    <div class="info">Total de donadores activos en el sistema: {contadorTotal}</div>
    <table>
        <thead>
            <tr>
                <th>Cédula</th>
                <th>Nombre Completo</th>
                <th>Tipo de Sangre</th>
                <th>Fecha de Nacimiento</th>
                <th>Peso</th>
                <th>Sexo</th>
                <th>Teléfono</th>
                <th>Correo</th>
            </tr>
        </thead>
        <tbody>
{filasHtml}        </tbody>
    </table>
</body>
</html>
"""
    nombreArchivo = f"reporteGeneral_{formatoFechaArchivo}.html"
    try:
        with open(nombreArchivo, "w", encoding="utf-8") as archivo:
            archivo.write(htmlCompleto)
        webbrowser.open(nombreArchivo)
        return True
    except Exception:
        return False
    
#5
def calcularEdadExacta(pFechaNacimientoStr):
    """
    Funcionalidad:
    Calcula la edad exacta de una persona utilizando su fecha de nacimiento.
    Entradas:
    - pFechaNacimientoStr (str): Fecha de nacimiento en formato DD/MM/AAAA.
    Salidas:
    - edad (int): Edad calculada en años.
    - 0: Si ocurre un error durante el cálculo.
    """
    try:
        fechaNacimiento = datetime.strptime(pFechaNacimientoStr, "%d/%m/%Y")
        fechaHoy = datetime.now()
        edad = fechaHoy.year - fechaNacimiento.year
        if (fechaHoy.month, fechaHoy.day) < (fechaNacimiento.month, fechaNacimiento.day):
            edad -= 1
        return edad
    except Exception:
        return 0

def procesarReporteMujeresOMinusculasHtml(pDonadores):
    """
    Funcionalidad:
    Genera un reporte HTML con las mujeres donadoras activas de tipo O- menores de 45 años, ordenadas ascendentemente por edad.
    Entradas:
    - pDonadores (list): Matriz con los registros de donadores.
    Salidas:
    - True: Si el reporte fue creado correctamente.
    - False: Si no existen registros que cumplan la condición o si ocurre un error.
    """
    fechaHoraSistema = datetime.now().strftime("%d/%m/%Y %I:%M %p")
    formatoFechaArchivo = datetime.now().strftime("%d_%m_%Y_%I_%M_%p")
    listaFiltrada = []
    for donador in pDonadores:
        if len(donador) < 9:
            continue
        tipoSangreStr = tipoSangre[donador[2]]
        estadoActivo = donador[8]  
        sexoDonador = "F" if donador[3] == False else "M"
        tuplaFecha = donador[4]
        fechaNacimientoStr = f"{tuplaFecha[0]:02d}/{tuplaFecha[1]:02d}/{tuplaFecha[2]}"
        if estadoActivo == 1 and sexoDonador == "F" and tipoSangreStr == "O-":
            edadCalculada = calcularEdadExacta(fechaNacimientoStr)
            if edadCalculada < 45:
                listaFiltrada.append({
                    "cedula": donador[1],
                    "nombreCompleto": " ".join(donador[0]),
                    "fechaNacimiento": fechaNacimientoStr,
                    "telefono": donador[7],
                    "correo": donador[6],
                    "edad": edadCalculada
                })
                
    listaFiltrada.sort(key=lambda x: x["edad"])
    filasHtml = ""
    for item in listaFiltrada:
        filasHtml += f"""        <tr>
            <td>{item['cedula']}</td>
            <td>{item['nombreCompleto']}</td>
            <td>{item['fechaNacimiento']}</td>
            <td>{item['edad']} años</td>
            <td>{item['telefono']}</td>
            <td>{item['correo']}</td>
        </tr>\n"""
        
    if len(listaFiltrada) == 0:
        messagebox.showinfo("Información", "No se encontraron mujeres donantes O- menores a 45 años en el sistema.")
        return False

    htmlCompleto = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Reporte Especial de Donantes</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; background-color: #fafafa; color: #2c3e50; }}
        h1 {{ color: #b03a2e; text-align: center; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 1px; }}
        h2 {{ color: #34495e; text-align: center; margin-top: 0px; font-weight: 300; font-size: 1.2em; }}
        .fecha-emision {{ text-align: center; color: #7f8c8d; font-style: italic; margin-bottom: 30px; }}
        .resumen {{ font-weight: bold; margin-bottom: 10px; color: #2c3e50; }}
        table {{ width: 100%; border-collapse: collapse; box-shadow: 0 2px 5px rgba(0,0,0,0.1); background-color: #ffffff; }}
        th, td {{ border: 1px solid #d2d7d9; text-align: left; padding: 12px; }}
        th {{ background-color: #b03a2e; color: white; font-weight: 600; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
        tr:hover {{ background-color: #f1f1f1; }}
    </style>
</head>
<body>
    <h1>Mujeres donantes O- menores a 45 años</h1>
    <h2>Ordenadas ascendentemente por edad</h2>
    <div class="fecha-emision">Fecha y hora del sistema: {fechaHoraSistema}</div>
    
    <div class="resumen">Registros encontrados que cumplen con el perfil: {len(listaFiltrada)}</div>
    <table>
        <thead>
            <tr>
                <th>Cédula</th>
                <th>Nombre Completo</th>
                <th>Fecha de Nacimiento</th>
                <th>Edad</th>
                <th>Teléfono</th>
                <th>Correo</th>
            </tr>
        </thead>
        <tbody>
{filasHtml}        </tbody>
    </table>
</body>
</html>
"""
    nombreArchivo = f"reporteMujeresONegativas_{formatoFechaArchivo}.html"
    try:
        with open(nombreArchivo, "w", encoding="utf-8") as archivo:
            archivo.write(htmlCompleto)
        webbrowser.open(nombreArchivo)
        return True
    except Exception:
        return False
    
# 6
def esDonadorCompatible(pTipoDonador, pTipoReceptor):
    """
    Funcionalidad:
    Determina si un tipo de sangre donador es compatible para donar a un tipo de sangre receptor.
    Entradas:
    - pTipoDonador (str): Tipo de sangre del donador.
    - pTipoReceptor (str): Tipo de sangre del receptor.
    Salidas:
    - True: Si existe compatibilidad de donación.
    - False: Si no existe compatibilidad.
    """
    if pTipoDonador == "O-":
        return True
    if pTipoDonador == "O+":
        return pTipoReceptor in ("O+", "A+", "B+", "AB+")
    if pTipoDonador == "A-":
        return pTipoReceptor in ("A+", "A-", "AB+", "AB-")
    if pTipoDonador == "A+":
        return pTipoReceptor in ("A+", "AB+")
    if pTipoDonador == "B-":
        return pTipoReceptor in ("B+", "B-", "AB+", "AB-")
    if pTipoDonador == "B+":
        return pTipoReceptor in ("B+", "AB+")
    if pTipoDonador == "AB-":
        return pTipoReceptor in ("AB+", "AB-")
    if pTipoDonador == "AB+":
        return pTipoReceptor == "AB+"  # Solo a sí mismo
    return False

def procesarReporteCompatibilidadDonacionHtml(pDonadores, pProvinciasDiccionario, pTipoDonador):
    """
    Funcionalidad:
    Genera un reporte HTML con todas las personas activas que pueden recibir
    sangre de un donador del tipo seleccionado, agrupadas por provincia.
    Entradas:
    - pDonadores (list): Matriz de donadores registrados.
    - pProvinciasDiccionario (dict): Diccionario con la información de provincias.
    - pTipoDonador (str): Tipo de sangre del donador seleccionado.
    Salidas:
    - True: Si el reporte fue generado correctamente.
    - False: Si no se encontraron registros o ocurrió un error.
    """
    #tipo del donador
    tablaReceptores = {
        "O-":  ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"],
        "O+":  ["O+", "A+", "B+", "AB+"],
        "A-":  ["A-", "A+", "AB-", "AB+"],
        "A+":  ["A+", "AB+"],
        "B-":  ["B-", "B+", "AB-", "AB+"],
        "B+":  ["B+", "AB+"],
        "AB-": ["AB-", "AB+"],
        "AB+": ["AB+"]
    }
    receptoresCompatibles = tablaReceptores.get(pTipoDonador, [])
    receptoresStr = ", ".join(receptoresCompatibles)
    fechaHoraActual = datetime.now().strftime("%d/%m/%Y %I:%M %p")
    formatoFechaArchivo = datetime.now().strftime("%d_%m_%Y_%I_%M_%p")
    filasHtml = ""
    contadorTotal = 0
    for claveProvincia in sorted(pProvinciasDiccionario.keys()):
        nombreProvincia = pProvinciasDiccionario[claveProvincia][0]
        filasProvincia = ""
        contadorProvincia = 0
        for donador in pDonadores:
            cedula = str(donador[1])
            tipoSangrePersona = tipoSangre[donador[2]]
            estado = donador[8]
            if estado == 1 and cedula[0] == claveProvincia and tipoSangrePersona in receptoresCompatibles:
                contadorProvincia += 1
                contadorTotal += 1
                nombreCompleto = " ".join(donador[0])
                telefono = donador[7]
                correo = donador[6]
                filasProvincia += f"""        <tr>
            <td>{cedula}</td>
            <td>{nombreCompleto}</td>
            <td style="color: #e74c3c; font-weight: bold;">{tipoSangrePersona}</td>
            <td>{telefono}</td>
            <td>{correo}</td>
        </tr>\n"""
        if contadorProvincia > 0:
            filasHtml += f"""        <tr style="background-color: #2c3e50; color: white; font-weight: bold;">
            <td colspan="5" style="text-align: center;">PROVINCIA: {nombreProvincia.upper()} ({contadorProvincia} personas)</td>
        </tr>\n"""
            filasHtml += filasProvincia
    if contadorTotal == 0:
        messagebox.showinfo("Información",
            f"No se encontraron personas activas que puedan recibir sangre tipo {pTipoDonador}.")
        return False

    htmlCompleto = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Reporte - ¿A quién puede donar?</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; background-color: #fdfefe; }}
        h1 {{ color: #c0392b; text-align: center; margin-bottom: 5px; }}
        h2 {{ color: #2c3e50; text-align: center; margin-top: 0px; font-weight: normal; }}
        .receptores {{ text-align: center; background-color: #eaf4fb; border: 1px solid #aed6f1;
                       border-radius: 6px; padding: 10px; margin-bottom: 20px; 
                       color: #1a5276; font-weight: bold; }}
        .fecha-reporte {{ text-align: center; color: #7f8c8d; font-style: italic; margin-bottom: 15px; }}
        .info {{ font-weight: bold; margin-bottom: 15px; color: #333; font-size: 1.1em; }}
        table {{ width: 100%; border-collapse: collapse; background-color: #ffffff; }}
        th, td {{ border: 1px solid #bdc3c7; text-align: left; padding: 12px; }}
        th {{ background-color: #e74c3c; color: white; }}
        tr:nth-child(even) {{ background-color: #f9ecec; }}
    </style>
</head>
<body>
    <h1>¿A quién puede donar?</h1>
    <h2>Personas que pueden recibir sangre de un donador tipo: <b>{pTipoDonador}</b></h2>
    <div class="receptores">Un donador {pTipoDonador} puede abastecer a los tipos: {receptoresStr}</div>
    <div class="fecha-reporte">Reporte generado el: {fechaHoraActual}</div>
    <div class="info">Total de personas encontradas a nivel nacional: {contadorTotal}</div>
    <table>
        <thead>
            <tr>
                <th>Cédula</th>
                <th>Nombre Completo</th>
                <th>Tipo de Sangre</th>
                <th>Teléfono</th>
                <th>Correo</th>
            </tr>
        </thead>
        <tbody>
{filasHtml}        </tbody>
    </table>
</body>
</html>
"""
    sangreLimpia = pTipoDonador.replace('+', 'pos').replace('-', 'neg')
    nombreArchivo = f"reporteQuienPuedeDonar_{sangreLimpia}_{formatoFechaArchivo}.html"
    try:
        with open(nombreArchivo, "w", encoding="utf-8") as archivo:
            archivo.write(htmlCompleto)
        webbrowser.open(nombreArchivo)
        return True
    except Exception:
        return False

    
#7

def procesarReporteCompatibilidadHtml(pDonadores, pTipoSangreObjetivo):
    """
    Funcionalidad:
    Genera un reporte HTML con los donadores activos compatibles para un receptor de un tipo de sangre determinado.
    Entradas:
    - pDonadores (list): Matriz de donadores registrados.
    - pTipoSangreObjetivo (str): Tipo de sangre del receptor.
    Salidas:
    - True: Si el reporte se genera correctamente.
    - False: Si no existen donadores compatibles o ocurre un error.
    """
    tablaCompatibilidad = {
        "O-":  ["O-"],
        "O+":  ["O+", "O-"],
        "A-":  ["A-", "O-"],
        "A+":  ["A+", "A-", "O+", "O-"],
        "B-":  ["B-", "O-"],
        "B+":  ["B+", "B-", "O+", "O-"],
        "AB-": ["AB-", "A-", "B-", "O-"],
        "AB+": ["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"]
    }
    tiposCompatibles = tablaCompatibilidad.get(pTipoSangreObjetivo, [])
    fechaHoraSistema = datetime.now().strftime("%d/%m/%Y %I:%M %p")
    formatoFechaArchivo = datetime.now().strftime("%d_%m_%Y_%I_%M_%p")
    listaCompatibles = []
    for donador in pDonadores:
        if len(donador) < 8:
            continue  
        tipoSangreDonador = tipoSangre[donador[2]]
        estadoActivo = donador[8] 
        cedulaStr = str(donador[1])
        if estadoActivo == 1 and (tipoSangreDonador in tiposCompatibles):
            codigoProvincia = cedulaStr[0]
            listaCompatibles.append({
                "cedula": donador[1],
                "nombreCompleto": " ".join(donador[0]),
                "tipoSangre": tipoSangreDonador,
                "telefono": donador[7],
                "correo": donador[6],
                "provinciaId": codigoProvincia
            })
            
    if len(listaCompatibles) == 0:
        messagebox.showinfo("Información", f"No se encontraron donadores activos compatibles para abastecer el tipo {pTipoSangreObjetivo}.")
        return False
        
    listaCompatibles.sort(key=lambda x: x["provinciaId"], reverse=True)
    provinciasNombres = {
        "1": "San José", "2": "Alajuela", "3": "Cartago", "4": "Heredia",
        "5": "Guanacaste", "6": "Puntarenas", "7": "Limón", "8": "Naturalizado"
    }
    filasHtml = ""
    for item in listaCompatibles:
        nombreProvincia = provinciasNombres.get(item["provinciaId"], f"Provincia ({item['provinciaId']})")
        filasHtml += f"""        <tr>
            <td>{nombreProvincia}</td>
            <td>{item['cedula']}</td>
            <td>{item['nombreCompleto']}</td>
            <td>{item['tipoSangre']}</td>
            <td>{item['telefono']}</td>
            <td>{item['correo']}</td>
        </tr>\n"""
    htmlCompleto = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Reporte de Compatibilidad de Receptores</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; background-color: #fcfcfc; color: #2c3e50; }}
        h1 {{ color: #16a085; text-align: center; margin-bottom: 5px; text-transform: uppercase; font-size: 1.8em; }}
        h2 {{ color: #7f8c8d; text-align: center; margin-top: 0px; font-weight: 400; font-size: 1.1em; margin-bottom: 25px; }}
        .meta-info {{ text-align: center; color: #95a5a6; font-style: italic; margin-bottom: 30px; }}
        table {{ width: 100%; border-collapse: collapse; background-color: #ffffff; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        th, td {{ border: 1px solid #e2e8f0; text-align: left; padding: 12px; }}
        th {{ background-color: #16a085; color: white; font-weight: 600; }}
        tr:nth-child(even) {{ background-color: #f8fafc; }}
        tr:hover {{ background-color: #f1f5f9; }}
        .badge-sangre {{ background-color: #e74c3c; color: white; padding: 3px 8px; border-radius: 4px; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>Reporte de Donadores Compatibles</h1>
    <h2>Donadores aptos para un receptor con tipo de sangre: <span class="badge-sangre">{pTipoSangreObjetivo}</span></h2>
    <div class="meta-info">Fecha y hora del sistema: {fechaHoraSistema}</div>
    
    <table>
        <thead>
            <tr>
                <th>Provincia</th>
                <th>Cédula</th>
                <th>Nombre Completo</th>
                <th>Tipo de Sangre</th>
                <th>Teléfono</th>
                <th>Correo</th>
            </tr>
        </thead>
        <tbody>
{filasHtml}        </tbody>
    </table>
</body>
</html>
"""
    nombreArchivo = f"reporteCompatibilidad{pTipoSangreObjetivo}_{formatoFechaArchivo}.html"
    try:
        with open(nombreArchivo, "w", encoding="utf-8") as archivo:
            archivo.write(htmlCompleto)
        webbrowser.open(nombreArchivo)
        return True
    except Exception:
        return False

#8
def procesarReporteInactivos(pmatrizDonadores):
    """
    Funcionalidad:
    Genera un reporte HTML con los donadores inactivos y la justificación de su exclusión.
    Entradas:
    - pmatrizDonadores (list): Matriz de donadores registrados.
    Salidas:
    - True: Si el reporte se genera correctamente.
    - False: Si ocurre un error o no existen donadores inactivos.
    """
    fechaHoraActual = datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")
    nombreArchivo = "reporteDonadoresInactivos.html"
    causasRechazo = {
        1: "Enfermedades Infecciosas/Crónicas",
        2: "Conductas de Riesgo",
        3: "Factores de Salud Física",
        4: "Procedimientos Médicos",
        5: "Uso de Medicamentos",
        6: "Estilo de Vida y Viajes",
        7: "Situaciones Específicas"
    }

    try:
        with open(nombreArchivo, "w", encoding="utf-8") as archivoHtml:
            archivoHtml.write("<!DOCTYPE html>\n<html lang='es'>\n<head>\n")
            archivoHtml.write("    <meta charset='UTF-8'>\n")
            archivoHtml.write("    <title>Reporte de Donadores Excluidos</title>\n")
            archivoHtml.write("    <style>\n")
            archivoHtml.write("        body { font-family: Arial, sans-serif; margin: 30px; background-color: #f9f9f9; }\n")
            archivoHtml.write("        h1 { color: #b30000; text-align: center; }\n")
            archivoHtml.write("        .info-sistema { text-align: center; margin-bottom: 20px; color: #555; }\n")
            archivoHtml.write("        table { width: 100%; border-collapse: collapse; margin-top: 10px; background-color: #fff; }\n")
            archivoHtml.write("        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; font-size: 13px; }\n")
            archivoHtml.write("        th { background-color: #b30000; color: white; }\n")
            archivoHtml.write("        tr:nth-child(even) { background-color: #f2f2f2; }\n")
            archivoHtml.write("    </style>\n</head>\n<body>\n")
            archivoHtml.write("    <h1>Reporte de Donadores No Activos (Excluidos)</h1>\n")
            archivoHtml.write(f"    <div class='info-sistema'><strong>Fecha y Hora del Sistema:</strong> {fechaHoraActual}</div>\n")
            archivoHtml.write("    <table>\n        <thead>\n            <tr>\n")
            archivoHtml.write("                <th>Cédula</th>\n                <th>Nombre Completo</th>\n")
            archivoHtml.write("                <th>Tipo Sangre</th>\n                <th>Fecha Nacimiento</th>\n")
            archivoHtml.write("                <th>Peso</th>\n                <th>Sexo</th>\n")
            archivoHtml.write("                <th>Teléfono</th>\n                <th>Correo</th>\n")
            archivoHtml.write("                <th>Justificación de Exclusión</th>\n")
            archivoHtml.write("            </tr>\n        </thead>\n        <tbody>\n")
            hayInactivos = False
            for donador in pmatrizDonadores:
                estado = donador[8]
                if estado != 0:
                    continue
                hayInactivos = True
                cedula = donador[1]
                nombreCompleto = " ".join(donador[0])
                tipoSangreStr = tipoSangre[donador[2]]
                sexo = "F" if donador[3] == False else "M"
                tuplaFecha = donador[4]
                fechaNacimiento = f"{tuplaFecha[0]:02d}/{tuplaFecha[1]:02d}/{tuplaFecha[2]}"
                peso = donador[5]
                correo = donador[6]
                telefono = donador[7]
                if len(donador) > 9:
                    codigoJustificacion = donador[9]
                    justificacion = causasRechazo.get(codigoJustificacion, f"Causa desconocida (código {codigoJustificacion})")
                else:
                    justificacion = "Sin justificación registrada"
                archivoHtml.write("            <tr>\n")
                archivoHtml.write(f"                <td>{cedula}</td>\n")
                archivoHtml.write(f"                <td>{nombreCompleto}</td>\n")
                archivoHtml.write(f"                <td>{tipoSangreStr}</td>\n")
                archivoHtml.write(f"                <td>{fechaNacimiento}</td>\n")
                archivoHtml.write(f"                <td>{peso} kg</td>\n")
                archivoHtml.write(f"                <td>{sexo}</td>\n")
                archivoHtml.write(f"                <td>{telefono}</td>\n")
                archivoHtml.write(f"                <td>{correo}</td>\n")
                archivoHtml.write(f"                <td><strong>{justificacion}</strong></td>\n")
                archivoHtml.write("            </tr>\n")
            archivoHtml.write("        </tbody>\n    </table>\n</body>\n</html>")
        if not hayInactivos:
            messagebox.showinfo("Información", "No hay donadores inactivos registrados en el sistema.")
            return False
        webbrowser.open(nombreArchivo)
        return True
    except Exception as e:
        print(f"Error al generar reporte: {e}")
        return False


# 9

def procesarReporteLugaresDonacionHtml(pDonadores, pProvinciasDiccionario):
    """
    funcion: Genera un reporte HTML con los lugares de donación por provincia,
    ordenados ascendentemente según el Registro Civil del TSE, mostrando
    la cantidad de donadores registrados (activos e inactivos) y los
    recintos posibles de recaudación.
    entradas:
    - pDonadores (list): matriz con los registros de donadores.
    - pProvinciasDiccionario (dict): diccionario de provincias con la estructura
      { "clave": [nombre_provincia, [lista_de_centros]] }.
    salidas:
    - True: si el reporte fue generado correctamente.
    - False: si ocurre un error al escribir el archivo.
    """
    fechaHoraActual = datetime.now().strftime("%d/%m/%Y %I:%M %p")
    formatoFechaArchivo = datetime.now().strftime("%d_%m_%Y_%I_%M_%p")
    filasHtml = ""

    for clave in sorted(pProvinciasDiccionario.keys()):
        nombreProvincia = pProvinciasDiccionario[clave][0]
        recintos = pProvinciasDiccionario[clave][1]
        cantidadDonadores = sum(1 for donador in pDonadores if str(donador[1])[0] == clave)
        recintosHtml = "".join(f"<li>{recinto}</li>" for recinto in recintos)
        filasHtml += f"""        <tr>
            <td>{nombreProvincia}</td>
            <td style="text-align: center;">{cantidadDonadores}</td>
            <td><ul style="margin: 0; padding-left: 18px;">{recintosHtml}</ul></td>
        </tr>\n"""

    htmlCompleto = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Reporte - Lugares de Donación</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; background-color: #f9f9f9; }}
        h1 {{ color: #c0392b; text-align: center; margin-bottom: 5px; }}
        h2 {{ color: #2c3e50; text-align: center; font-weight: normal; margin-top: 0; }}
        .fecha-reporte {{ text-align: center; color: #7f8c8d; font-style: italic; margin-bottom: 25px; }}
        table {{ width: 100%; border-collapse: collapse; background-color: #ffffff; }}
        th, td {{ border: 1px solid #bdc3c7; text-align: left; padding: 12px; vertical-align: top; }}
        th {{ background-color: #c0392b; color: white; }}
        tr:nth-child(even) {{ background-color: #f9ecec; }}
        ul {{ list-style-type: disc; }}
    </style>
</head>
<body>
    <h1>Lugares de Donación por Provincia</h1>
    <h2>Ordenados según el Registro Civil del Tribunal Supremo de Elecciones</h2>
    <div class="fecha-reporte">Reporte generado el: {fechaHoraActual}</div>
    <table>
        <thead>
            <tr>
                <th>Provincia</th>
                <th style="text-align: center;">Donadores Registrados</th>
                <th>Recintos de Recaudación</th>
            </tr>
        </thead>
        <tbody>
{filasHtml}        </tbody>
    </table>
</body>
</html>
"""
    nombreArchivo = f"reporteLugaresDonacion_{formatoFechaArchivo}.html"
    try:
        with open(nombreArchivo, "w", encoding="utf-8") as archivo:
            archivo.write(htmlCompleto)
        webbrowser.open(nombreArchivo)
        return True
    except Exception:
        return False

