import pyodbc
import config_logist_obj
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
        cursor.execute(f"SELECT ISNULL(MAX(Nro_Proceso), 0) + 1 FROM {config_logist_obj.tabla_datosexcel}")
        nuevo_nro_proceso = cursor.fetchone()[0]

        return nuevo_nro_proceso

    except Exception as e:
        funciones_generales.log_grabar(f"Error en la consulta: {e} - obtener_nuevo_nro_proceso()",
                                       config_logist_obj.dir_log)
        return None

    finally:
        cursor.close()
        conexion.close()

def insert_datos_excel(sql_server, sql_db, sql_user, sql_pass,
                       nro_proceso,
                       list_objetivos,
                       obj_tareas_perm,
                       obj_tipos_tareas_perm):
	"""
	Inserta registros en la tabla de objetivos de SQL Server de manera masiva.

	:param sql_server: Servidor SQL Server.
	:param sql_db: Base de datos SQL Server.
	:param sql_user: Usuario de SQL Server.
	:param sql_pass: Contraseña de SQL Server.
	:param nro_proceso: Número de proceso
	:param list_objetivos: Lista de diccionarios con los datos de las entregas
	:param obj_tareas_perm: Listado de tareas de objetivos permitidas (Valores de la columna TAREA)
	:param obj_tipos_tareas_perm: Listado de tipos de tareas de objetivos permitidas (Valores de la columna TIPO_TAREA)

	:return list_entregas_filtrada: Lista de diccionarios con los datos de las entregas que se deben
	integrar en principio
	:return list_entregas_no_integrar: Lista de diccionarios con los datos de las entregas que no se integran por
	diversos controles como número duplicado o empresa no permitida
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
		objetivos_procesados = set()
		list_objetivos_filtrada = []
		list_objetivos_no_integrar = []
		obj_tareas_perm_lower = {tp.lower() for tp in obj_tareas_perm}
		obj_tipos_tareas_perm_lower = {tp.lower() for tp in obj_tipos_tareas_perm}
		for objetivo in list_objetivos:
			# remito_valor = funciones_generales.safe_str(funciones_generales.safe_int(objetivo.get('Remito')))  # Convertir a int y luego a str
			objetivo_id = (funciones_generales.safe_str(objetivo.get('FECHA'))
			            + "-" + funciones_generales.safe_str(objetivo.get('TAREA'))
			            + "-" + funciones_generales.safe_str(objetivo.get('TIPO_TAREA')))

			tarea = funciones_generales.safe_str(objetivo.get('TAREA')).lower()
			tipo_tarea = funciones_generales.safe_str(objetivo.get('TIPO_TAREA')).lower()
			# Si repite la numercación no lo integro
			if objetivo_id in objetivos_procesados:
				objetivo['MOTIVO'] = 'DUPLICADO'
				list_objetivos_no_integrar.append(objetivo)
			# Si el transporte no está dentro de los permitidos NO lo integro
			elif tarea not in obj_tareas_perm_lower:
				objetivo['MOTIVO'] = 'TAREA NO PERMITIDA'
				list_objetivos_no_integrar.append(objetivo)
			elif tipo_tarea not in obj_tipos_tareas_perm_lower:
				objetivo['MOTIVO'] = 'TIPO_TAREA NO PERMITIDA'
				list_objetivos_no_integrar.append(objetivo)
			else:
				objetivos_procesados.add(objetivo_id)
				list_objetivos_filtrada.append(objetivo)


		# Listas para inserciones y actualizaciones masivas
		datos_insert = []

		for obj in list_objetivos_filtrada:

			# Transformaciones y validaciones
			fecha = obj.get('FECHA', None)
			tarea = funciones_generales.safe_str(obj.get('TAREA'))
			tipo_tarea = funciones_generales.safe_str(obj.get('TIPO_TAREA'))
			objetivo = funciones_generales.safe_int(obj.get('OBJETIVO'))  # Convertir a int

			'''
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
			'''

			# Agregar a la lista de inserción
			datos_insert.append((
				fecha, tarea, tipo_tarea, objetivo
			))

		# Ejecución masiva de INSERT
		if datos_insert:

			sql_upsert = f"""
			    MERGE INTO {config_logist_obj.tabla_datosexcel} AS target
			    USING (VALUES (?, ?, ?, ?)) AS source (Fecha, Tarea, Tipo_Tarea, Objetivo)
			    ON target.Fecha = source.Fecha AND target.Tarea = source.Tarea
			    AND target.Tipo_Tarea = source.Tipo_Tarea
			    WHEN MATCHED THEN
			        UPDATE SET 
			            Objetivo = source.Objetivo,
			            Nro_Proceso = {nro_proceso},
			            Fecha_Proceso = GETDATE(),
			            HostName_Proceso = HOST_NAME()
			    WHEN NOT MATCHED THEN
			        INSERT (Nro_Proceso, Fecha_Proceso, HostName_Proceso, Fecha, Tarea, Tipo_Tarea, Objetivo)
			        VALUES ({nro_proceso}, GETDATE(), HOST_NAME(), 
			        source.Fecha, source.Tarea, 
			        source.Tipo_Tarea, source.Objetivo);
			"""


			cursor.executemany(sql_upsert, datos_insert)
		# Confirmar transacciones
		conexion.commit()

	except Exception as e:
		mensaje_error = f"Error en insert_datos_excel: {e}"
		funciones_generales.log_grabar(mensaje_error, config_logist_obj.dir_log)
		if 'conexion' in locals():
			conexion.rollback()
		raise  # Relanza la excepción para que la captura `ejecutar_proceso`

	finally:
		if 'cursor' in locals():  # Verifica si cursor existe antes de cerrarlo
			cursor.close()
		if 'conexion' in locals():  # Verifica si conexión existe antes de cerrarla
			conexion.close()

	return list_objetivos_filtrada, list_objetivos_no_integrar


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
