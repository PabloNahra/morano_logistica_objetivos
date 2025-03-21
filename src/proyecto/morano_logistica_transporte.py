'''
Fecha: 2025-03-20
Autor: Pablo Nahra
Objetivo:
Proceso backend que al ejecutarse toma un Excel de un directorio y lo procesa para impactar algunos datos de este excel
en datos adicionales de bejerman
El Excel posee datos del transporte de envios a clientes
'''
import os
import config_logistica
import funciones_generales, func_baseintermedia, func_bejerman
import funciones_ipoint
from decimal import Decimal


try:
	funciones_generales.log_grabar('Logistica Transporte - Integracion - Inicio', config_logistica.dir_log)

	# Número de Proceso
	nro_proceso = func_baseintermedia.obtener_nuevo_nro_proceso(sql_server=config_logistica.sql_server_int,
	                                                     sql_db=config_logistica.sql_db_int,
	                                                     sql_user=config_logistica.sql_user_int,
	                                                     sql_pass=config_logistica.sql_pass_int)

	# Toma el Excel del directorio
	ruta_archivo = os.path.join(config_logistica.dir_lista_entrega, config_logistica.archivo_entrega)
	lista_entregas = funciones_generales.leer_excel_y_convertir_a_lista(ruta_archivo, titulo=0, datos=1)

	# Copia datos del excel a tabla intermedia (con número de proceso) - La tabla intermedia en DBReportes
	lista_entregas_filt = func_baseintermedia.insert_datos_excel(sql_server=config_logistica.sql_server_int,
	                                                     sql_db=config_logistica.sql_db_int,
	                                                     sql_user=config_logistica.sql_user_int,
	                                                     sql_pass=config_logistica.sql_pass_int,
	                                                     nro_proceso=nro_proceso,
	                                               list_entregas=lista_entregas
	                                               )

	# Con los mismos datos que se insertaron, copiar las fechas en el dato adicional de Bejerman: lista_entregas_filt
	list_entregas_actualizar = func_bejerman.actualizar_datos_adicionales_sb(sql_server=config_logistica.sql_server_sb,
	                                              sql_db=config_logistica.sql_db_sb,
	                                              sql_user=config_logistica.sql_user_sb,
	                                              sql_pass=config_logistica.sql_pass_sb,
	                                              list_entregas_filt=lista_entregas_filt
	                                              )

	print(len(list_entregas_actualizar))

	# Mueve el archivo a procesados o NO procesados

	# Muestra un resumen de lo que ocurrio en el proceso


	## CODIGO ANTERIOR
	sku_lista_exportar = []


	# Recorremos los SKU
	for sku in lista_sku:
		try:
			sku_datos_ordenados = {}

			# Leer datos de SKU de VTEX
			info_vtex_sku = funciones_vtex.vtex_sku_by_ref_id(sku=sku['SKU'])

			# Leer datos de SKU de iPoint
			info_sku_ipoint = funciones_ipoint.ipoint_by_sku_sql(sql_server=config.sql_server_ipoint,
			                                    sql_db=config.sql_db_ipoint,
			                                    sql_user=config.sql_user_ipoint,
			                                    sql_pass=config.sql_pass_ipoint,
			                                    sku=sku['SKU'])

			sku_datos_ordenados = {
				'ID': info_sku_ipoint['ID'],
				'URL': info_vtex_sku['URL'],
				'NAME': info_vtex_sku['NAME'],
				'EAN': info_sku_ipoint['EAN'],
				'PRICE': round(
					round(float(Decimal(info_sku_ipoint['PRICE'])), 2) *
					((100 + info_sku_ipoint['VAT']) / 100),
					0),
				'PRICE_BEFORE_OFFER': round(
					round(float(Decimal(info_sku_ipoint['PRICE_BEFORE_OFFER'])), 2) *
					((100 + info_sku_ipoint['VAT']) / 100),
					0),
				'COST': 0,
				'CURRENCY': "ARS",
				'VAT': info_sku_ipoint['VAT'],
				'STOCK': round(float(Decimal(info_sku_ipoint['STOCK'])), 0),
				'URL_IMAGE': info_vtex_sku['URL_IMAGE'],
				'BRAND': info_sku_ipoint['BRAND'],
				'OWN_BRAND': "",
				'OWN_BRAND_COMP': "",
				'MPN': info_sku_ipoint['MPN'],
				'CATEGORY': ">".join([value for key, value in info_vtex_sku['CATEGORY'].items()]),
				'TAG': info_vtex_sku['TAG'],
				'SHIPPING_COST': 0,
				'UNIT': "UNIDAD",
				'VALUE': 1
			}

			sku_lista_exportar.append(sku_datos_ordenados)

		except Exception as e:
			funciones_generales.log_grabar(f'ERROR - SKU: {sku["SKU"]} - Exception: {e}', config_logistica.dir_log)

			if hasattr(e, 'message'):
				funciones_generales.log_grabar(f'ERROR - SKU: {sku["SKU"]} - Message: {e.message}', config_logistica.dir_log)
			continue  # Continuar con el siguiente SKU después de manejar la excepción

	# Generar archivo de salida para subir al FTP
	file_to_ftp = funciones_generales.exportacion_archivo(sku_lista_exportar, config.nombre_archivo_exportar,
	                                        incl_fecha=0, tipo_archivo=config.tipo_archivo_exportar,
	                                        directorio=config.dir_archivo)

	# Generar archivo de salida de log
	funciones_generales.exportacion_archivo(sku_lista_exportar, config.nombre_archivo_exportar,
	                                        incl_fecha=1, tipo_archivo=config.tipo_archivo_exportar,
	                                        directorio=config.dir_archivo_historial)

	# Envio el archivo al directorio de RED que se publica por FTP
	# Codeo los valores para la conexión de red
	user = "SAT\\administrador"
	password = "Octaedro2020%"

	if config_logistica.copiar_direc_red == 1:
		funciones_generales.copiar_archivo_a_red(archivo_local=file_to_ftp,
		                                         directorio_red=config.directorio_red,
	                                             usuario=user,
	                                             contrasena=password)



	# Subir archivo a FTP
	if config.subir_ftp == 1:
		funciones_generales.subir_archivo_ftp(server=config.server_ftp,
	                                      port=config.port_ftp,
	                                      user=config.user_ftp,
	                                      password=config.password_ftp,
	                                      archivo_local=f"{config.dir_archivo}//"
	                                                    f"{config.nombre_archivo_exportar}."
	                                                    f"{config.tipo_archivo_exportar}" ,
	                                          archivo_remoto=f"{config.nombre_archivo_exportar}."
	                                                    f"{config.tipo_archivo_exportar}")


