# configuracion probando
import pytz
from pathlib import Path
import json
from cryptography.fernet import Fernet

# Clave de encriptación con fernet
key_generada = "vCpxjxZ3RiFHUI6GDOozI-NXAebX1a8r2GnjVBBifnI=".encode()
fernet = Fernet(key_generada)

# Levanto las configuraciones del archivo .json
with open('config_logist_obj.json', 'r') as file:
    # Lee el contenido del archivo JSON
    json_data = json.load(file)

#Defino time zon
timezone_argentina = pytz.timezone(json_data['generales']['timezone'])

# Directorio de Log
# dir_log = Path('C:/mis_entornos/vtex_api_catalogo/src/proyecto/vtex_catalogo_log.txt')
dir_log = Path(json_data['generales']['directorio_log'])


# Defino las credenciales del Server SQL de Bejerman
# sql_server_sb = json_data['cred_SQL_bejerman']['sql_server_sb']
sql_server_sb_encrypted_password = json_data['cred_SQL_bejerman']['sql_server_sb'].encode()
sql_server_sb = fernet.decrypt(sql_server_sb_encrypted_password).decode()

sql_db_sb = json_data['cred_SQL_bejerman']['sql_db_sb']
# sql_user_sb = json_data['cred_SQL_bejerman']['sql_user_sb']
sql_user_sb_encrypted_password = json_data['cred_SQL_bejerman']['sql_user_sb'].encode()
sql_user_sb = fernet.decrypt(sql_user_sb_encrypted_password).decode()


# sql_pass_sb = json_data['cred_SQL_bejerman']['sql_pass_sb']
sql_pass_sb_encrypted_password = json_data['cred_SQL_bejerman']['sql_pass_sb'].encode()
sql_pass_sb = fernet.decrypt(sql_pass_sb_encrypted_password).decode()


# Defino las credenciales del Server SQL INTERMEDIO
# sql_server_int = json_data['cred_SQL_intermedio']['sql_server_int']
sql_server_int_encrypted_password = json_data['cred_SQL_intermedio']['sql_server_int'].encode()
sql_server_int = fernet.decrypt(sql_server_int_encrypted_password).decode()

sql_db_int = json_data['cred_SQL_intermedio']['sql_db_int']

# sql_user_int = json_data['cred_SQL_intermedio']['sql_user_int']
sql_user_int_encrypted_password = json_data['cred_SQL_intermedio']['sql_user_int'].encode()
sql_user_int = fernet.decrypt(sql_user_int_encrypted_password).decode()

# sql_pass_int = json_data['cred_SQL_intermedio']['sql_pass_int']
sql_pass_int_encrypted_password = json_data['cred_SQL_intermedio']['sql_pass_int'].encode()
sql_pass_int = fernet.decrypt(sql_pass_int_encrypted_password).decode()

# Configuracion de envio de mails
email_smtp = json_data['envio_mail']['email_smtp']
email_port = json_data['envio_mail']['email_port']
sender_email_address = json_data['envio_mail']['sender_email_address']

# email_password = json_data['envio_mail']['email_password']
email_password_encrypted_password = json_data['envio_mail']['email_password'].encode()
email_password = fernet.decrypt(email_password_encrypted_password).decode()

mail_from = json_data['envio_mail']['mail_from']
mail_to = json_data['envio_mail']['mail_to']
mail_subject = json_data['envio_mail']['mail_subject']

# Parametros de negocio
tabla_datosexcel = json_data['parametros_negocio']['tabla_datosexcel']
dir_planilla_objetivos = Path(json_data['parametros_negocio']['directorio_planilla_objetivos'])
planilla_objetivos = json_data['parametros_negocio']['planilla_objetivos']
tareas_permitidas = json_data['parametros_negocio']['tareas_permitidas']
tipos_tareas_permitidas = json_data['parametros_negocio']['tipos_tareas_permitidas']
dir_archivo_procesado = Path(json_data['parametros_negocio']['dir_archivo_procesado'])
dir_archivo_no_procesado = Path(json_data['parametros_negocio']['dir_archivo_no_procesado'])
dir_items_no_procesados = Path(json_data['parametros_negocio']['dir_items_no_procesados'])
items_no_proc_orden_campos = json_data['parametros_negocio']['items_no_proc_orden_campos']
dir_archivo_proc_incluye_fecha = json_data['parametros_negocio']['dir_archivo_proc_incluye_fecha']

comprobantes_rt = json_data['parametros_negocio']['comprobantes_rt']
dias_hacia_atras = json_data['parametros_negocio']['dias_hacia_atras']

