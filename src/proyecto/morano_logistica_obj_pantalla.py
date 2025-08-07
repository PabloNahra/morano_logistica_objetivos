import os
import config_logist_obj
import funciones_generales, func_baseintermedia, func_bejerman
import tkinter as tk
from tkinter import ttk


def mostrar_mensaje_error(ventana, mensaje_error):
    for widget in ventana.winfo_children():
        widget.destroy()

    # Configurar el límite de caracteres por línea y cantidad máxima de líneas
    max_chars_per_line = 50
    max_lines = 3

    # Dividir el mensaje en líneas
    palabras = mensaje_error.split()
    lineas = []
    linea_actual = ""

    for palabra in palabras:
        if len(linea_actual) + len(palabra) + 1 <= max_chars_per_line:
            linea_actual += " " + palabra if linea_actual else palabra
        else:
            lineas.append(linea_actual)
            linea_actual = palabra
            if len(lineas) >= max_lines - 1:  # Si ya llenamos 2 líneas, cortamos
                break

    if linea_actual:
        lineas.append(linea_actual)

    # Si el mensaje es más largo, agregamos "..."
    if len(palabras) > sum(len(linea.split()) for linea in lineas):
        lineas[-1] += "..."

    # Agregar la cuarta línea fija
    lineas.append("REVISE EL LOG DE ERRORES")

    mensaje_formateado = "\n".join(lineas)

    label = tk.Label(
        ventana,
        text=mensaje_formateado,
        fg="red",
        font=("Arial", 12, "bold"),
        anchor="w",  # Alinear texto a la izquierda
        justify="left"  # Justificar texto a la izquierda
    )
    label.pack(pady=20, padx=10, fill="both", expand=True)

    boton_cerrar = tk.Button(ventana, text="Cerrar", command=ventana.destroy)
    boton_cerrar.pack(pady=10)

    ventana.mainloop()

def actualizar_progreso(progreso, ventana, porcentaje):
    progreso["value"] = porcentaje
    ventana.update_idletasks()

def mostrar_mensaje_final(ventana, mensaje):
    """Destruye widgets actuales y muestra el mensaje final."""
    for widget in ventana.winfo_children():
        widget.destroy()
    label_final = tk.Label(ventana, text=mensaje, font=("Arial", 12), pady=20)
    label_final.pack()
    boton_cerrar = tk.Button(ventana, text="Cerrar", command=ventana.destroy)
    boton_cerrar.pack()