except Exception as e:
	funciones_generales.log_grabar(f'ERROR - Termino programa - Exception: {e}', config_logistica.dir_log)
	funciones_generales.envio_mail(config_logistica.mail_from,
	                               config_logistica.mail_to,
	                               config_logistica.mail_subject, '',
	                               f'Mensaje: {e}')
	if hasattr(e, 'message'):
		funciones_generales.log_grabar(f'ERROR - Termino programa - Message: {e.message}', config_logistica.dir_log)
		funciones_generales.envio_mail(config_logistica.mail_from, config_logistica.mail_to,
		                               config_logistica.mail_subject,
		                               '',
		                               f'Mensaje: {e.message}')
except PermissionError as e:
	funciones_generales.log_grabar(f'ERROR - Termino programa: {e.message}', config_logistica.dir_log)
	funciones_generales.log_grabar('ERROR - Termino programa: Error de acceso a directorio', config_logistica.dir_log)
	funciones_generales.envio_mail(config_logistica.mail_from,
	                               config_logistica.mail_to,
	                               config_logistica.mail_subject,
	                               '',
	                               f'Mensaje: {e.message}')
	if hasattr(e, 'message'):
		funciones_generales.log_grabar(f'ERROR - Termino programa - Message: {e.message}', config_logistica.dir_log)
		funciones_generales.envio_mail(config_logistica.mail_from,
		                               config_logistica.mail_to,
		                               config_logistica.mail_subject,
		                               '',
		                               f'Mensaje: {e.message}')
finally:
	funciones_generales.log_grabar('Logistica Transporte - Integracion - Fin', config_logistica.dir_log)
