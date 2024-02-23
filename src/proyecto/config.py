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

# Defino las credenciales del Server SQL de integracion
sql_server_int = json_data['cred_SQL_integracion']['sql_server_int']
sql_db_int = json_data['cred_SQL_integracion']['sql_db_int']
sql_user_int = json_data['cred_SQL_integracion']['sql_user_int']
sql_pass_int = json_data['cred_SQL_integracion']['sql_pass_int']

# Defino las credenciales del Server SQL de iPoint
sql_server_ipoint = json_data['cred_SQL_ipoint']['sql_server_ipoint']
sql_db_ipoint = json_data['cred_SQL_ipoint']['sql_db_ipoint']
sql_user_ipoint = json_data['cred_SQL_ipoint']['sql_user_ipoint']
sql_pass_ipoint = json_data['cred_SQL_ipoint']['sql_pass_ipoint']

# Defino las credenciales del Server SQL DataWareHouse
sql_server_dw = json_data['cred_SQL_dw']['sql_server_dw']
sql_db_dw = json_data['cred_SQL_dw']['sql_db_dw']
sql_user_dw =  json_data['cred_SQL_dw']['sql_user_dw']
sql_pass_dw = json_data['cred_SQL_dw']['sql_pass_dw']

# Configuracion de envio de mails
email_smtp = json_data['envio_mail']['email_smtp']
email_port = json_data['envio_mail']['email_port']
sender_email_address = json_data['envio_mail']['sender_email_address']
email_password = json_data['envio_mail']['email_password']
mail_from = json_data['envio_mail']['mail_from']
mail_to = json_data['envio_mail']['mail_to']
mail_subject = json_data['envio_mail']['mail_subject']