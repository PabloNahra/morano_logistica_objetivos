# configuracion probando
import pytz
from pathlib import Path
import json

# Levanto las configuraciones del archivo .json
with open('config_logistica.json', 'r') as file:
    # Lee el contenido del archivo JSON
    json_data = json.load(file)

#Defino time zon
timezone_argentina = pytz.timezone(json_data['generales']['timezone'])

# Directorio de Log
# dir_log = Path('C:/mis_entornos/vtex_api_catalogo/src/proyecto/vtex_catalogo_log.txt')
dir_log = Path(json_data['generales']['directorio_log'])


# Defino las credenciales del Server SQL de Bejerman
sql_server_sb = json_data['cred_SQL_bejerman']['sql_server_sb']
sql_db_sb = json_data['cred_SQL_bejerman']['sql_db_sb']
sql_user_sb = json_data['cred_SQL_bejerman']['sql_user_sb']
sql_pass_sb = json_data['cred_SQL_bejerman']['sql_pass_sb']

# Defino las credenciales del Server SQL INTERMEDIO
sql_server_int = json_data['cred_SQL_intermedio']['sql_server_int']
sql_db_int = json_data['cred_SQL_intermedio']['sql_db_int']
sql_user_int = json_data['cred_SQL_intermedio']['sql_user_int']
sql_pass_int = json_data['cred_SQL_intermedio']['sql_pass_int']

# Directorio de red
copiar_direc_red = json_data['directorio_red']['copiar_direc_red']
directorio_red = json_data['directorio_red']['directorio_red']

# Configuracion de envio de mails
email_smtp = json_data['envio_mail']['email_smtp']
email_port = json_data['envio_mail']['email_port']
sender_email_address = json_data['envio_mail']['sender_email_address']
email_password = json_data['envio_mail']['email_password']
mail_from = json_data['envio_mail']['mail_from']
mail_to = json_data['envio_mail']['mail_to']
mail_subject = json_data['envio_mail']['mail_subject']

# Parametros de negocio
dir_lista_entrega = Path(json_data['parametros_negocio']['directorio_lista_entrega'])
archivo_entrega = json_data['parametros_negocio']['archivo_entrega']
tabla_datosexcel = json_data['parametros_negocio']['tabla_datosexcel']
comprobantes_rt = json_data['parametros_negocio']['comprobantes_rt']
dir_archivo_procesado = Path(json_data['parametros_negocio']['dir_archivo_procesado'])
dir_archivo_no_procesado = Path(json_data['parametros_negocio']['dir_archivo_no_procesado'])
dir_archivo_proc_incluye_fecha = json_data['parametros_negocio']['dir_archivo_proc_incluye_fecha']
