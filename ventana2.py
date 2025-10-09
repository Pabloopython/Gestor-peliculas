import tkinter as tk  # Importamos la librería

ventana = tk.Tk()  # Creamos la ventana principal
ventana.title("Gestor de películas")  # Le ponemos un título
ventana.geometry("1000x700") # Espacio que ocupa la ventana en el ordenador
ventana.configure(bg="lightblue")  # Le cambiamos el color de fondo de la ventana

# 2. Creación de Widgets

# --- Formulario de Entrada ---
etiqueta_desc = tk.Label(ventana, text="Descripción:",fg="white", bg="lightgreen", font=("Arial", 12,))
campo_desc = tk.Entry(ventana, width=40)

etiqueta_nombre = tk.Label(ventana, text="Nombre:",fg="white", bg="lightgreen", font=("Arial", 12,))
campo_nombre = tk.Entry(ventana)

etiqueta_director = tk.Label(ventana, text="Director:",fg="white", bg="lightgreen", font=("Arial", 12,))
campo_director = tk.Entry(ventana)

etiqueta_protagonista = tk.Label(ventana, text="Protagonista:",fg="white", bg="lightgreen", font=("Arial", 12,))
campo_protagonista = tk.Entry(ventana)

etiqueta_valoracion = tk.Label(ventana, text="Valoración:",fg="white", bg="lightgreen", font=("Arial", 12,))
campo_valoracion = tk.Entry(ventana)

etiqueta_prio = tk.Label(ventana, text="Prioridad:",fg="white", bg="lightgreen", font=("Arial", 12,))
campo_prio = tk.Entry(ventana)

etiqueta_completado = tk.Label(ventana, text = False,fg="white", bg="lightgreen", font=("Arial", 12,))
campo_completado = tk.Entry(ventana)

etiqueta_barra_estado = tk.Label(ventana, text="Listo",fg="white", bg="lightgreen", font=("Arial", 12,) )
campo_barra_estado = tk.Entry(ventana)


# --- Botones ---
boton_add = tk.Button(ventana, text="Añadir Tarea",fg="white", bg="lightgreen", font=("Arial", 12,))
boton_update = tk.Button(ventana, text="Modificar Tarea",fg="white", bg="lightgreen", font=("Arial", 12,))
boton_delete = tk.Button(ventana, text="Eliminar Tarea",fg="white", bg="lightgreen", font=("Arial", 12,))

# --- Lista de Tareas + Scrollbar ---
etiqueta_lista = tk.Label(ventana, text="Tareas Pendientes:",fg="white", bg="lightgreen", font=("Arial", 12,))
lista_tareas = tk.Listbox(ventana, width=60, height=10)
etiqueta_scrollbar = tk.Scrollbar(ventana, orient="vertical", command=lista_tareas.yview)
lista_tareas.config(yscrollcommand=etiqueta_scrollbar.set)

# 3. Posicionamiento con Grid

# --- Formulario de Entrada ---
etiqueta_desc.grid(row=1, column=0, padx=10, pady=5, sticky="w")
campo_desc.grid(row=1, column=1, padx=10, pady=5, columnspan=3, sticky="ew")

etiqueta_nombre.grid(row=0, column=1, padx=10, pady=5, sticky="w")
campo_nombre.grid(row=0, column=2, padx=10, pady=5, sticky="ew")

etiqueta_director.grid(row=2, column=0, padx=10, pady=5, sticky="w")
campo_director.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

etiqueta_protagonista.grid(row=2, column=2, padx=10, pady=5, sticky="w")
campo_protagonista.grid(row=2, column=3, padx=10, pady=5, sticky="ew")

etiqueta_valoracion.grid(row=3, column=0, padx=10, pady=5, sticky="w")
campo_valoracion.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

# --- Botones ---
boton_add.grid(row=4, column=1, padx=10, pady=10)
boton_update.grid(row=4, column=2, padx=10, pady=10)
boton_delete.grid(row=4, column=3, padx=10, pady=10)

# --- Lista de Tareas + Scrollbar ---
etiqueta_lista.grid(row=4, column=0, padx=10, pady=5, sticky="w")
lista_tareas.grid(row=6, column=0, columnspan=4, padx=10, pady=5, sticky="nsew")
etiqueta_scrollbar.grid(row=1, column=5, padx=10, pady=5, sticky="w")
etiqueta_scrollbar.grid(row=4, column=5, rowspan=5, padx=10, pady=5, sticky="nsew")

# --- Barra estado" ---
etiqueta_barra_estado = tk.Label(ventana, text="Listo",fg="white", bg="lightgreen", font=("Arial", 12,))
etiqueta_barra_estado.grid(row=8, column=3, padx=10, pady=5, sticky="ew")

ventana.mainloop()  # Mantiene la ventana abierta y a la espera de acciones
