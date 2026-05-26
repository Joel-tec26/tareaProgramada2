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

# Procesar
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
    cedulaInt = int(cedulaTarget.replace("-", ""))
    izquierda = 0
    derecha = len(matrizA_Buscar) - 1
    
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        cedulaMedio = matrizA_Buscar[medio][1] 
        
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
    root.geometry("400x300")
    root.resizable(False, False)
    tk.Label(root, text="Sistema Banco de Sangre", font=("Arial", 14, "bold")).pack(pady=20)
    tk.Button(root, text="Insertar Donador", width=25, command=lambda: insertarDonadorAux(donadores, provinciasDiccionario)).pack(pady=5)
    tk.Button(root, text="Eliminar Donador", width=25, command=lambda: eliminarDonadorAux(donadores)).pack(pady=5)
    tk.Button(root, text="Insertar Lugar de Donación", width=25, command=insertarLugarDonacionAux).pack(pady=5)
    tk.Button(root, text="Salir", width=25, command=root.destroy).pack(pady=20)
    root.mainloop()

menuPrincipal()