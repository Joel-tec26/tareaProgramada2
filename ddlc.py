#
#
#
#

import re
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk
import pickle
archivoDonadores = "donadores.dat"

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

# ingresar donadores

# prosesamiento 
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

def buscarDonador(cedulaTarget, matrizA_Buscar):
    izquierda = 0
    derecha = len(matrizA_Buscar) - 1
    
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        cedulaMedio = matrizA_Buscar[medio][0]
        
        if cedulaMedio == cedulaTarget:
            return True, medio
        elif cedulaMedio < cedulaTarget:
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
    peso = int(pesoStr)
    if peso <= 50:
        return "Usted debe pesar más de 50 kgms para poder ser donador."
    if 50 < peso <= 110:
        return "Usted posee un peso adecuado, correcto para ser donador de sangre."
    return "Dado su sobre peso, no es posible donar sangre."

def obtenerRecomendacionSangre(tipoSangre):
    mensaje = f"Conoce tu tipo de sangre {tipoSangre}"
    if tipoSangre in ["A+", "A-"]:
        mensaje += "\nPor el tipo de sangre le recomendamos ver el video de: Particularidades de la sangre tipo A Responde diferente al estrés según la ciencia."
    return mensaje

def obtenerInformacionResaltadaSangre(tipoSangre):
    tipoSangre = tipoSangre.upper()
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
    baseMensaje = f"Conoce tu tipo de sangre {tipoSangre}: A los donantes con este tipo {recomendaciones.get(tipoSangre, '')}"
    if tipoSangre in ["A+", "A-"]:
        baseMensaje += "\n\nAdemás, se le sugiere ver el video de Particularidades de la sangre tipo A: Responde diferente al estrés según la ciencia."
        
    return baseMensaje
    
# validaciones

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
        peso = int(pesoStr)
        return 50 < peso < 120
    except ValueError:
        return False
    
# auxiliar

