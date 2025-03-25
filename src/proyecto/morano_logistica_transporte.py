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
	lista_entregas = funciones_generales.leer_excel_y_convertir_a_lista(ruta_archivo, titulo=0, datos=0)

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

	# Mueve el archivo a procesados o NO procesados
	if 1 == 1:
		funciones_generales.mover_archivo(directorio_origen=config_logistica.dir_lista_entrega,
		                                  nombre_archivo_origen=config_logistica.archivo_entrega,
		                                  extension_origen="xlsx",
		                                  directorio_exportar=config_logistica.dir_archivo_procesado,
		                                  incluye_fecha=config_logistica.dir_archivo_proc_incluye_fecha)
	else:
		print("NO procesado")

	# Muestra un resumen de lo que ocurrio en el proceso


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
