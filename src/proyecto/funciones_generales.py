import datetime
import pyodbc
import config
from datetime import datetime as hora
import smtplib
from email.message import EmailMessage
import pandas as pd

def obtener_hora_actual():
    hora_actual = hora.now().time()
    # hora_sin_segundos = hora_actual.replace(minute=0, second=0, microsecond=0)
    hora_sin_segundos = hora_actual.replace(second=0, microsecond=0)
    return hora_sin_segundos

# Inserto registro de proceso actualizado
def log_grabar(texto, dir_log):
    fecha_actual = datetime.datetime.today()
    log = f'{fecha_actual} - Operación: {texto}\n'
    archivo = open(dir_log, 'a')
    archivo.write(log)
    archivo.close()

    return 0

def leer_excel_y_convertir_a_lista(nombre_archivo_excel):

	nombre_archivo = nombre_archivo_excel + ".xlsx"

	try:
		# Leer el archivo Excel
		df = pd.read_excel(nombre_archivo)

		# Inicializar una lista para almacenar los diccionarios
		lista_resultante = []

		# Iterar sobre las filas del DataFrame
		for indice, fila in df.iterrows():
			# Convertir cada fila a un diccionario
			diccionario = fila.to_dict()

			# Agregar el diccionario a la lista
			lista_resultante.append(diccionario)

		# Devolver la lista de diccionarios
		return lista_resultante

	except FileNotFoundError:
		print(f"Error: No se pudo encontrar el archivo {nombre_archivo}")
		return None
	except Exception as e:
		print(f"Error: {e}")
		return None
