import pyodbc
import config_logistica
import funciones_generales

def obtener_nuevo_nro_proceso(sql_server, sql_db, sql_user, sql_pass):
    """
    Obtiene el valor máximo de Nro_Proceso en la tabla y le suma 1.
    Si la tabla está vacía o el valor es NULL, devuelve 1.

    :param sql_server: Servidor SQL Server.
    :param sql_db: Base de datos SQL Server.
    :param sql_user: Usuario de SQL Server.
    :param sql_pass: Contraseña de SQL Server.
    :return: Nuevo valor de Nro_Proceso.
    """
    try:
        # Conexión con SQL Server
        conexion = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={sql_server};DATABASE={sql_db};'
            f'UID={sql_user};PWD={sql_pass}'
        )

        cursor = conexion.cursor()

        # Consulta para obtener el máximo Nro_Proceso
        cursor.execute(f"SELECT ISNULL(MAX(Nro_Proceso), 0) + 1 FROM {config_logistica.tabla_datosexcel}")
        nuevo_nro_proceso = cursor.fetchone()[0]

        return nuevo_nro_proceso

    except Exception as e:
        funciones_generales.log_grabar(f"Error en la consulta: {e} - obtener_nuevo_nro_proceso()", config_logistica.dir_log)
        return None

    finally:
        cursor.close()
        conexion.close()

def insert_datos_excel(sql_server, sql_db, sql_user, sql_pass, nro_proceso,list_entregas):
	"""
	Inserta registros en la tabla intermedia de SQL Server de manera masiva.

	:param sql_server: Servidor SQL Server.
	:param sql_db: Base de datos SQL Server.
	:param sql_user: Usuario de SQL Server.
	:param sql_pass: Contraseña de SQL Server.
	:param nro_proceso: Número de proceso
	:param list_entregas: Lista de diccionarios con los datos de las entregas
	"""
	try:
		# Conexión con SQL Server
		conexion = pyodbc.connect(
			f'DRIVER={{ODBC Driver 17 for SQL Server}};'
			f'SERVER={sql_server};DATABASE={sql_db};'
			f'UID={sql_user};PWD={sql_pass}'
		)

		cursor = conexion.cursor()

		# Filtrar duplicados basados en 'Remito'
		remitos_vistos = set()
		list_entregas_filtrada = []
		for ent in list_entregas:
			remito_valor = funciones_generales.safe_str(funciones_generales.safe_int(ent.get('Remito')))  # Convertir a int y luego a str
			if remito_valor not in remitos_vistos:
				remitos_vistos.add(remito_valor)
				list_entregas_filtrada.append(ent)

		# Listas para inserciones y actualizaciones masivas
		datos_insert = []

		for ent in list_entregas_filtrada:

			# Transformaciones y validaciones
			remito = funciones_generales.safe_str(funciones_generales.safe_int(ent.get('Remito')))  # Convertir a int y luego a str
			cliente = funciones_generales.safe_str(ent.get('Cliente'))
			destinatario = funciones_generales.safe_str(ent.get('Destinatario'))
			domicilio = funciones_generales.safe_str(ent.get('Domicilio'))
			provincia = funciones_generales.safe_str(ent.get('Provincia'))
			ciudad = funciones_generales.safe_str(ent.get('Ciudad'))
			codigo_postal = funciones_generales.safe_str(funciones_generales.safe_int(ent.get('Codigo Postal')))  # Convertir a int y luego a str
			retiro_generada = ent.get('Retiro Generada', None)
			retiro_efectivo = ent.get('Retiro Efectivo', None)
			entrega_efectiva = ent.get('Entrega Efectiva', None)
			tipo_entrega = funciones_generales.safe_str(ent.get('Tipo de Entrega'))
			cantidad_bulto = funciones_generales.safe_int(ent.get('Cantidad de Bulto'))  # Convertir a int

			# Agregar a la lista de inserción
			datos_insert.append((
				remito, cliente, destinatario, domicilio, provincia, ciudad,
				codigo_postal, retiro_generada, retiro_efectivo, entrega_efectiva,
				tipo_entrega, cantidad_bulto
			))

		# Ejecución masiva de INSERT
		if datos_insert:
			sql_insert = f"""
                INSERT INTO {config_logistica.tabla_datosexcel} (
                    Nro_Proceso, Fecha_Proceso, HostName_Proceso, Remito, 
                    Cliente, Destinatario, Domicilio, Provincia, 
                    Ciudad, Codigo_Postal, Orden_Retiro_Generada, Retiro_Efectivo, 
                    Entrega_Efectiva, Tipo_Entrega, Cantidad_Bulto
                )
                VALUES (
                    {nro_proceso}, GETDATE(), HOST_NAME(), ?, 
                    ?, ?, ?, ?, 
                    ?, ?, ?, ?, 
                    ?, ?, ?
                )
            """
			cursor.executemany(sql_insert, datos_insert)

		# Confirmar transacciones
		conexion.commit()

	except Exception as e:
		mensaje_error = f"Error en insert_datos_excel: {e}"
		funciones_generales.log_grabar(mensaje_error, config_logistica.dir_log)
		if 'conexion' in locals():
			conexion.rollback()
		raise  # Relanza la excepción para que la captura `ejecutar_proceso`

	finally:
		if 'cursor' in locals():  # Verifica si cursor existe antes de cerrarlo
			cursor.close()
		if 'conexion' in locals():  # Verifica si conexión existe antes de cerrarla
			conexion.close()

	return list_entregas_filtrada  # Retornar la lista filtrada


