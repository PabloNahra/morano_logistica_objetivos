import datetime
from datetime import datetime as hora
import smtplib
from email.message import EmailMessage
import pandas as pd
import os
import math
import config_logist_obj
import shutil
import datetime

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

def leer_excel_y_convertir_a_lista(nombre_archivo_excel, titulo=0, datos=1):
    """
    Lee un archivo Excel y lo convierte en una lista de diccionarios, deteniéndose en la primera fila completamente vacía.

    :param nombre_archivo_excel: Nombre del archivo Excel (sin extensión)
    :param titulo: Número de fila donde se encuentran los títulos (base 0)
    :param datos: Número de fila donde comienzan los datos (base 0)
    :return: Lista de diccionarios con los datos del Excel o None en caso de error.
    """
    # nombre_archivo = nombre_archivo_excel + ".xlsx"
    nombre_archivo = nombre_archivo_excel

    try:
        # Leer el archivo Excel con la fila de títulos y saltando las filas innecesarias
        df = pd.read_excel(nombre_archivo, header=titulo, skiprows=datos)

        # Convertir el DataFrame en una lista de diccionarios, pero solo hasta la primera fila vacía
        lista_resultante = []
        for _, row in df.iterrows():
            if row.isnull().all():  # Si TODAS las columnas de la fila están vacías, detener la lectura
                break
            lista_resultante.append(row.to_dict())

        return lista_resultante

    except FileNotFoundError:
        log_grabar(f"Error: No se pudo encontrar el archivo {nombre_archivo} - leer_excel_y_convertir_a_lista()",
                   config_logist_obj.dir_log)
        return None
    except Exception as e:
        log_grabar(f"Error: {e} - leer_excel_y_convertir_a_lista()",
                   config_logist_obj.dir_log)
        return None



def exportacion_archivo(lista_diccionarios, nombre_archivo,
                        campo_orden=None, incl_fecha=False,
                        tipo_archivo='excel', directorio=None,
                        user=None, password=None, server=None, share=None,
                        orden_campos=None):
    '''
    :param lista_diccionarios: Cada diccionario es un registro
    :param nombre_archivo: Nombre al exportar el archivo
    :param campo_orden: Campo por el que se ordenarán los registros
    :param incl_fecha: Si el nombre del archivo va a incluir o no la fecha de generación del mismo
    :param tipo_archivo: 'excel' o 'csv'
    :param orden_campos: Lista con los nombres de los campos para ordenar las columnas en la exportación
    :return: Ruta del archivo exportado
    '''

    # Crear un DataFrame a partir de la lista de diccionarios
    df = pd.DataFrame(lista_diccionarios)

    # Ordenar la lista si se proporciona un campo de orden
    if campo_orden:
        if campo_orden in df.columns:
            df = df.sort_values(by=campo_orden)
    else:
        # Si campo_orden es None, ordenar por la primera clave del primer diccionario
        if lista_diccionarios:
            primer_diccionario = lista_diccionarios[0]
            primer_clave = list(primer_diccionario.keys())[0]
            df = df.sort_values(by=primer_clave)

    # Reordenar columnas según orden_campos si está definido
    if orden_campos:
        orden_campos_lower = [campo.lower() for campo in orden_campos]  # Convertimos a minúsculas
        columnas_actuales = list(df.columns)

        # Separar las columnas que están en orden_campos y las que no
        columnas_ordenadas = [col for col in columnas_actuales if col.lower() in orden_campos_lower]
        columnas_restantes = [col for col in columnas_actuales if col.lower() not in orden_campos_lower]

        # Reordenar DataFrame con las columnas ordenadas primero
        df = df[columnas_ordenadas + columnas_restantes]

    # Agregar fecha y hora al nombre del archivo si incl_fecha es True
    nombre_archivo_con_fecha = nombre_archivo
    if incl_fecha:
        fecha_hora_actual = hora.now().strftime('%Y_%m_%d_%H_%M_%S')
        nombre_archivo_con_fecha = f"{nombre_archivo}_{fecha_hora_actual}"

    # Determinar el directorio de destino
    if directorio:
        if not os.path.exists(directorio):
            os.makedirs(directorio)
        archivo = os.path.join(directorio, nombre_archivo_con_fecha)
    else:
        archivo = nombre_archivo_con_fecha

    # Exportar el DataFrame a un archivo CSV o Excel según el tipo de archivo especificado
    if tipo_archivo == 'csv':
        archivo += ".csv"
        df.to_csv(archivo, index=False, sep=';')
    elif tipo_archivo == 'excel':
        archivo += ".xlsx"
        df.to_excel(archivo, index=False)
    else:
        raise ValueError("Tipo de archivo no válido. Debe ser 'csv' o 'excel'.")

    return archivo


