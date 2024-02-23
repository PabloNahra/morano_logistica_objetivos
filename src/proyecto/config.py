# configuracion probando
import pytz
from pathlib import Path
import json

# Levanto las configuraciones del archivo .json
with open('config.json', 'r') as file:
    # Lee el contenido del archivo JSON
    json_data = json.load(file)

#Defino time zon
timezone_argentina = pytz.timezone(json_data['generales']['timezone'])

# Directorio de Log
# dir_log = Path('C:/mis_entornos/vtex_api_catalogo/src/proyecto/vtex_catalogo_log.txt')
dir_log = Path(json_data['generales']['directorio_log'])

# Defino las credenciales del Server SQL de iPoint
sql_server_ipoint = json_data['cred_SQL_ipoint']['sql_server_ipoint']
sql_db_ipoint = json_data['cred_SQL_ipoint']['sql_db_ipoint']
sql_user_ipoint = json_data['cred_SQL_ipoint']['sql_user_ipoint']
sql_pass_ipoint = json_data['cred_SQL_ipoint']['sql_pass_ipoint']

# Configuracion de envio de mails
email_smtp = json_data['envio_mail']['email_smtp']
email_port = json_data['envio_mail']['email_port']
sender_email_address = json_data['envio_mail']['sender_email_address']
email_password = json_data['envio_mail']['email_password']
mail_from = json_data['envio_mail']['mail_from']
mail_to = json_data['envio_mail']['mail_to']
mail_subject = json_data['envio_mail']['mail_subject']

# Parametros de negocio
lista_precios_ipoint_id = json_data['parametros_negocio']['lista_precios_ipoint_id']