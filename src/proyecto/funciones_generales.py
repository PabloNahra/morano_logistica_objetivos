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
