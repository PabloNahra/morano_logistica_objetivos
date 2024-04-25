import pyodbc
import config

def ipoint_by_sku_sql(sql_server, sql_db, sql_user, sql_pass, sku=''):
	'''
	Leer datos de distintas vistas y tablas de iPoint a partir de un SKU
	https://stackoverflow.com/questions/16519385/output-pyodbc-cursor-results-as-python-dictionary
	:return:
	Diccionario con los datos del SKU obtenidos de iPoint
	'''

	try:
		# Conecto con SQL
		conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}'
		                          ';SERVER=' + sql_server +
		                          ';DATABASE=' + sql_db +
		                          ';UID=' + sql_user +
		                          ';PWD=' + sql_pass)

		# Consulto los datos del SKU en iPoint
		sku_info_ipoint_categorias = {}

		sql = "SELECT DISTINCT " \
		       "Producto.Codigo_Interno AS ID, " \
		       "ISNULL(Codigo_Barra.Codigo_Barras, '') AS EAN,  " \
		       "ISNULL(Impuesto.Tasa, '') AS VAT, " \
		       "isnull(Valor_Categoria.Valor, '') AS BRAND, " \
		       "Producto.Codigo_Interno AS MPN, " \
		       "ISNULL(SKU_Empresa.ID_SKU_Empresa, '') AS id_ipoint " \
		       "FROM Producto " \
		       "LEFT JOIN SKU ON Producto.ID_Producto = SKU.ID_Producto " \
		       "LEFT JOIN SKU_Empresa ON SKU.ID_SKU = SKU_Empresa.ID_SKU " \
		       "LEFT JOIN Codigo_Barra ON SKU_Empresa.ID_SKU_Empresa = Codigo_Barra.ID_SKU_Empresa AND Codigo_Barra.Es_Interno = 0 " \
		       "LEFT JOIN Producto_Empresa ON SKU_Empresa.ID_Producto_Empresa = Producto_Empresa.ID_Producto_Empresa " \
		       "LEFT JOIN Impuesto ON Producto_Empresa.ID_Impuesto = Impuesto.ID_Impuesto " \
		       "LEFT JOIN SKU_Valores_Asignados ON SKU.ID_SKU  = SKU_Valores_Asignados.ID_SKU " \
		       "LEFT JOIN Valor_Categoria ON SKU_Valores_Asignados.ID_Valor_Categoria = Valor_Categoria.ID_Valor_Categoria " \
		       f"WHERE Producto.Codigo_Interno = '{sku}'"

		cursor = conexion.cursor().execute(sql)
		row = cursor.fetchone()
		if row:
			columns = [column[0] for column in cursor.description]
			sku_info_ipoint_categorias = dict(zip(columns, row))

		# Cierro conexión
		conexion.commit()
		# consulta.close()
		conexion.close()

		# Consulto precios
		# Conecto con SQL
		conexion2 = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}'
		                          ';SERVER=' + sql_server +
		                          ';DATABASE=' + sql_db +
		                          ';UID=' + sql_user +
		                          ';PWD=' + sql_pass)

		# Consulto el precio
		sku_info_ipoint_precio = {}

		'''
		sql = "SELECT " \
		      "ROUND(Precio, 0) AS PRICE, " \
		      "ID_Lista_Precio " \
		      "FROM Precio_SKU " \
		      "WHERE  " \
		      f"ID_SKU_Empresa = {sku_info_ipoint_categorias['id_ipoint']} and " \
		      f"ID_Lista_Precio = {config.lista_precios_ipoint_id}"
		      '''

		sql = (f"SELECT TOP 1 "
		       "ROUND(ISNULL(price_before_offer.Precio, ISNULL(price.Precio, 0)), 0) AS PRICE_BEFORE_OFFER, "
		       "price_before_offer.ID_Lista_Precio AS ID_Lista_Precio_PRICE_BEFORE_OFFER, "
		       "ROUND(ISNULL(price.Precio, ISNULL(price_before_offer.Precio, 0)), 0) AS PRICE, "
		       "ISNULL(price.ID_Lista_Precio, 0) AS ID_Lista_Precio_PRICE "
		       "FROM Precio_SKU as price_before_offer "
		       "left JOIN Precio_SKU as price "
		       "ON "
		       "price_before_offer.ID_SKU_Empresa = price.ID_SKU_Empresa and "
		       f"price.ID_Lista_Precio = {config.lista_precios_ipoint_id_PRICE} "
		       "WHERE "
		       f"price_before_offer.ID_SKU_Empresa = {sku_info_ipoint_categorias['id_ipoint']} and "
		       f"price_before_offer.ID_Lista_Precio = {config.lista_precios_ipoint_id_PRICE_BEFORE_OFFER}")

		cursor = conexion2.cursor().execute(sql)
		row = cursor.fetchone()
		if row:
			columns = [column[0] for column in cursor.description]
			sku_info_ipoint_precio = dict(zip(columns, row))

		# Cierro conexión
		conexion2.commit()
		# consulta.close()
		conexion2.close()

		# Combinando los dos diccionarios
		sku_info_ipoint = sku_info_ipoint_categorias.copy()
		sku_info_ipoint.update(sku_info_ipoint_precio)

		return sku_info_ipoint

	except Exception as e:
		# Si ocurre un error, lanza una nueva excepción con un mensaje personalizado
		raise Exception(f"Error en búsqueda del SKU en iPoint: {e}")
