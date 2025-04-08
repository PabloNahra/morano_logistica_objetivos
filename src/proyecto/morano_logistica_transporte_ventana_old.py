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
import tkinter as tk
from tkinter import ttk

def actualizar_progreso(progreso, ventana, porcentaje):
	progreso["value"] = porcentaje
	ventana.update_idletasks()


def mostrar_mensaje_final(ventana, mensaje):
	for widget in ventana.winfo_children():
		widget.destroy()
	label_final = tk.Label(ventana, text=mensaje, font=("Arial", 12), pady=20)
	label_final.pack()
	boton_cerrar = tk.Button(ventana, text="Cerrar", command=ventana.destroy)
	boton_cerrar.pack()


def ejecutar_proceso():
	ventana = tk.Tk()
	ventana.title("LOGISTICA - ACTUALIZANDO")
	ventana.geometry("350x180")
	ventana.resizable(False, False)
	ventana.eval('tk::PlaceWindow . center')

	# Cambiar el icono de la ventana
	ventana.iconbitmap("morano_icon2.ico")

	# label = tk.Label(ventana, text="Procesando...", font=("Arial", 14), bg=ventana.cget("bg"))
	label = tk.Label(ventana, text="Procesando...", font=("Arial", 14), bg="white")
	label.pack(pady=10)

	progreso = ttk.Progressbar(ventana, length=300, mode="determinate")
	progreso.pack(pady=10)

	ventana.update_idletasks()

	try:
		funciones_generales.log_grabar('Logistica Transporte - Integracion - Inicio', config_logistica.dir_log)
		actualizar_progreso(progreso, ventana, 10)

		# Número de Proceso
		funciones_generales.log_grabar('nro_proceso - inicio - ejecutar_proceso()', config_logistica.dir_log)
		nro_proceso = func_baseintermedia.obtener_nuevo_nro_proceso(sql_server=config_logistica.sql_server_int,
		                                                            sql_db=config_logistica.sql_db_int,
		                                                            sql_user=config_logistica.sql_user_int,
		                                                            sql_pass=config_logistica.sql_pass_int)
		actualizar_progreso(progreso, ventana, 30)

		# Toma el Excel del directorio
		funciones_generales.log_grabar('ruta_archivo - inicio - ejecutar_proceso()', config_logistica.dir_log)
		ruta_archivo = os.path.join(config_logistica.dir_lista_entrega, config_logistica.archivo_entrega)
		lista_entregas = funciones_generales.leer_excel_y_convertir_a_lista(ruta_archivo, titulo=0, datos=0)
		actualizar_progreso(progreso, ventana, 50)

		# Copia datos del excel a tabla intermedia
		funciones_generales.log_grabar('lista_entregas_filt - inicio - ejecutar_proceso()', config_logistica.dir_log)
		try:
			lista_entregas_filt = func_baseintermedia.insert_datos_excel(sql_server=config_logistica.sql_server_int,
			                                                             sql_db=config_logistica.sql_db_int,
			                                                             sql_user=config_logistica.sql_user_int,
			                                                             sql_pass=config_logistica.sql_pass_int,
			                                                             nro_proceso=nro_proceso,
			                                                             list_entregas=lista_entregas)
			actualizar_progreso(progreso, ventana, 70)
		except Exception as e:
			mostrar_mensaje_final(ventana, f"Error al insertar datos en la base de datos: {str(e)}")
			return  # Detener el proceso aquí

		# Actualiza datos en Bejerman
		funciones_generales.log_grabar('list_entregas_actualizar - inicio - ejecutar_proceso()',
		                               config_logistica.dir_log)
		try:
			list_entregas_actualizar = func_bejerman.actualizar_datos_adicionales_sb(
				sql_server=config_logistica.sql_server_sb,
				sql_db=config_logistica.sql_db_sb,
				sql_user=config_logistica.sql_user_sb,
				sql_pass=config_logistica.sql_pass_sb,
				list_entregas_filt=lista_entregas_filt,
				dias_hacia_atras=config_logistica.dias_hacia_atras)
			actualizar_progreso(progreso, ventana, 90)
		except Exception as e:
			mostrar_mensaje_final(ventana, f"Error al actualizar datos en Bejerman: {str(e)}")
			return  # Detener el proceso aquí

		# Mueve el archivo a procesados o NO procesados
		funciones_generales.log_grabar('mover_archivo - inicio - ejecutar_proceso()', config_logistica.dir_log)
		if len(list_entregas_actualizar) != 0:
			funciones_generales.mover_archivo(directorio_origen=config_logistica.dir_lista_entrega,
			                                  nombre_archivo_origen=config_logistica.archivo_entrega,
			                                  extension_origen="xlsx",
			                                  directorio_exportar=config_logistica.dir_archivo_procesado,
			                                  incluye_fecha=config_logistica.dir_archivo_proc_incluye_fecha)
			mensaje_final = (f"El proceso terminó exitosamente\n\n"
			                 f"Del total de {len(lista_entregas)} registros:\n"
			                 f"Se actualizaron: {len(list_entregas_actualizar)}\n"
			                 f"NO se utilizaron: {len(lista_entregas) - len(list_entregas_actualizar)}")

		else:
			funciones_generales.mover_archivo(directorio_origen=config_logistica.dir_lista_entrega,
			                                  nombre_archivo_origen=config_logistica.archivo_entrega,
			                                  extension_origen="xlsx",
			                                  directorio_exportar=config_logistica.dir_archivo_no_procesado,
			                                  incluye_fecha=config_logistica.dir_archivo_proc_incluye_fecha)
			mensaje_final = (f"El proceso terminó con INCONVENIENTES")

		actualizar_progreso(progreso, ventana, 100)

	except Exception as e:
		funciones_generales.log_grabar(f'ERROR - Termino programa - Exception: {e} - ejecutar_proceso()', config_logistica.dir_log)
		funciones_generales.envio_mail(config_logistica.mail_from,
		                               config_logistica.mail_to,
		                               config_logistica.mail_subject, '',
		                               f'Mensaje: {e}')
		funciones_generales.mover_archivo(directorio_origen=config_logistica.dir_lista_entrega,
		                                  nombre_archivo_origen=config_logistica.archivo_entrega,
		                                  extension_origen="xlsx",
		                                  directorio_exportar=config_logistica.dir_archivo_no_procesado,
		                                  incluye_fecha=config_logistica.dir_archivo_proc_incluye_fecha)
		mensaje_final = (f"El proceso terminó con INCONVENIENTES: {e}")
		# mostrar_mensaje_final(ventana, f"Se produjo un error inesperado: {str(e)}")
		mostrar_mensaje_final(ventana, mensaje_final)

	finally:
		funciones_generales.log_grabar('Logistica Transporte - Integracion - Fin - ejecutar_proceso()',
		                               config_logistica.dir_log)
		mostrar_mensaje_final(ventana, mensaje_final)
		ventana.mainloop()

if __name__ == "__main__":
	ejecutar_proceso()
