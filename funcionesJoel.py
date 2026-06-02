#
#
#
#

import re
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk
import pickle
import webbrowser

archivoDonadores = "donadores.dat"

tipoSangre = ("O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-")

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

# Pickle
def cargarDatosDesdeArchivo():
    try:
        with open(archivoDonadores, "rb") as archivo:
            return pickle.load(archivo, encoding="utf-8")
    except FileNotFoundError:
        return []
    except (pickle.PickleError, EOFError):
        return []

def guardarMatrizEnArchivo(matrizGuardar):
    with open(archivoDonadores, "wb") as archivo:
        pickle.dump(matrizGuardar, archivo)
    return
# procesar

def buscarDonador(cedulaTarget, matrizABuscar):
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
    hoy = datetime.now()
    fechaNac = datetime.strptime(fechaNacimientoStr, "%d/%m/%Y")
    return hoy.year - fechaNac.year - ((hoy.month, hoy.day) < (fechaNac.month, fechaNac.day))

def obtenerMensajeEdad(fechaNacimientoStr):
    if calcularEdad(fechaNacimientoStr) >= 18:
        return "Dado su fecha de nacimiento usted ya puede ser donador."
    return "Dado su fecha de nacimiento usted aún no puede ser donador."

def obtenerLugarDonacion(cedula, pprovincias):
    primerDigito = cedula[0]
    if primerDigito == "8":
        return "Casos especiales de las cédulas que donen en San José. Centro asignado Sede Central de Donación."
    if primerDigito in pprovincias:
        provincia = pprovincias[primerDigito][0]
        hospitales = " o ".join(pprovincias[primerDigito][1])
        return f"Dado que usted nació en la provincia de {provincia}, usted podría donar en {hospitales}."
    return "Provincia no encontrada."

def obtenerMensajePeso(pesoStr):
    peso = float(pesoStr)
    if peso <= 50:
        return "Usted debe pesar más de 50 kgms para poder ser donador."
    if 50 < peso <= 110:
        return "Usted posee un peso adecuado, correcto para ser donador de sangre."
    return "Dado su sobre peso, no es posible donar sangre."

def obtenerInformacionResaltadaSangre(tipoSangreStr):
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
    
# Validaciones

def validarCedula(cedula):
    patron = r"^[1-9]-\d{3,5}-\d{3,4}$"
    return bool(re.match(patron, cedula))

