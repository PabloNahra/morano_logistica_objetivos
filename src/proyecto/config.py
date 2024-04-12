# configuracion probando
import pytz
from pathlib import Path
import json

# Levanto las configuraciones del archivo .json
with open('config_minderest.json', 'r') as file:
    # Lee el contenido del archivo JSON
    json_data = json.load(file)

#Defino time zon
timezone_argentina = pytz.timezone(json_data['generales']['timezone'])

# Directorio de Log
# dir_log = Path('C:/mis_entornos/vtex_api_catalogo/src/proyecto/vtex_catalogo_log.txt')
dir_log = Path(json_data['generales']['directorio_log'])
dir_archivo = Path(json_data['generales']['directorio_archivo'])
dir_archivo_historial = Path(json_data['generales']['directorio_archivo_historial'])

# Defino las credenciales del Server SQL de iPoint
sql_server_ipoint = json_data['cred_SQL_ipoint']['sql_server_ipoint']
sql_db_ipoint = json_data['cred_SQL_ipoint']['sql_db_ipoint']
sql_user_ipoint = json_data['cred_SQL_ipoint']['sql_user_ipoint']
sql_pass_ipoint = json_data['cred_SQL_ipoint']['sql_pass_ipoint']

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

# FTP de subida
subir_ftp = json_data['ftp']['subir_ftp']
server_ftp = json_data['ftp']['server_ftp']
port_ftp = json_data['ftp']['port_ftp']
user_ftp = json_data['ftp']['user_ftp']
password_ftp = json_data['ftp']['password_ftp']


# Parametros de negocio
archivo_skus_integrar = json_data['parametros_negocio']['archivo_skus_integrar']
lista_precios_ipoint_id = json_data['parametros_negocio']['lista_precios_ipoint_id']
nombre_archivo_exportar = json_data['parametros_negocio']['nombre_archivo_exportar']
tipo_archivo_exportar = json_data['parametros_negocio']['tipo_archivo_exportar']