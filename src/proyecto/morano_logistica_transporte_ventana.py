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
import tkinter as tk
from tkinter import ttk
from decimal import Decimal


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
	ventana.title("Actualizando datos de Logística")
	ventana.geometry("400x200")
	ventana.resizable(False, False)
	ventana.eval('tk::PlaceWindow . center')

	label = tk.Label(ventana, text="Procesando...", font=("Arial", 12))
	label.pack(pady=10)

	progreso = ttk.Progressbar(ventana, length=300, mode="determinate")
	progreso.pack(pady=10)

	ventana.update_idletasks()

	try:
		funciones_generales.log_grabar('Logistica Transporte - Integracion - Inicio', config_logistica.dir_log)
		actualizar_progreso(progreso, ventana, 10)

		# Número de Proceso
		nro_proceso = func_baseintermedia.obtener_nuevo_nro_proceso(sql_server=config_logistica.sql_server_int,
		                                                            sql_db=config_logistica.sql_db_int,
		                                                            sql_user=config_logistica.sql_user_int,
		                                                            sql_pass=config_logistica.sql_pass_int)
		actualizar_progreso(progreso, ventana, 30)

		# Toma el Excel del directorio
		ruta_archivo = os.path.join(config_logistica.dir_lista_entrega, config_logistica.archivo_entrega)
		lista_entregas = funciones_generales.leer_excel_y_convertir_a_lista(ruta_archivo, titulo=0, datos=1)
		actualizar_progreso(progreso, ventana, 50)

		# Copia datos del excel a tabla intermedia
		lista_entregas_filt = func_baseintermedia.insert_datos_excel(sql_server=config_logistica.sql_server_int,
		                                                             sql_db=config_logistica.sql_db_int,
		                                                             sql_user=config_logistica.sql_user_int,
		                                                             sql_pass=config_logistica.sql_pass_int,
		                                                             nro_proceso=nro_proceso,
		                                                             list_entregas=lista_entregas)
		actualizar_progreso(progreso, ventana, 70)

		# Actualiza datos en Bejerman
		list_entregas_actualizar = func_bejerman.actualizar_datos_adicionales_sb(
			sql_server=config_logistica.sql_server_sb,
			sql_db=config_logistica.sql_db_sb,
			sql_user=config_logistica.sql_user_sb,
			sql_pass=config_logistica.sql_pass_sb,
			list_entregas_filt=lista_entregas_filt)
		actualizar_progreso(progreso, ventana, 90)

		# Mueve el archivo a procesados
		funciones_generales.mover_archivo(directorio_origen=config_logistica.dir_lista_entrega,
		                                  nombre_archivo_origen=config_logistica.archivo_entrega,
		                                  extension_origen="xlsx",
		                                  directorio_exportar=config_logistica.dir_archivo_procesado,
		                                  incluye_fecha=config_logistica.dir_archivo_proc_incluye_fecha)
		actualizar_progreso(progreso, ventana, 100)

		mensaje_final = f"El proceso terminó exitosamente\nDel total de {len(lista_entregas)} registros:\n- Se actualizaron {len(list_entregas_actualizar)}\n- NO se utilizaron {len(lista_entregas) - len(list_entregas_actualizar)}"

	except Exception as e:
		funciones_generales.log_grabar(f'ERROR - Termino programa - Exception: {e}', config_logistica.dir_log)
		funciones_generales.envio_mail(config_logistica.mail_from,
		                               config_logistica.mail_to,
		                               config_logistica.mail_subject, '',
		                               f'Mensaje: {e}')
		mensaje_final = "El proceso tuvo INCONVENIENTES"

	finally:
		funciones_generales.log_grabar('Logistica Transporte - Integracion - Fin', config_logistica.dir_log)
		mostrar_mensaje_final(ventana, mensaje_final)
		ventana.mainloop()


if __name__ == "__main__":
	ejecutar_proceso()
