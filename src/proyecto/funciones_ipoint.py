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

	# Consulto los datos del SKU en iPoint
	sku_info_ipoint_categorias = {}

	sql = "SELECT " \
	      "Codigo_Interno AS ID, " \
	      "Codigo_Barras AS EAN, " \
	      "Impuesto_Tasa AS VAT, " \
	      "Val_Cat_PRD_VALOR AS BRAND, " \
	      "Codigo_Interno AS MPN, " \
	      "ID_SKU_Empresa AS id_ipoint " \
	      "FROM ALL_SKU_INFO_CON_CATEGORIAS " \
	      "WHERE " \
	      f"Codigo_Interno = '{sku}' AND " \
	      "Codigo_Interno <> Codigo_Barras AND " \
	      "Val_Cat_PRD_ID_CAT_PROD = 3"

	cursor = conexion.cursor().execute(sql)
	row = cursor.fetchone()
	if row:
		columns = [column[0] for column in cursor.description]
		sku_info_ipoint_categorias = dict(zip(columns, row))

	# Consulto el precio
	sku_info_ipoint_precio = {}

	sql = "SELECT " \
	      "Precio AS PRICE, " \
	      "ID_Lista_Precio " \
	      "FROM Precio_SKU " \
	      "WHERE  " \
	      f"ID_SKU_Empresa = {sku_info_ipoint_categorias['id_ipoint']} and " \
	      f"ID_Lista_Precio = {config.lista_precios_ipoint_id}"

	cursor = conexion.cursor().execute(sql)
	row = cursor.fetchone()
	if row:
		columns = [column[0] for column in cursor.description]
		sku_info_ipoint_precio = dict(zip(columns, row))

	# Combinando los dos diccionarios
	sku_info_ipoint = sku_info_ipoint_categorias.copy()
	sku_info_ipoint.update(sku_info_ipoint_precio)

	# Cierro conexión
	conexion.commit()
	# consulta.close()
	conexion.close()

	return sku_info_ipoint

'''
info_sku_ipoint = ipoint_by_sku_sql(sql_server=config.sql_server_ipoint,
                             sql_db=config.sql_db_ipoint,
                             sql_user=config.sql_user_ipoint,
                             sql_pass=config.sql_pass_ipoint,
                             sku='SWSUOP101')

print("info_sku_ipoint")
print(info_sku_ipoint)'''
