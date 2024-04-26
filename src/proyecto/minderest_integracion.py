'''
Fecha: 2024-02-19
Autor: Pablo Nahra
Objetivo:
Usando las APIs de VTEX puede tomar la información de la plataforma y luego tomar el resto de la información de iPoint
La APP tiene que tener como INPUT los SKU que vamos a querer controlar.. Puede ser un archivo de EXCEL con
el detalle de los artículos
A controlar.. Ese Archivo de EXCEL lo tiene que generar el sector de Compras (Sebas Rossi y su equipo) y
dejarlo en una carpeta compartida del Z:
La APP tiene que tomar ese EXCEL y generar el archivo para los SKU declarados..
El archivo resultante lo tiene que subir a un FTP
(que nos van a asignar dirección usuario y clave) y (por las dudas) dejar una copia
En la misma carpeta (usando un subdirectorio) desde donde leyó el Excel.
El proceso se tiene que poder ejecutar desde una tarea de Windows. Dejarlo en el servidor 10.10.29.223
'''
import os
import config
import funciones_generales
import funciones_vtex
import funciones_ipoint
from decimal import Decimal


try:
	funciones_generales.log_grabar('Minderest - Integracion - Inicio', config.dir_log)

	sku_lista_exportar = []

	# archivo de lista de SKU
	# archivo_lista_sku = config.dir_sku_lista + config.archivo_skus_integrar
	ruta_archivo = os.path.join(config.dir_sku_lista, config.archivo_skus_integrar)

	# Tomar excel de SKU a integrar
	lista_sku = funciones_generales.leer_excel_y_convertir_a_lista(ruta_archivo)

	# Generar el auxiliar de stock de ipoint
	funciones_ipoint.ipoint_genero_stock_sql(sql_server=config.sql_server_ipoint,
	                                         sql_db=config.sql_db_ipoint,
	                                         sql_user=config.sql_user_ipoint,
	                                         sql_pass=config.sql_pass_ipoint)

	# PRUEBA
	# lista_sku = [{'SKU': 'CAL36024ARA'}]
	# lista_sku = [{'SKU': 'SMA145MLGEARO'}]

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
			funciones_generales.log_grabar(f'ERROR - SKU: {sku["SKU"]} - Exception: {e}', config.dir_log)

			if hasattr(e, 'message'):
				funciones_generales.log_grabar(f'ERROR - SKU: {sku["SKU"]} - Message: {e.message}', config.dir_log)
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

	if config.copiar_direc_red == 1:
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
	funciones_generales.log_grabar(f'ERROR - Termino programa - Exception: {e}', config.dir_log)
	funciones_generales.envio_mail(config.mail_from, config.mail_to, config.mail_subject, '',
	                               f'Mensaje: {e}')
	if hasattr(e, 'message'):
		funciones_generales.log_grabar(f'ERROR - Termino programa - Message: {e.message}', config.dir_log)
		funciones_generales.envio_mail(config.mail_from, config.mail_to,
		                               config.mail_subject,
		                               '',
		                               f'Mensaje: {e.message}')
except PermissionError as e:
	funciones_generales.log_grabar(f'ERROR - Termino programa: {e.message}', config.dir_log)
	funciones_generales.log_grabar('ERROR - Termino programa: Error de acceso a directorio', config.dir_log)
	funciones_generales.envio_mail(config.mail_from, config.mail_to,
	                               config.mail_subject,
	                               '',
	                               f'Mensaje: {e.message}')
	if hasattr(e, 'message'):
		funciones_generales.log_grabar(f'ERROR - Termino programa - Message: {e.message}', config.dir_log)
		funciones_generales.envio_mail(config.mail_from, config.mail_to,
		                               config.mail_subject,
		                               '',
		                               f'Mensaje: {e.message}')
finally:
	funciones_generales.log_grabar('Minderest - Integracion - Fin', config.dir_log)
