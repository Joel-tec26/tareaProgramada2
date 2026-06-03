# creado por: Alexis Torres y Joel Porras
# fecha de creacion: 2/06/2026
# ultima modificación: 
# version: 3.14

# importacion de librerias
import pickle

# definicion de funciones
archivoDonadores = "donadores.dat"

def cargarDatosDesdeArchivo():
    """
   función:Carga la lista de donadores almacenada en el archivo binario.
    Entradas:
        No recibe parámetros.
    Salidas:
        list: Lista de donadores cargada desde el archivo.
              Retorna una lista vacía si el archivo no existe
              o si ocurre un error de lectura.
    """
    try:
        with open(archivoDonadores, "rb") as archivo:
            return pickle.load(archivo)
    except FileNotFoundError:
        return []
    except (pickle.PickleError, EOFError):
        return []

def guardarMatrizEnArchivo(matrizGuardar):
    """
    funcion: Guardar la matriz de donadores en un archivo binario.
    entradas:
    - matrizGuardar: matriz con la información de los donadores.
    salidas:
    - Ninguna.
    """
    with open(archivoDonadores, "wb") as archivo:
        pickle.dump(matrizGuardar, archivo)
    return