import config_logistica,funciones_generales
import pyodbc


def actualizar_datos_adicionales_sb(sql_server, sql_db, sql_user, sql_pass, list_entregas_filt):
	"""
	Realiza un INSERT o UPDATE en la tabla DtsSegCabV.

	:param sql_server: Servidor SQL Server.
	:param sql_db: Base de datos SQL Server.
	:param sql_user: Usuario de SQL Server.
	:param sql_pass: Contraseña de SQL Server.
	:param list_entregas_filt: Lista de diccionarios con los datos de las entregas.
	"""
	try:
		# Conexión con SQL Server
		conexion = pyodbc.connect(
			f'DRIVER={{ODBC Driver 17 for SQL Server}};'
			f'SERVER={sql_server};DATABASE={sql_db};'
			f'UID={sql_user};PWD={sql_pass}'
		)
		cursor = conexion.cursor()

		# Obtener scv_id para cada remito
		for ent in list_entregas_filt:
			remito_padded = funciones_generales.safe_str(funciones_generales.safe_int(ent.get('Remito'))).zfill(8)  # RIGHT( "00000000" & remito, 8)
			# cursor.execute("SELECT scv_id FROM SegTiposV WHERE spv_nro = ?", remito_padded)
			cursor.execute(f"SELECT TOP 1 spvscv_id, spvemp_codigo, spvsuc_cod  "
			               "FROM SegTiposV WHERE spv_nro = ? "
			               f"AND spvtco_Cod IN {config_logistica.comprobantes_rt} "
			               "ORDER BY spvscv_id desc", remito_padded)
			row = cursor.fetchone()
			if row:
				ent['scv_id'] = row.spvscv_id
				ent['emp_codigo'] = row.spvemp_codigo
				ent['suc_cod'] = row.spvsuc_cod
			else:
				ent['scv_id'] = None  # No se encontró un ID, omitir este registro

		# Filtrar registros válidos
		list_entregas_actualizar = [ent for ent in list_entregas_filt if ent['scv_id'] is not None]

		# Listas para inserciones y actualizaciones
		datos_upsert = []
		for ent in list_entregas_actualizar:
			datos_upsert.append((
				ent['scv_id'],
				ent['emp_codigo'],
				ent['suc_cod'],
				ent.get('Entrega Efectiva'),
				ent.get('Retiro Efectivo'),
				ent.get('Retiro Generada')
			))

		# Sentencia MERGE para hacer INSERT o UPDATE
		sql_merge = f'''
            MERGE INTO DtsSegCabV AS target
            USING (VALUES (?, ?, ?, ?, ?, ?)) AS source 
            (scv_id, scvemp_Codigo, scvsuc_Cod,
            Dscv_TrEntregaEfec, Dscv_TrRetiroEfec, Dscv_TrRetiroGenerado)
            ON target.scv_id = source.scv_id
            WHEN MATCHED THEN 
                UPDATE SET 
                    Dscv_TrEntregaEfec = source.Dscv_TrEntregaEfec,
                    Dscv_TrRetiroEfec = source.Dscv_TrRetiroEfec,
                    Dscv_TrRetiroGenerado = source.Dscv_TrRetiroGenerado
            WHEN NOT MATCHED THEN
                INSERT 
                (scv_id, scvemp_Codigo, scvsuc_Cod, 
                Dscv_TrEntregaEfec, Dscv_TrRetiroEfec, Dscv_TrRetiroGenerado)
                VALUES 
                (source.scv_id, source.scvemp_codigo, source.scvsuc_cod, 
                source.Dscv_TrEntregaEfec, source.Dscv_TrRetiroEfec, source.Dscv_TrRetiroGenerado);
        '''

		if datos_upsert:
			cursor.executemany(sql_merge, datos_upsert)
			conexion.commit()

	except Exception as e:
		print(f"Error en la operación: {e}")
		conexion.rollback()

	finally:
		cursor.close()
		conexion.close()

	return list_entregas_actualizar  # Retorna la lista con scv_id encontrados