def ejecutar_proceso():
    """Ejecuta el proceso y muestra una ventana con progreso."""
    ventana = tk.Tk()
    ventana.title("LOGIST - OBJETIVOS - ACTUALIZANDO")
    ventana.geometry("350x180")
    ventana.resizable(False, False)
    ventana.eval('tk::PlaceWindow . center')
    ventana.iconbitmap("morano_icon2.ico")

    label = tk.Label(ventana, text="Procesando...", font=("Arial", 14), bg="white")
    label.pack(pady=10)

    progreso = ttk.Progressbar(ventana, length=300, mode="determinate")
    progreso.pack(pady=10)

    ventana.update_idletasks()

    try:
        funciones_generales.log_grabar('Logistica - Objetivos - Inicio',
                                       config_logist_obj.dir_log)
        actualizar_progreso(progreso, ventana, 10)

        # Obtener Número de Proceso
        funciones_generales.log_grabar('nro_proceso - inicio - ejecutar_proceso()',
                                       config_logist_obj.dir_log)
        nro_proceso = func_baseintermedia.obtener_nuevo_nro_proceso(
            sql_server=config_logist_obj.sql_server_int,
            sql_db=config_logist_obj.sql_db_int,
            sql_user=config_logist_obj.sql_user_int,
            sql_pass=config_logist_obj.sql_pass_int
        )
        actualizar_progreso(progreso, ventana, 30)

        # Leer el Excel
        funciones_generales.log_grabar('ruta_archivo - inicio - ejecutar_proceso()', config_logist_obj.dir_log)
        ruta_archivo = os.path.join(config_logist_obj.dir_planilla_objetivos,
                                    config_logist_obj.planilla_objetivos)
        # lista_entregas = funciones_generales.leer_excel_y_convertir_a_lista(ruta_archivo, titulo=0, datos=0)
        objetivos = funciones_generales.leer_excel_y_convertir_a_lista(ruta_archivo, titulo=0, datos=0)
        actualizar_progreso(progreso, ventana, 50)

        # Insertar datos en tabla intermedia y tengo dos listas, las a integrar y la NO a integrar
        funciones_generales.log_grabar('planillas_objetivos - inicio - ejecutar_proceso()',
                                       config_logist_obj.dir_log)
        lista_obj_filt, list_obj_no_integrar = func_baseintermedia.insert_datos_excel(
            sql_server=config_logist_obj.sql_server_int,
            sql_db=config_logist_obj.sql_db_int,
            sql_user=config_logist_obj.sql_user_int,
            sql_pass=config_logist_obj.sql_pass_int,
            nro_proceso=nro_proceso,
            list_objetivos=objetivos,
            obj_tareas_perm=config_logist_obj.tareas_permitidas,
            obj_tipos_tareas_perm=config_logist_obj.tipos_tareas_permitidas,
        )
        actualizar_progreso(progreso, ventana, 70)

        actualizar_progreso(progreso, ventana, 90)

        # Mover archivo a procesados o no procesados
        funciones_generales.log_grabar('mover_archivo - inicio - ejecutar_proceso()',
                                       config_logist_obj.dir_log)
        # if len(list_entregas_actualizar) != 0:
        if len(lista_obj_filt) != 0:
            funciones_generales.mover_archivo(
                directorio_origen=config_logist_obj.dir_planilla_objetivos,
                nombre_archivo_origen=config_logist_obj.planilla_objetivos,
                extension_origen="xlsx",
                directorio_exportar=config_logist_obj.dir_archivo_procesado,
                incluye_fecha=config_logist_obj.dir_archivo_proc_incluye_fecha
            )
            mensaje_final = (f"El archivo sé procesó\n\n"
                             f"Del total de {len(objetivos)} registros:\n"
                             f"Se actualizaron: {len(lista_obj_filt)}\n"
                             f"NO se utilizaron: {len(list_obj_no_integrar)} \n"
                             f"(Revisar Detalle en Archivo)")
        else:
            funciones_generales.mover_archivo(
                directorio_origen=config_logist_obj.dir_planilla_objetivos,
                nombre_archivo_origen=config_logist_obj.planilla_objetivos,
                extension_origen="xlsx",
                directorio_exportar=config_logist_obj.dir_archivo_no_procesado,
                incluye_fecha=config_logist_obj.dir_archivo_proc_incluye_fecha
            )
            mensaje_final = "El archivo NO se procesó por INCONSISTENCIAS"

        # Exportó el detalle de registros que NO pudieron procesarse
        if len(list_obj_no_integrar) != 0:
            listas_registros_no_proc = list_obj_no_integrar

            funciones_generales.exportacion_archivo(lista_diccionarios=listas_registros_no_proc,
                                                    nombre_archivo=config_logist_obj.planilla_objetivos,
                                                    campo_orden='Motivo',
                                                    incl_fecha=True,
                                                    tipo_archivo='excel',
                                                    directorio=config_logist_obj.dir_items_no_procesados,
                                                    orden_campos=config_logist_obj.items_no_proc_orden_campos)

        actualizar_progreso(progreso, ventana, 100)
        mostrar_mensaje_final(ventana, mensaje_final)
        ventana.mainloop()

    except Exception as e:
        # Capturar cualquier error y mostrarlo en la ventana
        funciones_generales.log_grabar(f'ERROR - Termino programa - Exception: {e}',
                                       config_logist_obj.dir_log)
        funciones_generales.mover_archivo(
            directorio_origen=config_logist_obj.dir_lista_entrega,
            nombre_archivo_origen=config_logist_obj.archivo_entrega,
            extension_origen="xlsx",
            directorio_exportar=config_logist_obj.dir_archivo_no_procesado,
            incluye_fecha=config_logist_obj.dir_archivo_proc_incluye_fecha
        )
        mensaje_error = f"Error: {str(e)}"
        mostrar_mensaje_error(ventana, mensaje_error)  # Muestra el error en pantalla

if __name__ == "__main__":
    ejecutar_proceso()
