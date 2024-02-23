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
import config
import funciones_generales
import funciones_vtex

try:
	funciones_generales.log_grabar('Minderest - Integracion - Inicio', config.dir_log)

	# Tomar excel de SKU a integrar
	lista_sku = funciones_generales.leer_excel_y_convertir_a_lista('SKU_integrar')
	print(lista_sku)

	# Recorremos los SKU
	for sku in lista_sku:
		print(sku)
		# Leer datos de SKU de VTEX
		# info_vtex_sku = funciones_vtex.vtex_sku_by_ref_id(sku='kit-gm00002')
		info_vtex_sku = funciones_vtex.vtex_sku_by_ref_id(sku=sku['SKU'])
		print("info_vtex_sku")
		print(info_vtex_sku)


		# Leer datos de SKU de iPoint


		# complementar datos

	# Generar archivo de salida

	# Generar archivo de log (copia)

	# Subir archivo a FTP (Musimundo?)


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
