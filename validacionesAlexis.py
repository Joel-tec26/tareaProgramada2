baseDatos=[]
from funcionesAlexis import *
import tkinter as tk
from tkinter import messagebox, ttk
from ddlc import *
archivoDonadores = "donadores.dat"
baseDatos=cargarDatosDesdeArchivo()

print(baseDatos)

def validarCantidad(pcantidad):
    try:
        cantidad = int(pcantidad)
        return 0 < cantidad 
    except ValueError:
        return False
    
def actualizarMatrizEnArchivo(matrizGuardar):
    with open(archivoDonadores, "wb") as archivo:
        pickle.dump(matrizGuardar, archivo)
    return



def generarDonantesAux(pbaseDatos):
    def generar():
        cantidad = entradaCantidad.get().strip()
        if not validarCantidad(cantidad):
            messagebox.showwarning("Aviso","debe escribir un valor numerico")
            return pbaseDatos
        for i in generarDonantes(int(cantidad)):
            pbaseDatos.append(i)
        guardarMatrizEnArchivo(pbaseDatos)
        regresar()
    
    def limpiar():
        entradaCantidad.delete(0, tk.END)

    def regresar():
        ventana.destroy()

    ventana = tk.Tk()
    ventana.title("Insertar donador")
    ventana.geometry("550x360")
    tk.Label(ventana, text="Actualizar Donante", font=("Arial", 20)).grid(row=0, column=1, sticky="w", padx=10, pady=5)
    tk.Label(ventana, text="Cantidad de Donantes").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    entradaCantidad = tk.Entry(ventana, width=25)
    entradaCantidad.grid(row=1, column=1, padx=10, pady=5)
    marcoBotones = tk.Frame(ventana)
    marcoBotones.grid(row=8, column=0, columnspan=3, pady=15)
    tk.Button(marcoBotones, text="Generar", command=generar, width=10).pack(side="left", padx=5)
    tk.Button(marcoBotones, text="Limpiar", command=limpiar, width=10).pack(side="left", padx=5)
    tk.Button(marcoBotones, text="Regresar", command=regresar, width=10).pack(side="left", padx=5)
    ventana.mainloop()
    return pbaseDatos

def actualizarDonanteAux(pbaseDatos):
    def actualizar():
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
        # Búsqueda Binaria para ver si existe para poder actualizar
        existe, posicion = buscarDonador(cedula, pbaseDatos)
        if not existe:
            messagebox.showwarning("Aviso", f"La cédula {cedula} no se encuentra registrada en el sistema.")
            return
        confirmacion = messagebox.askyesno("Confirmar acción", f"¿Está seguro de que desea inactivar al donador con cédula {cedula}?")
        if confirmacion:
            nuevoRegistro = [cedula, nombre, fechaNac, tipoSangre, sexo, int(peso), telefono, correo]
            pbaseDatos[posicion]=nuevoRegistro
            actualizarMatrizEnArchivo(pbaseDatos)
            messagebox.showinfo("Información", "Donador actualizado satisfactoriamente.")
            regresar()
        else:
            messagebox.showinfo("Información", "Donador NO actualizado.")    
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
    tk.Button(marcoBotones, text="Regresar", command=regresar, width=10, cursor="hand2").pack(side="left", padx=5)
    ventana.mainloop()
    return pbaseDatos



generarDonantesAux(baseDatos)
print(baseDatos)
baseDatos=actualizarDonanteAux(baseDatos)
print(baseDatos)