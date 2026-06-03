# creado por: Alexis Torres y Joel Porras
# fecha de creacion: 2/06/2026
# ultima modificación: 
# version: 3.14

# imporaticion de librerias
import re
import pickle
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import *
import faker
fk=faker.Faker("es_ES")
from funciones import *


# definicion de funciones

def validarCantidad(pcantidad):
    """
    funcion: verifica que una cantidad es entera y mayor a 0
    entradas:
    -pcantidad(int) numero ingresado por el usuario
    salidas:
    -bool: si es o no valido
    """
    try:
        cantidad = int(pcantidad)
        return 0 < cantidad 
    except ValueError:
        return False
    
def actualizarMatrizEnArchivo(matrizGuardar):
    """
    funcion: guarda la matriz actualizada en archivo, reemplazando lo viejo con lo nuevo
    entradas:
    -matrizGuardar: matriz nueva
    salidas:
    -no hay
    """
    with open(archivoDonadores, "wb") as archivo:
        pickle.dump(matrizGuardar, archivo)
    return

def normalizarNombre(nombreSucio):
    """
    Funcionalidad:
    Limpia y normaliza un nombre eliminando espacios extra y aplicando 
    formato de título.
    Entradas:
    -nombreSucio(str): nombre con posibles espacios innecesarios 
    o formato incorrecto
    Salidas:
    -nombre(tupla): nombre limpio con la primera letra de cada palabra
    en mayúscula
    """
    return tuple(" ".join(nombreSucio.strip().split()).title().split())

def generarDonantesAux(pbaseDatos):
    """
    funcion: Mostrar la ventana y genera la cantidad de donantes que uno quiera.
    entradas:
    - pbaseDatos: matriz de donadores.
    salidas:
    - pbaseDatos: matriz de donadores actualizada.
    """
    def generar():
        """
        funcion: valida entradas genera los donantes
        entradas: ninguna
        salidas: ninguna
        """
        cantidad = entradaCantidad.get().strip()
        if not validarCantidad(cantidad):
            messagebox.showwarning("Aviso","debe escribir un valor numerico mayor a 0")
            return pbaseDatos
        for i in generarDonantes(int(cantidad),pbaseDatos):
            pbaseDatos.append(i)
        guardarMatrizEnArchivo(pbaseDatos)
        limpiar()
    
    def limpiar():
        """
        funcion:
        Limpiar los campos del formulario de registro.
        entradas:
        - Ninguna.
        salidas:
        - Ninguna.
        """
        entradaCantidad.delete(0, tk.END)

    ventana = tk.Toplevel()
    ventana.title("Generar Donante/s")
    ventana.geometry("550x360")
    tk.Label(ventana, text="Generar Donante/s", font=("Arial", 20)).grid(row=0, column=1, sticky="w", padx=10, pady=5)
    tk.Label(ventana, text="Cantidad de Donantes").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    entradaCantidad = tk.Entry(ventana, width=25)
    entradaCantidad.grid(row=1, column=1, padx=10, pady=5)
    marcoBotones = tk.Frame(ventana)
    marcoBotones.grid(row=8, column=0, columnspan=3, pady=15)
    tk.Button(marcoBotones, text="Generar", command=generar, width=10).pack(side="left", padx=5)
    tk.Button(marcoBotones, text="Limpiar", command=limpiar, width=10).pack(side="left", padx=5)
    tk.Button(marcoBotones, text="Regresar", command=lambda: ventana.destroy(), width=10).pack(side="left", padx=5)
    ventana.mainloop()
    return pbaseDatos

