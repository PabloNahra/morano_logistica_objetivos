import pyodbc
import config


def ipoint_by_sku_sql(sql_server, sql_db, sql_user, sql_pass, sku=''):
	'''
	Leer datos de distintas vistas y tablas de iPoint a partir de un SKU
	https://stackoverflow.com/questions/16519385/output-pyodbc-cursor-results-as-python-dictionary
	:return:
	Diccionario con los datos del SKU obtenidos de iPoint
	'''
	# Conecto con SQL
	conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}'
	                          ';SERVER=' + sql_server +
	                          ';DATABASE=' + sql_db +
	                          ';UID=' + sql_user +
	                          ';PWD=' + sql_pass)

	# Consulto el stock de Nodum y ya realizo la conversion de los nombres
	sku_info_ipoint = []
	consulta = conexion.cursor()

	sql = "SELECT 'PRUEBA'"

	cursor = conexion.cursor().execute(sql)
	columns = [column[0] for column in cursor.description]
	for row in cursor.fetchall():
		sku_info_ipoint.append(dict(zip(columns, row)))
	# Cierro conexión
	conexion.commit()
	consulta.close()
	conexion.close()

	return sku_info_ipoint



info_sku_ipoint = ipoint_by_sku_sql(sql_server=config.sql_server_ipoint,
                             sql_db=config.sql_db_ipoint,
                             sql_user=config.sql_user_ipoint,
                             sql_pass=config.sql_pass_ipoint,
                             sku='kit-gm00002')
print(info_sku_ipoint)
print("info_sku_ipoint")