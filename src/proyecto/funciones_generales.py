import datetime
import pyodbc
import config
from datetime import datetime as hora
import smtplib
from email.message import EmailMessage
import pandas as pd
import os

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

def exportacion_excel_old(lista_diccionarios, nombre_archivo_excel, campo_orden=None,incl_fecha=0):
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

	# Agregar fecha y hora al nombre del archivo si incl_fecha es 1
	if incl_fecha == 1:
		fecha_hora_actual = hora.now().strftime('%Y_%m_%d_%H_%M_%S')
		archivo = f"{nombre_archivo_excel}_{fecha_hora_actual}.xlsx"
	else:
		archivo = f"{nombre_archivo_excel}.xlsx"

	# Exportar el DataFrame a un archivo Excel
	df.to_excel(archivo, index=False)

	return

def exportacion_archivo(lista_diccionarios, nombre_archivo,
                        campo_orden=None, incl_fecha=False,
                        tipo_archivo='excel', directorio=None):
	'''
	:param lista_diccionarios:
	:param nombre_archivo:
	:param campo_orden:
	:param incl_fecha:
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
		df.to_csv(archivo, index=False)
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
	email_smtp = 'mail.satrendy.net'
	server = smtplib.SMTP(email_smtp, '587')

	# Identify this client to the SMTP server
	server.ehlo()

	# Secure the SMTP connection
	server.starttls()

	# loguearse en el mail
	sender_email_address = "noreply@satrendy.net"
	email_password = "Swatch2021%"
	server.login(sender_email_address, email_password)

	# Send email
	server.send_message(message)
	# Close connection to server
	server.quit()

	return