def actualizarDonanteAux(pbaseDatos):
    """
    funcion: Mostrar la ventana para actualizar un donante.
    entradas:
    - pbaseDatos: matriz de donadores.
    salidas:
    - pbaseDatos: matriz de donadores actualizada.
    """
    def actualizar():
        """
        funcion: valida entradas y actualiza a un donante
        entradas: ninguna
        salidas: ninguna
        """
        if pbaseDatos==[]:
            messagebox.showwarning("Aviso", "no hay ningun paciente registrado")
            return
        cedula = entradaCedula.get().strip()
        nombre = entradaNombre.get().strip()
        fechaNac = entradaFecha.get().strip()
        dia, mes, anno = map(int, fechaNac.split("/"))
        tuplaFecha = (dia, mes, anno)
        tipoSangreInt = ("O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-").index(comboSangre.get())
        sexo = varSexo.get()
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
        # Búsqueda Binaria para ver si existe para poder actualizar
        existe, posicion = validarDonante(pcedula=cedula, pmatriz=pbaseDatos)
        if not existe:
            messagebox.showwarning("Aviso", f"La cédula {cedula} no se encuentra registrada en el sistema.")
            return
        confirmacion = messagebox.askyesno("Confirmar acción", f"¿Está seguro de que desea actualizar al donador con cédula {cedula}?")
        if confirmacion:
            nuevoRegistro = [normalizarNombre(nombre), cedula, tuplaFecha, tipoSangreInt, sexo, float(peso), telefono, correo]
            pbaseDatos[posicion]=nuevoRegistro
            actualizarMatrizEnArchivo(pbaseDatos)
            messagebox.showinfo("Información", "Donador actualizado satisfactoriamente.")
            limpiar()
        else:
            messagebox.showinfo("Información", "Donador NO actualizado.")    

    def limpiar():
        """
        funcion:
        Limpiar los campos del formulario de registro.
        entradas:
        - Ninguna.
        salidas:
        - Ninguna.
        """
        entradaCedula.delete(0, tk.END)
        entradaNombre.delete(0, tk.END)
        entradaFecha.delete(0, tk.END)
        comboSangre.set("O+")
        varSexo.set(1)
        entradaPeso.delete(0, tk.END)
        entradaTelefono.delete(0, tk.END)
        entradaCorreo.delete(0, tk.END)

    ventana = tk.Tk()
    ventana.title("Insertar donador")
    ventana.geometry("550x360")
    tk.Label(ventana, text="Actualizar Donante", font=("Arial", 20)).grid(row=0, column=1, sticky="w", padx=10, pady=5)

    tk.Label(ventana, text="Cédula").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    entradaCedula = tk.Entry(ventana, width=25)
    entradaCedula.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Nombre Completo").grid(row=2, column=0, sticky="w", padx=10, pady=5)
    entradaNombre = tk.Entry(ventana, width=40)
    entradaNombre.grid(row=2, column=1, columnspan=2, sticky="w", padx=10, pady=5)

    tk.Label(ventana, text="Fecha de nacimiento").grid(row=3, column=0, sticky="w", padx=10, pady=5)
    entradaFecha = tk.Entry(ventana, width=25)
    entradaFecha.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Tipo de sangre").grid(row=5, column=0, sticky="w", padx=10, pady=5)
    opcionesSangre = ["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"]
    comboSangre = ttk.Combobox(ventana, values=opcionesSangre, state="readonly", width=10)
    comboSangre.set("O+")
    comboSangre.grid(row=5, column=1, sticky="w", padx=10, pady=5)

    tk.Label(ventana, text="Sexo").grid(row=4, column=0, sticky="w", padx=10, pady=5)
    varSexo = tk.IntVar(value=1)
    tk.Radiobutton(ventana, text="Masculino", variable=varSexo, value=1).grid(row=4, column=1, sticky="w", padx=10)
    tk.Radiobutton(ventana, text="Femenino", variable=varSexo, value=2).grid(row=4, column=1, sticky="w", padx=110)

    tk.Label(ventana, text="Peso").grid(row=6, column=0, sticky="w", padx=10, pady=5)
    entradaPeso = tk.Entry(ventana, width=25)
    entradaPeso.grid(row=6, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Teléfono").grid(row=7, column=0, sticky="w", padx=10, pady=5)
    entradaTelefono = tk.Entry(ventana, width=25)
    entradaTelefono.grid(row=7, column=1, padx=10, pady=5)

    tk.Label(ventana, text="Correo").grid(row=8, column=0, sticky="w", padx=10, pady=5)
    entradaCorreo = tk.Entry(ventana, width=35)
    entradaCorreo.grid(row=8, column=1, columnspan=2, sticky="w", padx=10, pady=5)
    marcoBotones = tk.Frame(ventana)
    marcoBotones.grid(row=9, column=0, columnspan=3, pady=15)
    tk.Button(marcoBotones, text="Actualizar", command=actualizar, width=10, cursor="hand2").pack(side="left", padx=5)
    tk.Button(marcoBotones, text="Limpiar", command=limpiar, width=10, cursor="hand2").pack(side="left", padx=5)
    tk.Button(marcoBotones, text="Regresar", command=lambda:ventana.destroy(), width=10, cursor="hand2").pack(side="left", padx=5)
    ventana.mainloop()
    return pbaseDatos

# joel

# Validaciones

def validarCedula(cedula):
    """
    funcion: Verificar que la cédula cumpla con el formato permitido.
    entradas:
    - cedula: cédula a validar.
    salidas:
    - True si la cédula es válida, False en caso contrario.
    """
    patron = r"^[1-9]-\d{3,5}-\d{3,4}$"
    return bool(re.match(patron, cedula))

def validarFechaNacimiento(fechaStr):
    """
    funcion: Verificar que la fecha tenga un formato válido.
    entradas:
    - fechaStr: fecha en formato DD/MM/AAAA.
    salidas:
    - True si la fecha es válida, False en caso contrario.
    """
    try:
        datetime.strptime(fechaStr, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def validarCorreo(correo):
    """
    funcion: Verificar que el correo pertenezca a un dominio permitido.
    entradas:
    - correo: dirección de correo electrónico.
    salidas:
    - True si el correo es válido, False en caso contrario.
    """
    patron = r"^[a-zA-Z0-9._%+-]+@(costarricense\.cr|racsa\.go\.cr|ccss\.sa\.cr|gmail\.com)$"
    return bool(re.match(patron, correo))

def validarTelefono(telefono):
    """
    funcion: Verificar que el número telefónico tenga el formato correcto.
    entradas:
    - telefono: número telefónico.
    salidas:
    - True si el teléfono es válido, False en caso contrario.
    """
    patron = r"^[246789]\d{3}-\d{4}$"
    return bool(re.match(patron, telefono))

def validarPeso(pesoStr):
    """
    funcion: Verificar que el peso esté dentro del rango permitido.
    entradas:
    - pesoStr: peso de la persona.
    salidas:
    - True si el peso es válido, False en caso contrario.
    """
    try:
        peso = float(pesoStr)
        return 50.0 < peso < 120.0
    except ValueError:
        return False
    
# aux
def insertarDonadorAux(matrizDonadores, pprovincias):
    """
    funcion: Mostrar la ventana para registrar un nuevo donador.
    entradas:
    - matrizDonadores: matriz de donadores.
    - pprovincias: diccionario con provincias y lugares de donación.
    salidas:
    - Ninguna.
    """
    def registrar():
        """
        funcion:
        Validar y registrar un nuevo donador en la matriz.
        entradas:
        - Ninguna. Obtiene los datos desde los componentes de la ventana.
        salidas:
        - Ninguna.
        """
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
        """
        funcion:
        Limpiar los campos del formulario de registro.
        entradas:
        - Ninguna.
        salidas:
        - Ninguna.
        """
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
    """
    funcion: Mostrar la ventana para inactivar un donador registrado.
    entradas:
    - matrizDonadores: matriz de donadores.
    salidas:
    - Ninguna.
    """
    def ProcesarInactivacion():
        """
        funcion:
        Inactivar un donador y registrar la causa de rechazo.
        entradas:
        - Ninguna. Obtiene los datos desde la ventana.
        salidas:
        - Ninguna.
        """
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
    """
    funcion: Mostrar la ventana para agregar nuevos lugares de donación.
    entradas:
    - Ninguna.
    salidas:
    - Ninguna.
    """
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
        """
        funcion:
        Agregar un nuevo lugar de donación a una provincia.
        entradas:
        - Ninguna. Obtiene los datos desde la ventana.
        salidas:
        - Ninguna.
        """
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

# reporte1

def validarSeleccionProvincia(provinciaSeleccionada):
    """
    funcion:
    Valida que el usuario haya seleccionado una provincia.
    entradas:
    - provinciaSeleccionada: cadena con la provincia elegida.
    salidas:
    - True si se seleccionó una provincia.
    - False si no se seleccionó ninguna provincia.
    """
    if not provinciaSeleccionada:
        messagebox.showwarning("Validación", "Debe seleccionar una provincia de la lista.")
        return False
    return True

def reportePorProvinciaAux(pdonadores):
    """
    funcion:
    Despliega la ventana para seleccionar una provincia y generar el reporte correspondiente.
    entradas:
    - pdonadores: matriz con los registros de donadores.
    salidas:
    - Ventana para seleccionar provincia y generar reporte.
    """
    if not pdonadores:
        messagebox.showwarning("Aviso", "No hay donadores registrados en el sistema.")
        return
    ventanaFiltro = tk.Toplevel()
    ventanaFiltro.title("Filtrar por Provincia")
    ventanaFiltro.geometry("350x200")
    ventanaFiltro.resizable(False, False)
    tk.Label(ventanaFiltro, text="Seleccione la provincia a consultar:").pack(pady=15)
    opcionesProvincias = [f"{clave} - {datos[0]}" for clave, datos in provinciasDiccionario.items()]
    comboProvincia = ttk.Combobox(ventanaFiltro, values=opcionesProvincias, state="readonly", width=25)
    comboProvincia.pack(pady=5)
    def ejecutarReporte():
        """
        funcion:
        Obtiene la provincia seleccionada y ejecuta la generación del reporte.
        entradas:
        - Ninguna.
        salidas:
        - Reporte HTML por provincia.
        """
        seleccion = comboProvincia.get()
        if validarSeleccionProvincia(seleccion):
            idProvincia = seleccion.split(" - ")[0]
            procesarReportePorProvinciaHtml(idProvincia, pdonadores, provinciasDiccionario)
            ventanaFiltro.destroy()
    marcoBotones = tk.Frame(ventanaFiltro)
    marcoBotones.pack(pady=15)
    tk.Button(marcoBotones, text="Generar Reporte", command=ejecutarReporte, width=15).pack(side="left", padx=5)
    tk.Button(marcoBotones, text="Regresar", command=ventanaFiltro.destroy, width=15).pack(side="left", padx=5)
    
# reporte 2

def validarSeleccionSangre(tipoSangre):
    """
    funcion:
    Valida que el usuario haya seleccionado un tipo de sangre.
    entradas:
    - tipoSangre: cadena con el tipo de sangre seleccionado.
    salidas:
    - True si existe una selección.
    - False en caso contrario.
    """
    if not tipoSangre:
        messagebox.showwarning("Validación", "Debe seleccionar un tipo de sangre de la lista.")
        return False
    return True

def reportePorSangreAux(pdonadores):
    """
    funcion:
    Despliega la ventana para seleccionar un tipo de sangre y generar el reporte.
    entradas:
    - pdonadores: matriz con los registros de donadores.
    salidas:
    - Ventana para generar el reporte.
    """
    if not pdonadores:
        messagebox.showwarning("Aviso", "No hay donadores registrados en el sistema.")
        return
    ventanaFiltro = tk.Toplevel()
    ventanaFiltro.title("Filtrar por Sangre")
    ventanaFiltro.geometry("300x200")
    ventanaFiltro.resizable(False, False)
    tk.Label(ventanaFiltro, text="Seleccione el tipo de sangre:").pack(pady=15)
    opcionesSangre = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    comboSangre = ttk.Combobox(ventanaFiltro, values=opcionesSangre, state="readonly", width=15)
    comboSangre.pack(pady=5)
    def ejecutarReporte():
        """
        funcion:
        Obtiene el tipo de sangre seleccionado y genera el reporte correspondiente.
        entradas:
        - Ninguna.
        salidas:
        - Reporte HTML por tipo de sangre.
        """
        seleccion = comboSangre.get()
        if validarSeleccionSangre(seleccion):
            procesarReportePorSangreHtml(seleccion, pdonadores, provinciasDiccionario)
            ventanaFiltro.destroy()
    marcoBotones = tk.Frame(ventanaFiltro)
    marcoBotones.pack(pady=15)
    tk.Button(marcoBotones, text="Generar Reporte", command=ejecutarReporte, width=15).pack(side="left", padx=5)
    tk.Button(marcoBotones, text="Regresar", command=ventanaFiltro.destroy, width=15).pack(side="left", padx=5)

# reporte 3
def validarFiltrosTipoSangreProvincia(pseleccionProvincia, pseleccionSangre):
    """
    funcion:
    Valida que se haya seleccionado una provincia y un tipo de sangre.
    entradas:
    - pseleccionProvincia: provincia seleccionada.
    - pseleccionSangre: tipo de sangre seleccionado.
    salidas:
    - True si ambos filtros son válidos.
    - False en caso contrario.
    """
    if not pseleccionProvincia or not pseleccionSangre:
        messagebox.showwarning("Aviso", "Debe seleccionar una provincia y un tipo de sangre para generar el reporte.")
        return False
    return True

def reporteTipoSangreProvinciaAux(pcomboProvincia, pcomboSangre, pdonadores, pprovinciasDiccionario):
    """
    funcion:
    Obtiene los filtros seleccionados y coordina la generación del reporte por provincia y tipo de sangre.
    entradas:
    - pcomboProvincia: combobox de provincias.
    - pcomboSangre: combobox de tipos de sangre.
    - pdonadores: matriz con los registros de donadores.
    - pprovinciasDiccionario: diccionario de provincias.
    salidas:
    - Reporte generado o mensaje de error.
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
    """
    funcion:
    Crea la ventana para seleccionar provincia y tipo de sangre.
    entradas:
    - Ninguna.
    salidas:
    - Ventana gráfica para generar el reporte.
    """
    ventana = tk.Toplevel()
    ventana.title("Reporte por Tipo de Sangre y Provincia")
    ventana.geometry("400x250")
    ventana.resizable(False, False)
    tk.Label(
        ventana,
        text="Reporte por Tipo de Sangre y Provincia",
        font=("Arial", 12, "bold")
    ).pack(pady=(15, 10))
    marco = tk.Frame(ventana)
    marco.pack(padx=20, pady=5)
    tk.Label(marco, text="Provincia:", anchor="w", width=15).grid(row=0, column=0, sticky="w", pady=8)
    comboProvincia = ttk.Combobox(
        marco,
        values=[datos[0] for datos in provinciasDiccionario.values()],
        state="readonly",
        width=25
    )
    comboProvincia.grid(row=0, column=1, sticky="w", pady=8)
    tk.Label(marco, text="Tipo de Sangre:", anchor="w", width=15).grid(row=1, column=0, sticky="w", pady=8)
    comboSangre = ttk.Combobox(
        marco,
        values=tipoSangre,
        state="readonly",
        width=25
    )
    comboSangre.grid(row=1, column=1, sticky="w", pady=8)
    marcoBotones = tk.Frame(ventana)
    marcoBotones.pack(pady=15)
    tk.Button(
        marcoBotones,
        text="Generar Reporte",
        width=15,
        command=lambda: reporteTipoSangreProvinciaAux(
            comboProvincia,
            comboSangre,
            donadores,
            provinciasDiccionario
        )
    ).pack(side="left", padx=5)
    tk.Button(
        marcoBotones,
        text="Regresar",
        width=15,
        command=ventana.destroy
    ).pack(side="left", padx=5)

# reporte 4

def validarMatrizDonadoresReporteGeneral(pdonadores):
    """
    funcion:
    Verifica que existan donadores registrados para generar el reporte general.
    entradas:
    - pdonadores: matriz con los registros de donadores.
    salidas:
    - True si existen registros.
    - False en caso contrario.
    """
    if not pdonadores:
        messagebox.showwarning("Aviso", "No existen donadores registrados en el sistema para generar el reporte.")
        return False
    return True

def reporteGeneralDonadoresAux(pdonadores, pprovinciasDiccionario):
    """
    funcion:
    Coordina la validación y generación del reporte general de donadores.
    entradas:
    - pdonadores: matriz con los registros de donadores.
    - pprovinciasDiccionario: diccionario de provincias.
    salidas:
    - Reporte generado o mensaje de error.
    """
    if not validarMatrizDonadoresReporteGeneral(pdonadores):
        return  
    fueCreadoExitosamente = procesarReporteGeneralDonadoresHtml(pdonadores, pprovinciasDiccionario)
    if fueCreadoExitosamente:
        messagebox.showinfo("Éxito", "Reporte generado")
    else:
        messagebox.showerror("Error", "No se pudo escribir el archivo del reporte general en el disco.")

# reporte 5

def validarMatrizDonadores(pDonadores):
    """
    Funcionalidad:
    Valida que la matriz de donadores exista y contenga registros antes de procesar un reporte.
    Entradas:
    - pDonadores (list): Matriz de donadores registrada en el sistema.
    Salidas:
    - True: Si existen registros en la matriz.
    - False: Si la matriz está vacía o no existe.
    """
    if not pDonadores or len(pDonadores) == 0:
        messagebox.showwarning("Aviso", "No existen donadores registrados en el sistema para procesar.")
        return False
    return True

def reporteMujeresOMinusculasAux(pDonadores):
    """
    Funcionalidad:
    Coordina la validación y generación del reporte de mujeres donadoras O- menores de 45 años.
    Entradas:
    - pDonadores (list): Matriz con los registros de donadores.
    Salidas:
    - Ninguna.
    """
    if not validarMatrizDonadores(pDonadores):
        return
    fueCreadoExitosamente = procesarReporteMujeresOMinusculasHtml(pDonadores)
    if fueCreadoExitosamente:
        messagebox.showinfo("Éxito", "Reporte creado satisfactoriamente")
    else:
        messagebox.showerror("Error", "Reporte no creado.")

# reporte 6

def validarFiltroCompatibilidadDonacion(pTipoSangreSeleccionado):
    """
    Funcionalidad:
    Verifica que el usuario haya seleccionado un tipo de sangre antes de generar el reporte de compatibilidad.
    Entradas:
    - pTipoSangreSeleccionado (str): Tipo de sangre elegido por el usuario.
    Salidas:
    - True: Si existe una selección válida.
    - False: Si no se seleccionó ningún tipo de sangre.
    """
    if not pTipoSangreSeleccionado:
        messagebox.showwarning("Aviso", "Por favor, seleccione un tipo de sangre para continuar.")
        return False
    return True

def reporteCompatibilidadDonacionAux(pDonadores, pProvinciasDiccionario, pTipoSangreTupla):
    """
    Funcionalidad:
    Despliega la ventana de selección y coordina la generación del reporte de compatibilidad de donación.
    Entradas:
    - pDonadores (list): Matriz de donadores registrados.
    - pProvinciasDiccionario (dict): Diccionario de provincias.
    - pTipoSangreTupla (tuple): Tupla con los tipos de sangre disponibles.
    Salidas:
    - Ninguna.
    """
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
        """
        Funcionalidad:
        Ejecuta el proceso de validación y generación del reporte de compatibilidad de donación según el tipo de sangre seleccionado por el usuario.
        Entradas:
        - Ninguna. Utiliza las variables disponibles en el ámbito de la ventana.
        Salidas:
        - Ninguna.
        """
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
    """
    Funcionalidad:
    Valida que el usuario haya seleccionado un tipo de sangre para generar el reporte de compatibilidad de recepción.
    Entradas:
    - pTipoSangreSeleccionado (str): Tipo de sangre seleccionado.
    Salidas:
    - True: Si el tipo de sangre es válido.
    - False: Si no existe selección.
    """
    if not pTipoSangreSeleccionado or pTipoSangreSeleccionado == "":
        messagebox.showerror("Error de Validación", "Por favor, seleccione un tipo de sangre de la lista.")
        return False
    return True

def reporteCompatibilidadRecibirAux(pDonadores, pTipoSangreTupla):
    """
    Funcionalidad:
    Despliega la ventana de selección y coordina la generación del reporte de compatibilidad para recibir sangre.
    Entradas:
    - pDonadores (list): Matriz de donadores registrados.
    - pTipoSangreTupla (tuple): Tupla con los tipos de sangre disponibles.
    Salidas:
    - Ninguna.
    """
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
    """
    Funcionalidad:
    Verifica si existen donadores inactivos dentro de la matriz de registros.
    Entradas:
    - pmatrizDonadores (list): Matriz de donadores registrados.
    Salidas:
    - True: Si existe al menos un donador inactivo.
    - False: Si no existen donadores inactivos.
    """
    if not pmatrizDonadores:
        return False
    for donador in pmatrizDonadores:
        if donador[8] == 0:  
            return True
    return False

# submenu reportes
def submenuReportes(pventanaPadre):
    """
    Funcionalidad:
    Despliega el submenú de reportes y permite acceder a las diferentes opciones de generación de reportes del sistema.
    Entradas:
    - pventanaPadre (Tk/Toplevel): Ventana desde la cual se invoca el submenú.
    Salidas:
    - Ninguna.
    """
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

def menuPrincipal():
    """
    funcion: Mostrar el menú principal del sistema.
    entradas:
    - Ninguna.
    salidas:
    - Ninguna.
    """
    root = tk.Tk()
    root.title("Sistema Banco de Sangre")
    root.geometry("400x420")
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
        text="Actualizar Datos",
        width=25,
        command=lambda: actualizarDonanteAux(donadores)
    ).pack(pady=5)
    tk.Button(
        root,
        text="Generar Donadores",
        width=25,
        command=lambda: generarDonantesAux(donadores)
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
        command=lambda: ventanaDespedida(root)
    ).pack(pady=20)

    root.mainloop()

def ventanaDespedida(root):
    """
    funcion: Mostrar una ventana de despedida por 5 segundos al salir.
    entradas:
    - root: ventana principal del sistema.
    salidas:
    - Ninguna.
    """
    root.destroy()
    ventana = tk.Tk()
    ventana.title("Hasta pronto")
    ventana.geometry("350x150")
    ventana.resizable(False, False)
    tk.Label(
        ventana,
        text="Donar sangre, es donar vida",
        font=("Arial", 16, "bold"),
        fg="red"
    ).pack(expand=True)
    ventana.after(2000, ventana.destroy)
    ventana.mainloop()

#programa principal
donadores = cargarDatosDesdeArchivo()
menuPrincipal()