def validarFechaNacimiento(fechaStr):
    try:
        datetime.strptime(fechaStr, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def validarCorreo(correo):
    patron = r"^[a-zA-Z0-9._%+-]+@(costarricense\.cr|racsa\.go\.cr|ccss\.sa\.cr|gmail\.com)$"
    return bool(re.match(patron, correo))

def validarTelefono(telefono):
    patron = r"^[246789]\d{3}-\d{4}$"
    return bool(re.match(patron, telefono))

def validarPeso(pesoStr):
    try:
        peso = float(pesoStr)
        return 50.0 < peso < 120.0
    except ValueError:
        return False

# aux
def insertarDonadorAux(matrizDonadores, pprovincias):
    def registrar():
        cedula = entradaCedula.get().strip()
        nombreCompletoStr = entradaNombreCompleto.get().strip()
        fechaNac = entradaFecha.get().strip()
        tipoSangreString = comboSangre.get()
        sexoBool = True if varSexo.get() == 1 else False
        pesoStr = entradaPeso.get().strip()
        telefono = entradaTelefono.get().strip()
        correoStr = entradaCorreo.get().strip()
        if not nombreCompletoStr:
            messagebox.showwarning("Aviso", "El nombre completo es requerido.")
            return
        partesNombre = nombreCompletoStr.split()
        if len(partesNombre) < 3:
            messagebox.showwarning("Aviso", "Por favor ingrese Nombre, Primer Apellido y Segundo Apellido separados por espacios.")
            return
        if not validarCedula(cedula):
            messagebox.showwarning("Aviso", "Formato de cédula incorrecto.\nDebe ser #-####-####.")
            return
        if not validarFechaNacimiento(fechaNac):
            messagebox.showwarning("Aviso", "Fecha de nacimiento inválida (DD/MM/AAAA).")
            return
        if not validarPeso(pesoStr):
            messagebox.showwarning("Aviso", "El peso debe ser un número mayor a 50 y menor a 120.")
            return
        if not validarTelefono(telefono):
            messagebox.showwarning("Aviso", "Formato de teléfono incorrecto.")
            return
        if not validarCorreo(correoStr):
            messagebox.showwarning("Aviso", "Correo no permitido.")
            return
        existe, posicion = buscarDonador(cedula, matrizDonadores)
        if existe:
            messagebox.showwarning("Aviso", f"La cédula {cedula} ya se encuentra registrada.")
            return
        apellido2 = partesNombre[-1]
        apellido1 = partesNombre[-2]
        nombre = " ".join(partesNombre[:-2])
        listaNombreEstructurada = [nombre, apellido1, apellido2]
        cedulaInt = int(cedula.replace("-", ""))
        tipoSangreInt = tipoSangre.index(tipoSangreString)
        dia, mes, anno = map(int, fechaNac.split("/"))
        tuplaFecha = (dia, mes, anno)
        pesoFloat = float(pesoStr)
        estadoInicial = 1
        nuevoRegistro = [
            listaNombreEstructurada,     
            cedulaInt,       
            tipoSangreInt,   
            sexoBool,        
            tuplaFecha,      
            pesoFloat,       
            correoStr,          
            telefono,        
            estadoInicial    
        ]
        matrizDonadores.insert(posicion, nuevoRegistro)
        guardarMatrizEnArchivo(matrizDonadores)
        msgEdad = obtenerMensajeEdad(fechaNac)
        msgLugar = obtenerLugarDonacion(cedula, pprovincias)
        msgPeso = obtenerMensajePeso(pesoStr)
        msgSangre = obtenerInformacionResaltadaSangre(tipoSangreString)
        resultadoFluido = f"{msgEdad}\n\n{msgLugar}\n\n{msgPeso}\n\n{msgSangre}"
        messagebox.showinfo("Información de la inserción inicial", resultadoFluido)
        limpiar()

    def limpiar():
        entradaCedula.delete(0, tk.END)
        entradaNombreCompleto.delete(0, tk.END)
        entradaFecha.delete(0, tk.END)
        comboSangre.set("O+")
        varSexo.set(1)
        entradaPeso.delete(0, tk.END)
        entradaTelefono.delete(0, tk.END)
        entradaCorreo.delete(0, tk.END)
    ventana = tk.Toplevel()
    ventana.title("Insertar donador")
    ventana.geometry("550x360")
    tk.Label(ventana, text="Cédula").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    entradaCedula = tk.Entry(ventana, width=25)
    entradaCedula.grid(row=0, column=1, padx=10, pady=5)
    tk.Label(ventana, text="Nombre Completo").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    entradaNombreCompleto = tk.Entry(ventana, width=40)
    entradaNombreCompleto.grid(row=1, column=1, columnspan=2, sticky="w", padx=10, pady=5)
    tk.Label(ventana, text="Fecha de nacimiento").grid(row=2, column=0, sticky="w", padx=10, pady=5)
    entradaFecha = tk.Entry(ventana, width=25)
    entradaFecha.grid(row=2, column=1, padx=10, pady=5)
    tk.Label(ventana, text="Tipo de sangre").grid(row=3, column=0, sticky="w", padx=10, pady=5)
    comboSangre = ttk.Combobox(ventana, values=tipoSangre, state="readonly", width=10)
    comboSangre.set("O+")
    comboSangre.grid(row=3, column=1, sticky="w", padx=10, pady=5)
    tk.Label(ventana, text="Sexo").grid(row=4, column=0, sticky="w", padx=10, pady=5)
    varSexo = tk.IntVar(value=1)
    tk.Radiobutton(ventana, text="Masculino", variable=varSexo, value=1).grid(row=4, column=1, sticky="w", padx=10)
    tk.Radiobutton(ventana, text="Femenino", variable=varSexo, value=2).grid(row=4, column=1, sticky="w", padx=110)
    tk.Label(ventana, text="Peso (kg)").grid(row=5, column=0, sticky="w", padx=10, pady=5)
    entradaPeso = tk.Entry(ventana, width=25)
    entradaPeso.grid(row=5, column=1, padx=10, pady=5)
    tk.Label(ventana, text="Teléfono").grid(row=6, column=0, sticky="w", padx=10, pady=5)
    entradaTelefono = tk.Entry(ventana, width=25)
    entradaTelefono.grid(row=6, column=1, padx=10, pady=5)
    tk.Label(ventana, text="Correo").grid(row=7, column=0, sticky="w", padx=10, pady=5)
    entradaCorreo = tk.Entry(ventana, width=35)
    entradaCorreo.grid(row=7, column=1, sticky="w", padx=10, pady=5)
    marcoBotones = tk.Frame(ventana)
    marcoBotones.grid(row=8, column=0, columnspan=2, pady=15)
    tk.Button(marcoBotones, text="Registrar", command=registrar, width=10).pack(side="left", padx=5)
    tk.Button(marcoBotones, text="Limpiar", command=limpiar, width=10).pack(side="left", padx=5)
    tk.Button(marcoBotones, text="Regresar", command=lambda: ventana.destroy(), width=10).pack(side="left", padx=5)

# eliminar donador

def eliminarDonadorAux(matrizDonadores):
    def ProcesarInactivacion():
        cedula = entradaCedula.get().strip()
        justificacionTexto = comboJustificacion.get()
        if not validarCedula(cedula):
            messagebox.showwarning("Aviso", "Formato de cédula incorrecto.")
            return
        if not justificacionTexto:
            messagebox.showwarning("Aviso", "Debe seleccionar una justificación.")
            return
        existe, posicion = buscarDonador(cedula, matrizDonadores)
        if not existe:
            messagebox.showwarning("Aviso", f"La cédula {cedula} no está registrada.")
            return
        if matrizDonadores[posicion][8] == 0:
            messagebox.showinfo("Información", "Esta persona ya se encuentra registrada como Inactiva.")
            return
        confirmacion = messagebox.askyesno("Confirmar acción", "¿Está seguro de que desea inactivar al donador?")
        if confirmacion:
            justificacionInt = causasRechazo.index(justificacionTexto) + 1
            matrizDonadores[posicion][8] = 0
            if len(matrizDonadores[posicion]) == 9:
                matrizDonadores[posicion].append(justificacionInt)
            else:
                matrizDonadores[posicion][9] = justificacionInt
            guardarMatrizEnArchivo(matrizDonadores)
            messagebox.showinfo("Información", "Donador inactivado satisfactoriamente.")
            ventana.destroy()
        else:
            messagebox.showinfo("Información", "Donador NO inactivado.")
    ventana = tk.Toplevel()
    ventana.title("Eliminar donador")
    ventana.geometry("520x200")
    tk.Label(ventana, text="Cédula a buscar:").grid(row=0, column=0, sticky="w", padx=15, pady=15)
    entradaCedula = tk.Entry(ventana, width=20)
    entradaCedula.grid(row=0, column=1, sticky="w", padx=15, pady=15)
    tk.Label(ventana, text="Justificación del rechazo:").grid(row=1, column=0, sticky="w", padx=15, pady=10)
    causasRechazo = [
        "Enfermedades Infecciosas/Crónicas", 
        "Conductas de Riesgo",               
        "Factores de Salud Física",          
        "Procedimientos Médicos",            
        "Uso de Medicamentos",               
        "Estilo de Vida y Viajes",           
        "Situaciones Específicas"            
    ]
    comboJustificacion = ttk.Combobox(ventana, values=causasRechazo, state="readonly", width=35)
    comboJustificacion.grid(row=1, column=1, sticky="w", padx=15, pady=10)
    marcoBotones = tk.Frame(ventana)
    marcoBotones.grid(row=2, column=0, columnspan=2, pady=15)
    tk.Button(marcoBotones, text="Inactivar", command=ProcesarInactivacion, width=10).pack(side="left", padx=5)
    tk.Button(marcoBotones, text="Limpiar", command=lambda: [entradaCedula.delete(0, tk.END), comboJustificacion.set("")], width=10).pack(side="left", padx=5)
    tk.Button(marcoBotones, text="Regresar", command=lambda: ventana.destroy(), width=10).pack(side="left", padx=5)


# ingresar lugar de donacion

def insertarLugarDonacionAux():
    ventanaLugares = tk.Toplevel()
    ventanaLugares.title("Insertar lugar de donación")
    ventanaLugares.geometry("350x250")
    tk.Label(ventanaLugares, text="Seleccione la Provincia:").pack(pady=(10, 0))
    opcionesProvincias = [f"{clave} - {datos[0]}" for clave, datos in provinciasDiccionario.items()]
    comboProvincia = ttk.Combobox(ventanaLugares, values=opcionesProvincias, state="readonly", width=30)
    comboProvincia.pack(pady=5)
    tk.Label(ventanaLugares, text="Nuevo lugar de donación:").pack(pady=(10, 0))
    entradaLugar = tk.Entry(ventanaLugares, width=35)
    entradaLugar.pack(pady=5)
    
    def insertarLugar():
        seleccion = comboProvincia.get()
        nuevoLugar = entradaLugar.get().strip()
        if not seleccion:
            messagebox.showwarning("Aviso", "Debe seleccionar una provincia.")
            return
        if not nuevoLugar:
            messagebox.showwarning("Aviso", "Debe ingresar el nombre del nuevo lugar.")
            return
        claveProvincia = seleccion.split(" - ")[0]
        lugaresActuales = provinciasDiccionario[claveProvincia][1]
        lugaresMinuscula = [lugar.lower() for lugar in lugaresActuales]
        if nuevoLugar.lower() in lugaresMinuscula:
            messagebox.showerror("Error", "Este lugar ya está registrado en la provincia seleccionada.")
        else:
            provinciasDiccionario[claveProvincia][1].append(nuevoLugar)
            messagebox.showinfo("Éxito", f"Lugar '{nuevoLugar}' agregado correctamente.")
            entradaLugar.delete(0, tk.END)
    marcoBotones = tk.Frame(ventanaLugares)
    marcoBotones.pack(pady=20)
    tk.Button(marcoBotones, text="Insertar", command=insertarLugar, width=10).pack(side=tk.LEFT, padx=10)
    tk.Button(marcoBotones, text="Salir", command=lambda: ventanaLugares.destroy(), width=10).pack(side=tk.RIGHT, padx=10)


donadores = cargarDatosDesdeArchivo()

def menuPrincipal():
    root = tk.Tk()
    root.title("Sistema Banco de Sangre")
    root.geometry("400x350")
    root.resizable(False, False)
    tk.Label(
        root,
        text="Sistema Banco de Sangre",
        font=("Arial", 14, "bold")
    ).pack(pady=20)
    tk.Button(
        root,
        text="Insertar Donador",
        width=25,
        command=lambda: insertarDonadorAux(donadores, provinciasDiccionario)
    ).pack(pady=5)
    tk.Button(
        root,
        text="Eliminar Donador",
        width=25,
        command=lambda: eliminarDonadorAux(donadores)
    ).pack(pady=5)
    tk.Button(
        root,
        text="Insertar Lugar de Donación",
        width=25,
        command=insertarLugarDonacionAux
    ).pack(pady=5)
    tk.Button(
        root,
        text="Reportes",
        width=25,
        command=lambda: submenuReportes(root)
    ).pack(pady=5)

    tk.Button(
        root,
        text="Salir",
        width=25,
        command=root.destroy
    ).pack(pady=20)

    root.mainloop()


# reportes

# reporte1

def validarSeleccionProvincia(provinciaSeleccionada):
    if not provinciaSeleccionada:
        messagebox.showwarning("Validación", "Debe seleccionar una provincia de la lista.")
        return False
    return True

def procesarReportePorProvinciaHtml(idProvinciaSeleccionada, pdonadores, pprovincias):
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
            lugarDonacion = donador[6]
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

def reportePorProvinciaAux(pdonadores):
    if not pdonadores:
        messagebox.showwarning("Aviso", "No hay donadores registrados en el sistema.")
        return
    ventanaFiltro = tk.Toplevel()
    ventanaFiltro.title("Filtrar por Provincia")
    ventanaFiltro.geometry("350x180")
    ventanaFiltro.resizable(False, False)
    tk.Label(ventanaFiltro, text="Seleccione la provincia a consultar:").pack(pady=15)
    opcionesProvincias = [f"{clave} - {datos[0]}" for clave, datos in provinciasDiccionario.items()]
    comboProvincia = ttk.Combobox(ventanaFiltro, values=opcionesProvincias, state="readonly", width=25)
    comboProvincia.pack(pady=5)

    def ejecutarReporte():
        seleccion = comboProvincia.get()
        if validarSeleccionProvincia(seleccion):
            idProvincia = seleccion.split(" - ")[0]
            procesarReportePorProvinciaHtml(idProvincia, pdonadores, provinciasDiccionario)
            ventanaFiltro.destroy()
    tk.Button(ventanaFiltro, text="Generar Reporte", command=ejecutarReporte, bg="#c0392b", fg="white").pack(pady=15)

# reporte 2

def validarSeleccionSangre(tipoSangre):
    if not tipoSangre:
        messagebox.showwarning("Validación", "Debe seleccionar un tipo de sangre de la lista.")
        return False
    return True

def procesarReportePorSangreHtml(tipoSangreSeleccionado, pdonadores, pprovincias):
    fechaHoraActual = datetime.now().strftime("%d/%m/%Y %I:%M %p")
    filasHtml = ""
    contadorFilas = 0
    for donador in pdonadores:
        tipoSangreDonador = tipoSangre[donador[2]]
        if tipoSangreDonador == tipoSangreSeleccionado:
            contadorFilas += 1
            cedula = donador[1]
            nombreCompleto = " ".join(donador[0])
            idProvincia = str(donador[1])[0]
            lugarDonacion = donador[6]
            estado = "Activo" if donador[8] == 1 else "Inactivo"
            nombreProvincia = pprovincias.get(idProvincia, ["Desconocida"])[0]
            filasHtml += f"""        <tr>
            <td>{cedula}</td>
            <td>{nombreCompleto}</td>
            <td>{nombreProvincia}</td>
            <td>{lugarDonacion}</td>
            <td>{estado}</td>
        </tr>\n"""
    if contadorFilas == 0:
        messagebox.showinfo("Información", f"No se encontraron donadores con tipo de sangre {tipoSangreSeleccionado}.")
        return

    htmlCompleto = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Reporte - Tipo {tipoSangreSeleccionado}</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; background-color: #f4f7f6; }}
        h1 {{ color: #2c3e50; text-align: center; margin-bottom: 5px; }}
        .fecha-reporte {{ text-align: center; color: #7f8c8d; font-style: italic; margin-bottom: 25px; }}
        .info {{ font-weight: bold; margin-bottom: 15px; color: #555; }}
        table {{ width: 100%; border-collapse: collapse; background-color: #ffffff; }}
        th, td {{ border: 1px solid #dbdbdb; text-align: left; padding: 12px; }}
        th {{ background-color: #2c3e50; color: white; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
    </style>
</head>
<body>
    <h1>Donadores con Tipo de Sangre: {tipoSangreSeleccionado}</h1>
    <div class="fecha-reporte">Reporte generado el: {fechaHoraActual}</div>
    
    <div class="info">Total de registros encontrados: {contadorFilas}</div>
    <table>
        <thead>
            <tr>
                <th>Cédula</th>
                <th>Nombre Completo</th>
                <th>Provincia</th>
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
    nombreArchivo = f"reporte_donadores_{tipoSangreSeleccionado}.html"
    with open(nombreArchivo, "w", encoding="utf-8") as archivo:
        archivo.write(htmlCompleto)
    webbrowser.open(nombreArchivo)

def reportePorSangreAux(pdonadores):
    if not pdonadores:
        messagebox.showwarning("Aviso", "No hay donadores registrados en el sistema.")
        return
    ventanaFiltro = tk.Toplevel()
    ventanaFiltro.title("Filtrar por Sangre")
    ventanaFiltro.geometry("300x180")
    ventanaFiltro.resizable(False, False)
    tk.Label(ventanaFiltro, text="Seleccione el tipo de sangre:").pack(pady=15)
    opcionesSangre = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    comboSangre = ttk.Combobox(ventanaFiltro, values=opcionesSangre, state="readonly", width=15)
    comboSangre.pack(pady=5)

    def ejecutarReporte():
        seleccion = comboSangre.get()
        if validarSeleccionSangre(seleccion):
            procesarReportePorSangreHtml(seleccion, pdonadores, provinciasDiccionario)
            ventanaFiltro.destroy()
    tk.Button(ventanaFiltro, text="Generar Reporte", command=ejecutarReporte, bg="#5cb85c", fg="white").pack(pady=15)

# reporte 3
def validarFiltrosTipoSangreProvincia(pseleccionProvincia, pseleccionSangre):
    if not pseleccionProvincia or not pseleccionSangre:
        messagebox.showwarning("Aviso", "Debe seleccionar una provincia y un tipo de sangre para generar el reporte.")
        return False
    return True

def procesarReporteTipoSangreProvinciaHtml(pdonadores, pclaveProvincia, pnombreProvincia, ptipoSangre):
    fechaHoraActual = datetime.now().strftime("%d/%m/%Y %I:%M %p")
    filasHtml = ""
    contadorFilas = 0
    for donador in pdonadores:
        cedula = str(donador[1])
        tipoSangreDonador = tipoSangre[donador[2]]
        estado = donador[8] # 1 es Activo
        if estado == 1 and cedula[0] == pclaveProvincia and tipoSangreDonador == ptipoSangre:
            contadorFilas += 1
            nombreCompleto = " ".join(donador[0])
            lugarDonacion = donador[6]
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

def reporteTipoSangreProvinciaAux(pcomboProvincia, pcomboSangre, pdonadores, pprovinciasDiccionario):
    """
    """
    seleccionProvincia = pcomboProvincia.get().strip()
    seleccionSangre = pcomboSangre.get().strip()
    if not validarFiltrosTipoSangreProvincia(seleccionProvincia, seleccionSangre):
        return  
    if not pdonadores:
        messagebox.showwarning("Aviso", "No hay donadores registrados en el sistema.")
        return
    claveProvincia = ""
    for clave, datosProvincia in pprovinciasDiccionario.items():
        nombreProvinciaDiccionario = datosProvincia[0]
        if nombreProvinciaDiccionario.lower() == seleccionProvincia.lower():
            claveProvincia = str(clave)
            break
    if not claveProvincia:
        messagebox.showerror("Error", f"La provincia '{seleccionProvincia}' no es válida en el sistema.")
        return
    try:
        procesarReporteTipoSangreProvinciaHtml(pdonadores, claveProvincia, seleccionProvincia, seleccionSangre)
        messagebox.showinfo("Éxito", "Reporte generado correctamente.")
    except Exception as error:
        messagebox.showerror("Error", f"Ocurrió un fallo inesperado al construir el reporte: {str(error)}")

def ventanaReporteTipoSangreProvincia():
    ventana = tk.Toplevel()
    comboProvincia = ttk.Combobox(
        ventana,
        values=[datos[0] for datos in provinciasDiccionario.values()],
        state="readonly"
    )
    comboProvincia.pack()
    comboSangre = ttk.Combobox(
        ventana,
        values=tipoSangre,
        state="readonly"
    )
    comboSangre.pack()
    tk.Button(
        ventana,
        text="Generar",
        command=lambda: reporteTipoSangreProvinciaAux(
            comboProvincia,
            comboSangre,
            donadores,
            provinciasDiccionario
        )
    ).pack()

# reporte 4

def validarMatrizDonadoresReporteGeneral(pdonadores):
    if not pdonadores:
        messagebox.showwarning("Aviso", "No existen donadores registrados en el sistema para generar el reporte.")
        return False
    return True

def procesarReporteGeneralDonadoresHtml(pdonadores, pprovinciasDiccionario):
    fechaHoraActual = datetime.now().strftime("%d/%m/%Y %I:%M %p")
    formatoFechaArchivo = datetime.now().strftime("%d_%m_%Y_%I_%M_%p")
    filasHtml = ""
    contadorTotalDonadores = 0
    for claveProvincia in sorted(pprovinciasDiccionario.keys()):
        nombreProvincia = pprovinciasDiccionario[claveProvincia][0]
        filasProvincia = ""
        contadorProvincia = 0
        for donador in pdonadores:
            cedula = str(donador[1])
            estado = donador[8]  
            if estado == 1 and cedula[0] == claveProvincia:
                contadorProvincia += 1
                contadorTotalDonadores += 1
                nombreCompleto = " ".join(donador[0])
                tipoSangreDonador = tipoSangre[donador[2]]
                lugarDonacion = donador[6]
                filasProvincia += f"""        <tr>
            <td>{cedula}</td>
            <td>{nombreCompleto}</td>
            <td style="color: #e74c3c; font-weight: bold;">{tipoSangreDonador}</td>
            <td>{lugarDonacion}</td>
        </tr>\n"""
        if contadorProvincia > 0:
            filasHtml += f"""        <tr style="background-color: #2c3e50; color: white; font-weight: bold;">
            <td colspan="4" style="text-align: center;">PROVINCIA: {nombreProvincia.upper()} ({contadorProvincia} activos)</td>
        </tr>\n"""
            filasHtml += filasProvincia

    if contadorTotalDonadores == 0:
        messagebox.showinfo("Información", "No se encontraron donadores activos registrados en ninguna provincia.")
        return False
    htmlCompleto = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Reporte General de Donadores Activos</title>
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
    <h1>Reporte General de Donadores</h1>
    <h2>Distribución Nacional de Donadores Activos</h2>
    <div class="fecha-reporte">Reporte generado el: {fechaHoraActual}</div>
    
    <div class="info">Total global de donadores activos en el sistema: {contadorTotalDonadores}</div>
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
    
    nombreArchivo = f"reporteGeneral{formatoFechaArchivo}.html"
    try:
        with open(nombreArchivo, "w", encoding="utf-8") as archivo:
            archivo.write(htmlCompleto)
        webbrowser.open(nombreArchivo)
        return True
    except Exception:
        return False
    
def reporteGeneralDonadoresAux(pdonadores, pprovinciasDiccionario):
    if not validarMatrizDonadoresReporteGeneral(pdonadores):
        return  
    fueCreadoExitosamente = procesarReporteGeneralDonadoresHtml(pdonadores, pprovinciasDiccionario)
    if fueCreadoExitosamente:
        messagebox.showinfo("Éxito", "Reporte generado")
    else:
        messagebox.showerror("Error", "No se pudo escribir el archivo del reporte general en el disco.")

# reporte 5

def validarMatrizDonadores(pDonadores):
    if not pDonadores or len(pDonadores) == 0:
        messagebox.showwarning("Aviso", "No existen donadores registrados en el sistema para procesar.")
        return False
    return True

def calcularEdadExacta(pFechaNacimientoStr):
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
    fechaHoraSistema = datetime.now().strftime("%d/%m/%Y %I:%M %p")
    formatoFechaArchivo = datetime.now().strftime("%d_%m_%Y_%I_%M_%p")
    listaFiltrada = []
    for donador in pDonadores:
        if len(donador) < 10:
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

def reporteMujeresOMinusculasAux(pDonadores):
    if not validarMatrizDonadores(pDonadores):
        return
    fueCreadoExitosamente = procesarReporteMujeresOMinusculasHtml(pDonadores)
    if fueCreadoExitosamente:
        messagebox.showinfo("Éxito", "Reporte creado satisfactoriamente")
    else:
        messagebox.showerror("Error", "Reporte no creado.")


# reporte 6

def validarFiltroCompatibilidadDonacion(pTipoSangreSeleccionado):
    if not pTipoSangreSeleccionado:
        messagebox.showwarning("Aviso", "Por favor, seleccione un tipo de sangre para continuar.")
        return False
    return True

def esDonadorCompatible(pTipoDonador, pTipoReceptor):
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

def procesarReporteCompatibilidadDonacionHtml(pDonadores, pProvinciasDiccionario, pTipoReceptor):
    fechaHoraActual = datetime.now().strftime("%d/%m/%Y %I:%M %p")
    formatoFechaArchivo = datetime.now().strftime("%d_%m_%Y_%I_%M_%p")
    
    filasHtml = ""
    contadorTotalDonadores = 0
    for claveProvincia in sorted(pProvinciasDiccionario.keys()):
        nombreProvincia = pProvinciasDiccionario[claveProvincia][0]
        filasProvincia = ""
        contadorProvincia = 0
        for donador in pDonadores:
            cedula = str(donador[1])
            tipoDonador = tipoSangre[donador[2]]
            idProvinciaDonador = cedula[0]
            estado = donador[8]  
            if estado == 1 and idProvinciaDonador == claveProvincia and esDonadorCompatible(tipoDonador, pTipoReceptor):

                contadorProvincia += 1
                contadorTotalDonadores += 1
                nombreCompleto = " ".join(donador[0])
                telefono = donador[7]
                correo = donador[6]
                filasProvincia += f"""        <tr>
            <td>{cedula}</td>
            <td>{nombreCompleto}</td>
            <td style="color: #e74c3c; font-weight: bold;">{tipoDonador}</td>
            <td>{telefono}</td>
            <td>{correo}</td>
        </tr>\n"""
        if contadorProvincia > 0:
            filasHtml += f"""        <tr style="background-color: #2c3e50; color: white; font-weight: bold;">
            <td colspan="5" style="text-align: center;">PROVINCIA: {nombreProvincia.upper()} ({contadorProvincia} compatibles)</td>
        </tr>\n"""
            filasHtml += filasProvincia

    if contadorTotalDonadores == 0:
        messagebox.showinfo("Información", f"No se encontraron donadores activos compatibles para abastecer al tipo {pTipoReceptor}.")
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
        .fecha-reporte {{ text-align: center; color: #7f8c8d; font-style: italic; margin-bottom: 25px; }}
        .info {{ font-weight: bold; margin-bottom: 15px; color: #333; font-size: 1.1em; }}
        table {{ width: 100%; border-collapse: collapse; background-color: #ffffff; }}
        th, td {{ border: 1px solid #bdc3c7; text-align: left; padding: 12px; }}
        th {{ background-color: #e74c3c; color: white; }}
        tr:nth-child(even) {{ background-color: #f9ecec; }}
    </style>
</head>
<body>
    <h1>¿A quién puede donar?</h1>
    <h2>Donadores Aptos para Abastecer a Receptores Tipo: <b>{pTipoReceptor}</b></h2>
    <div class="fecha-reporte">Reporte generado el: {fechaHoraActual}</div>
    
    <div class="info">Total de donadores compatibles encontrados a nivel nacional: {contadorTotalDonadores}</div>
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
    sangreLimpia = pTipoReceptor.replace('+', '_pos').replace('-', '_neg')
    nombreArchivo = f"reporteCompatibilidad{sangreLimpia}_{formatoFechaArchivo}.html"
    try:
        with open(nombreArchivo, "w", encoding="utf-8") as archivo:
            archivo.write(htmlCompleto)
        webbrowser.open(nombreArchivo)
        return True
    except Exception:
        return False

def reporteCompatibilidadDonacionAux(pDonadores, pProvinciasDiccionario, pTipoSangreTupla):
    ventanaCompatibilidad = tk.Toplevel()
    ventanaCompatibilidad.title("¿A quién puede donar?")
    ventanaCompatibilidad.geometry("360x220")
    ventanaCompatibilidad.resizable(False, False)
    tk.Label(
        ventanaCompatibilidad, 
        text="Seleccione el Tipo de Sangre del Receptor:", 
        font=("Arial", 10, "bold")
    ).pack(pady=(20, 5))
    comboSangre = ttk.Combobox(
        ventanaCompatibilidad, 
        values=pTipoSangreTupla, 
        state="readonly", 
        width=20
    )
    comboSangre.pack(pady=10)
    marcoBotones = tk.Frame(ventanaCompatibilidad)
    marcoBotones.pack(pady=20)
    
    def ejecutarAccionGenerar():
        seleccionSangre = comboSangre.get().strip()
        if not validarFiltroCompatibilidadDonacion(seleccionSangre):
            return  
        if not pDonadores:
            messagebox.showwarning("Aviso", "No hay donadores registrados en el sistema.")
        fueCreadoExitosamente = procesarReporteCompatibilidadDonacionHtml(
            pDonadores, pProvinciasDiccionario, seleccionSangre
        )
        if fueCreadoExitosamente:
            messagebox.showinfo("Éxito", "Reporte creado satisfactoriamente")
            ventanaCompatibilidad.destroy()
        else:
            messagebox.showerror("Error", "Reporte no creado.")
    btnGenerar = tk.Button(
        marcoBotones, 
        text="Generar reporte", 
        width=15, 
        command=ejecutarAccionGenerar
    )
    btnGenerar.pack(side="left", padx=5)
    btnRegresar = tk.Button(
        marcoBotones, 
        text="Regresar", 
        width=15, 
        command=lambda: ventanaCompatibilidad.destroy()
    )
    btnRegresar.pack(side="left", padx=5)

# reporte 7

def validarCamposCompatibilidad(pTipoSangreSeleccionado):
    if not pTipoSangreSeleccionado or pTipoSangreSeleccionado == "":
        messagebox.showerror("Error de Validación", "Por favor, seleccione un tipo de sangre de la lista.")
        return False
    return True

def procesarReporteCompatibilidadHtml(pDonadores, pTipoSangreObjetivo):
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

def reporteCompatibilidadRecibirAux(pDonadores, pTipoSangreTupla):
    ventanaCompatibilidad = tk.Toplevel()
    ventanaCompatibilidad.title("Compatibilidad de Receptores")
    ventanaCompatibilidad.geometry("380x200")
    ventanaCompatibilidad.resizable(False, False)
    ventanaCompatibilidad.grab_set()
    lblInstruccion = tk.Label(
        ventanaCompatibilidad, 
        text="Seleccione el Tipo de Sangre del Receptor:",
        font=("Arial", 10, "bold")
    )
    lblInstruccion.pack(pady=(20, 5))
    comboSangre = ttk.Combobox(
        ventanaCompatibilidad, 
        values=pTipoSangreTupla, 
        state="readonly", 
        width=20
    )
    comboSangre.pack(pady=10)
    def ejecutarGeneracionReporte():
        tipoSangreSeleccionado = comboSangre.get()
        if not validarCamposCompatibilidad(tipoSangreSeleccionado):
            return
        fueCreado = procesarReporteCompatibilidadHtml(pDonadores, tipoSangreSeleccionado)
        if fueCreado:
            messagebox.showinfo("Éxito", "Reporte creado satisfactoriamente")
            ventanaCompatibilidad.destroy() 
        else:
            messagebox.showerror("Error", "Reporte no creado.")
    marcoBotones = tk.Frame(ventanaCompatibilidad)
    marcoBotones.pack(pady=20)
    btnGenerar = tk.Button(
        marcoBotones, 
        text="Generar reporte", 
        width=15, 
        bg="#16a085", 
        fg="white",
        command=ejecutarGeneracionReporte
    )
    btnGenerar.pack(side="left", padx=10)
    btnRegresar = tk.Button(
        marcoBotones, 
        text="Regresar", 
        width=15, 
        command=ventanaCompatibilidad.destroy
    )
    btnRegresar.pack(side="left", padx=10)

# Donadores inactvos
def validarDonadoresInactivos(pmatrizDonadores):
    if not pmatrizDonadores:
        return False
    for donador in pmatrizDonadores:
        if donador[8] == 0:  
            return True
    return False

def procesarReporteInactivos(pmatrizDonadores):
    fechaHoraActual = datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")
    nombreArchivo = "reporteDonadoresInactivos.html"

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

            for donador in pmatrizDonadores:
                estado = donador[8]
                if estado != 0:
                    continue  # 👈 saltar activos

                cedula = donador[1]
                nombreCompleto = " ".join(donador[0])
                tipoSangreStr = tipoSangre[donador[2]]  
                sexo = "F" if donador[3] == False else "M"
                tuplaFecha = donador[4]
                fechaNacimiento = f"{tuplaFecha[0]:02d}/{tuplaFecha[1]:02d}/{tuplaFecha[2]}"
                peso = donador[5]
                correo = donador[6]
                telefono = donador[7]
                justificacion=donador[9]
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
        webbrowser.open(nombreArchivo)  
        return True
    except Exception as e:
        print(f"Error al generar reporte: {e}")  
        return False

# submenu reportes
def submenuReportes(pventanaPadre):

    ventanaReportes = tk.Toplevel(pventanaPadre)

    ventanaReportes.title("Menú de Reportes")
    ventanaReportes.geometry("450x500")
    ventanaReportes.resizable(False, False)

    tk.Label(
        ventanaReportes,
        text="Menú de Reportes",
        font=("Arial", 14, "bold")
    ).pack(pady=15)

    tk.Button(
        ventanaReportes,
        text="1. Donadores por Provincia",
        width=35,
        command=lambda: reportePorProvinciaAux(donadores)
    ).pack(pady=3)

    tk.Button(
        ventanaReportes,
        text="2. Donadores por Tipo de Sangre",
        width=35,
        command=lambda: reportePorSangreAux(donadores)
    ).pack(pady=3)

    tk.Button(
        ventanaReportes,
        text="3. Tipo de Sangre por Provincia",
        width=35,
        command=lambda: ventanaReporteTipoSangreProvincia()
    ).pack(pady=3)

    tk.Button(
        ventanaReportes,
        text="4. Reporte General de Donadores",
        width=35,
        command=lambda: reporteGeneralDonadoresAux(
            donadores,
            provinciasDiccionario
        )
    ).pack(pady=3)

    tk.Button(
        ventanaReportes,
        text="5. Mujeres O- Menores de 45",
        width=35,
        command=lambda: reporteMujeresOMinusculasAux(donadores)
    ).pack(pady=3)

    tk.Button(
        ventanaReportes,
        text="6. ¿A quién puede donar?",
        width=35,
        command=lambda: reporteCompatibilidadDonacionAux(
            donadores,
            provinciasDiccionario,
            tipoSangre
        )
    ).pack(pady=3)

    tk.Button(
        ventanaReportes,
        text="7. Compatibilidad para recibir",
        width=35,
        command=lambda: reporteCompatibilidadRecibirAux(
            donadores,
            tipoSangre
        )
    ).pack(pady=3)

    tk.Button(
        ventanaReportes,
        text="8. Donadores Inactivos",
        width=35,
        command=lambda: procesarReporteInactivos(donadores)
    ).pack(pady=3)

    tk.Button(
        ventanaReportes,
        text="Regresar",
        width=35,
        command=ventanaReportes.destroy
    ).pack(pady=15)

menuPrincipal()