def insert_datos_excel_old(sql_server, sql_db, sql_user, sql_pass, nro_proceso,list_entregas):
	"""
	Inserta registros en la tabla intermedia de SQL Server de manera masiva.

	:param sql_server: Servidor SQL Server.
	:param sql_db: Base de datos SQL Server.
	:param sql_user: Usuario de SQL Server.
	:param sql_pass: Contraseña de SQL Server.
	:param nro_proceso: Número de proceso
	:param list_entregas: Lista de diccionarios con los datos de las entregas
	"""
	try:
		# Conexión con SQL Server
		conexion = pyodbc.connect(
			f'DRIVER={{ODBC Driver 17 for SQL Server}};'
			f'SERVER={sql_server};DATABASE={sql_db};'
			f'UID={sql_user};PWD={sql_pass}'
		)

		cursor = conexion.cursor()

		# Filtrar duplicados basados en 'Remito'
		remitos_vistos = set()
		list_entregas_filtrada = []
		for ent in list_entregas:
			remito_valor = funciones_generales.safe_str(funciones_generales.safe_int(ent.get('Remito')))  # Convertir a int y luego a str
			if remito_valor not in remitos_vistos:
				remitos_vistos.add(remito_valor)
				list_entregas_filtrada.append(ent)

		# Listas para inserciones y actualizaciones masivas
		datos_insert = []

		for ent in list_entregas_filtrada:

			# Transformaciones y validaciones
			remito = funciones_generales.safe_str(funciones_generales.safe_int(ent.get('Remito')))  # Convertir a int y luego a str
			cliente = funciones_generales.safe_str(ent.get('Cliente'))
			destinatario = funciones_generales.safe_str(ent.get('Destinatario'))
			domicilio = funciones_generales.safe_str(ent.get('Domicilio'))
			provincia = funciones_generales.safe_str(ent.get('Provincia'))
			ciudad = funciones_generales.safe_str(ent.get('Ciudad'))
			codigo_postal = funciones_generales.safe_str(funciones_generales.safe_int(ent.get('Codigo Postal')))  # Convertir a int y luego a str
			retiro_generada = ent.get('Retiro Generada', None)
			retiro_efectivo = ent.get('Retiro Efectivo', None)
			entrega_efectiva = ent.get('Entrega Efectiva', None)
			tipo_entrega = funciones_generales.safe_str(ent.get('Tipo de Entrega'))
			cantidad_bulto = funciones_generales.safe_int(ent.get('Cantidad de Bulto'))  # Convertir a int

			# Agregar a la lista de inserción
			datos_insert.append((
				remito, cliente, destinatario, domicilio, provincia, ciudad,
				codigo_postal, retiro_generada, retiro_efectivo, entrega_efectiva,
				tipo_entrega, cantidad_bulto
			))

		# Ejecución masiva de INSERT
		if datos_insert:
			sql_insert = f"""
                INSERT INTO {config_logistica.tabla_datosexcel} (
                    Nro_Proceso, Fecha_Proceso, HostName_Proceso, Remito, 
                    Cliente, Destinatario, Domicilio, Provincia, 
                    Ciudad, Codigo_Postal, Orden_Retiro_Generada, Retiro_Efectivo, 
                    Entrega_Efectiva, Tipo_Entrega, Cantidad_Bulto
                )
                VALUES (
                    {nro_proceso}, GETDATE(), HOST_NAME(), ?, 
                    ?, ?, ?, ?, 
                    ?, ?, ?, ?, 
                    ?, ?, ?
                )
            """
			cursor.executemany(sql_insert, datos_insert)

		# Confirmar transacciones
		conexion.commit()

	except Exception as e:
		funciones_generales.log_grabar(f"Error en la operación: {e} - insert_datos_excel()",
		                               config_logistica.dir_log)
		conexion.rollback()

	finally:
		cursor.close()
		conexion.close()

	return list_entregas_filtrada  # Retornar la lista filtrada