def insertarDonadorAux(matrizDonadores, pprovincias):
    def registrar():
        cedula = entradaCedula.get().strip()
        nombre = entradaNombre.get().strip()
        fechaNac = entradaFecha.get().strip()
        tipoSangre = comboSangre.get()
        sexo = "Masculino" if varSexo.get() == 1 else "Femenino"
        peso = entradaPeso.get().strip()
        telefono = entradaTelefono.get().strip()
        correo = entradaCorreo.get().strip()
        #  Validaciones
        if not validarCedula(cedula):
            messagebox.showwarning("Aviso", "Formato de cédula incorrecto.\nDebe ser #-####-#### (ej. 2-0893-0750) y no puede iniciar con 0.")
            return
        if not nombre:
            messagebox.showwarning("Aviso", "El nombre completo es requerido.")
            return
        if not validarFechaNacimiento(fechaNac):
            messagebox.showwarning("Aviso", "Fecha de nacimiento inválida.\nDebe usar el formato DD/MM/AAAA (ej. 25/12/2000).")
            return
        if not validarPeso(peso):
            messagebox.showwarning("Aviso", "El peso debe ser un número entero mayor a 50 y menor a 120.")
            return
        if not validarTelefono(telefono):
            messagebox.showwarning("Aviso", "Formato de teléfono incorrecto.\nDebe ser de 8 dígitos (ej. 61375404) y no puede iniciar con 0, 1, 3 o 5.")
            return
        if not validarCorreo(correo):
            messagebox.showwarning("Aviso", "Correo no permitido.\nSolo se aceptan dominios: @costarricense.cr, @racsa.go.cr, @ccss.sa.cr o @gmail.com")
            return

        # Búsqueda Binaria para evitar duplicaciones
        existe, posicion = buscarDonador(cedula, matrizDonadores)
        if existe:
            messagebox.showwarning("Aviso", f"La cédula {cedula} ya se encuentra registrada en el sistema.")
            return
        nuevoRegistro = [cedula, nombre, fechaNac, tipoSangre, sexo, int(peso), telefono, correo, True]
        matrizDonadores.insert(posicion, nuevoRegistro)
        # Guardar el objeto completo usando pickle
        guardarMatrizEnArchivo(matrizDonadores)
        #  textos para el mensaje
        msgEdad = obtenerMensajeEdad(fechaNac)
        msgLugar = obtenerLugarDonacion(cedula, pprovincias)
        msgPeso = obtenerMensajePeso(peso)
        msgSangre = obtenerInformacionResaltadaSangre(tipoSangre)

        resultadoFluido = (
            f"{msgEdad}\n\n"
            f"{msgLugar}\n\n"
            f"{msgPeso}\n\n"
            f"{msgSangre}"
        )
        messagebox.showinfo("Información de la inserción inicial", resultadoFluido)
        limpiar()

    def limpiar():
        entradaCedula.delete(0, tk.END)
        entradaNombre.delete(0, tk.END)
        entradaFecha.delete(0, tk.END)
        comboSangre.set("O+")
        varSexo.set(1)
        entradaPeso.delete(0, tk.END)
        entradaTelefono.delete(0, tk.END)
        entradaCorreo.delete(0, tk.END)

    def regresar():
        ventana.destroy()

    # Creación de la Interfaz con Tkinter
    ventana = tk.Tk()
    ventana.title("Insertar donador")
    ventana.geometry("550x360")

    tk.Label(ventana, text="Cédula").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    entradaCedula = tk.Entry(ventana, width=25)
    entradaCedula.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Nombre Completo").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    entradaNombre = tk.Entry(ventana, width=40)
    entradaNombre.grid(row=1, column=1, columnspan=2, sticky="w", padx=10, pady=5)

    tk.Label(ventana, text="Fecha de nacimiento").grid(row=2, column=0, sticky="w", padx=10, pady=5)
    entradaFecha = tk.Entry(ventana, width=25)
    entradaFecha.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Tipo de sangre").grid(row=3, column=0, sticky="w", padx=10, pady=5)
    opcionesSangre = ["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"]
    comboSangre = ttk.Combobox(ventana, values=opcionesSangre, state="readonly", width=10)
    comboSangre.set("O+")
    comboSangre.grid(row=3, column=1, sticky="w", padx=10, pady=5)

    tk.Label(ventana, text="Sexo").grid(row=4, column=0, sticky="w", padx=10, pady=5)
    varSexo = tk.IntVar(value=1)
    tk.Radiobutton(ventana, text="Masculino", variable=varSexo, value=1).grid(row=4, column=1, sticky="w", padx=10)
    tk.Radiobutton(ventana, text="Femenino", variable=varSexo, value=2).grid(row=4, column=1, sticky="w", padx=110)

    tk.Label(ventana, text="Peso").grid(row=5, column=0, sticky="w", padx=10, pady=5)
    entradaPeso = tk.Entry(ventana, width=25)
    entradaPeso.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Teléfono").grid(row=6, column=0, sticky="w", padx=10, pady=5)
    entradaTelefono = tk.Entry(ventana, width=25)
    entradaTelefono.grid(row=6, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Correo").grid(row=7, column=0, sticky="w", padx=10, pady=5)
    entradaCorreo = tk.Entry(ventana, width=35)
    entradaCorreo.grid(row=7, column=1, columnspan=2, sticky="w", padx=10, pady=5)

    marcoBotones = tk.Frame(ventana)
    marcoBotones.grid(row=8, column=0, columnspan=3, pady=15)

    tk.Button(marcoBotones, text="Registrar", command=registrar, width=10).pack(side="left", padx=5)
    tk.Button(marcoBotones, text="Limpiar", command=limpiar, width=10).pack(side="left", padx=5)
    tk.Button(marcoBotones, text="Regresar", command=regresar, width=10).pack(side="left", padx=5)

    ventana.mainloop()

# eliminar donador

def eliminarDonadorAux(matrizDonadores):
    """
    """
    def ProcesarInactivacion():
        cedula = entradaCedula.get().strip()
        justificacionSeleccionada = comboJustificacion.get()

        if not validarCedula(cedula):
            messagebox.showwarning("Aviso", "Formato de cédula incorrecto.\nDebe ser #-####-####.")
            return
        if not justificacionSeleccionada:
            messagebox.showwarning("Aviso", "Debe seleccionar una justificación para la exclusión del donador.")
            return

        # Búsqueda binaria 
        existe, posicion = buscarDonador(cedula, matrizDonadores)

        if not existe:
            messagebox.showwarning("Aviso", f"La persona con el número de cédula: {cedula} no está registrado en la base de datos del Banco de Sangre aún.")
            return

        # Validación lógica por si ya fue inactivado previamente
        if matrizDonadores[posicion][8] == False:
            messagebox.showinfo("Información", "Esta persona ya se encuentra registrada como un donador Inactivo.")
            return

        # Ventana de confirmación
        confirmacion = messagebox.askyesno("Confirmar acción", f"¿Está seguro de que desea inactivar al donador con cédula {cedula}?")
        
        if confirmacion:
            # Cambio de estado lógico 
            if len(matrizDonadores[posicion]) == 8:
                matrizDonadores[posicion].append(False) 
                matrizDonadores[posicion].append(justificacionSeleccionada) 
            elif len(matrizDonadores[posicion]) == 9:
                matrizDonadores[posicion][8] = False # Modifica el estado existente
                matrizDonadores[posicion].append(justificacionSeleccionada) 
            else:
                matrizDonadores[posicion][8] = False
                matrizDonadores[posicion][9] = justificacionSeleccionada
            guardarMatrizEnArchivo(matrizDonadores)
            messagebox.showinfo("Información", "Donador eliminado satisfactoriamente.")
            regresar()
        else:
            messagebox.showinfo("Información", "Donador NO eliminado.")

    def limpiar():
        entradaCedula.delete(0, tk.END)
        comboJustificacion.set("")

    def regresar():
        ventana.destroy()

    ventana = tk.Tk()
    ventana.title("Eliminar donador")
    ventana.geometry("520x200")

    tk.Label(ventana, text="Cédula a buscar:").grid(row=0, column=0, sticky="w", padx=15, pady=15)
    entradaCedula = tk.Entry(ventana, width=20)
    entradaCedula.grid(row=0, column=1, sticky="w", padx=15, pady=15)

    tk.Label(ventana, text="Justificación del rechazo:").grid(row=1, column=0, sticky="w", padx=15, pady=10)
    
    # Lista de causas de rechazo según normativas
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

    # Contenedor de control inferior
    marcoBotones = tk.Frame(ventana)
    marcoBotones.grid(row=2, column=0, columnspan=2, pady=15)

    tk.Button(marcoBotones, text="Inactivar", command=ProcesarInactivacion, width=10).pack(side="left", padx=5)
    tk.Button(marcoBotones, text="Limpiar", command=limpiar, width=10).pack(side="left", padx=5)
    tk.Button(marcoBotones, text="Regresar", command=regresar, width=10).pack(side="left", padx=5)

    ventana.mainloop()


donadores= cargarDatosDesdeArchivo()