def exportacion_archivo_OLD(lista_diccionarios, nombre_archivo,
                        campo_orden=None, incl_fecha=False,
                        tipo_archivo='excel', directorio=None,
                        user=None, password=None, server=None, share=None):
	'''
	:param lista_diccionarios: Cada diccionario es un registro
	:param nombre_archivo: Nombre al exportar el archivo
	:param campo_orden: Campo por el que se ordenarán los registros
	:param incl_fecha: Si el nombre del archivo va a incluir o no la fecha de generacion del mismo
	:param tipo_archivo: 'excel' o 'csv'
	:return:
	'''

	# Crear un DataFrame a partir de la lista de diccionarios
	df = pd.DataFrame(lista_diccionarios)

	# Ordenar la lista si se proporciona un campo de orden
	if campo_orden:
		if campo_orden in df.columns:
			df = df.sort_values(by=campo_orden)
	else:
		# Si campo_orden es None, ordenar por la primera clave del primer diccionario
		if lista_diccionarios:
			primer_diccionario = lista_diccionarios[0]
			primer_clave = list(primer_diccionario.keys())[0]
			df = df.sort_values(by=primer_clave)

	# Agregar fecha y hora al nombre del archivo si incl_fecha es True
	nombre_archivo_con_fecha = nombre_archivo
	if incl_fecha:
		fecha_hora_actual = hora.now().strftime('%Y_%m_%d_%H_%M_%S')
		nombre_archivo_con_fecha = f"{nombre_archivo}_{fecha_hora_actual}"

	# Determinar el directorio de destino
	if directorio:
		if not os.path.exists(directorio):
			os.makedirs(directorio)
		archivo = os.path.join(directorio, nombre_archivo_con_fecha)
	else:
		archivo = nombre_archivo_con_fecha

	# Exportar el DataFrame a un archivo CSV o Excel según el tipo de archivo especificado
	if tipo_archivo == 'csv':
		archivo += ".csv"
		df.to_csv(archivo, index=False, sep=';')
	elif tipo_archivo == 'excel':
		archivo += ".xlsx"
		df.to_excel(archivo, index=False)
	else:
		raise ValueError("Tipo de archivo no válido. Debe ser 'csv' o 'excel'.")

	return archivo

def envio_mail(mail_from, mail_to, mail_subject, mail_attachment, mail_content):
	'''
	Envio de mail con o sin adjunto
	:return:
	'''
	# crear un objeto de tipo mensaje de email
	message = EmailMessage()

	# Configurar cabecera del mail
	message['Subject'] = mail_subject
	message['From'] = mail_from
	message['To'] = mail_to

	# configurar cuerpo del mensaje
	message.set_content(mail_content)

	# tomar el archivo adjunto
	if mail_attachment and len(mail_attachment) > 0:
		with open(f"{mail_attachment}", "rb") as f:
			message.add_attachment(
				f.read(),
				filename=f"{mail_attachment}",
				maintype="application",
				subtype="vnd.ms-excel"
			)

	# configurar smtp server y port
	email_smtp = config_logistica
	server = smtplib.SMTP(email_smtp, '587')

	# Identify this client to the SMTP server
	server.ehlo()

	# Secure the SMTP connection
	server.starttls()

	# loguearse en el mail
	sender_email_address = config_logistica.email_smtp # "noreply@satrendy.net"
	email_password = config_logistica.email_password # "Swatch2021%"
	server.login(sender_email_address, email_password)

	# Send email
	server.send_message(message)
	# Close connection to server
	server.quit()

	return

def safe_int(value, default=0):
    """Convierte a int asegurándose de manejar NaN, None y valores inválidos."""
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return default
    return int(value)

def safe_str(value, default=""):
    """Convierte a string asegurándose de manejar None y NaN."""
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return default
    return str(value).strip()




def mover_archivo(directorio_origen=None, nombre_archivo_origen="Entregas", extension_origen="xlsx",
                  directorio_exportar=None,
                  incluye_fecha=1):
	# Si no se especifica directorio de origen, usar el del ejecutable
	if directorio_origen is None:
		directorio_origen = os.getcwd()

	# Construir la ruta completa del archivo de origen
	archivo_origen = os.path.join(directorio_origen, f"{nombre_archivo_origen}.{extension_origen}")

	# Verificar si el archivo existe
	if not os.path.exists(archivo_origen):
		# print(f"El archivo {archivo_origen} no existe.")
		log_grabar(f"El archivo {archivo_origen} no existe - mover_archivo()",
		           config_logistica.dir_log)
		return False

	# Si no se especifica directorio de origen, usar el del ejecutable
	if directorio_exportar is None:
		directorio_exportar = os.path.join(os.getcwd(), "Procesados")

	# Asegurar que el directorio de exportación existe
	if not os.path.exists(directorio_exportar):
		os.makedirs(directorio_exportar)

	# Construir el nuevo nombre del archivo
	if incluye_fecha:
		fecha_actual = datetime.datetime.now().strftime("_%Y%m%d_%H%M%S")
		nombre_archivo_destino = f"{nombre_archivo_origen}{fecha_actual}.{extension_origen}"
	else:
		nombre_archivo_destino = f"{nombre_archivo_origen}.{extension_origen}"

	# Construir la ruta completa del archivo de destino
	archivo_destino = os.path.join(directorio_exportar, nombre_archivo_destino)

	# Mover el archivo
	try:
		shutil.move(archivo_origen, archivo_destino)
		# print(f"rchivo movido a: {archivo_destino}")
		log_grabar(f"Archivo movido a: {archivo_destino} - mover_archivo()",
		           config_logist_obj.dir_log)
		return True
	except Exception as e:
		log_grabar(f"Error al mover el archivo: {e} - mover_archivo()", config_logistica.dir_log)
		return False
