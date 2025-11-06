import tkinter as tk
import sqlite3

class Pelicula:

    def __init__(self, nombre, descripcion, director, protagonista, valoracion, prioridad=True, completada=False):
        
            # Creamos los atributos de la película
        self.id = None
        self.nombre = nombre
        self.descripcion = descripcion
        self.director = director
        self.protagonista = protagonista
        self.valoracion = valoracion
        self.prioridad = prioridad
        self.completada = completada

    def __str__(self):
        return f"Nombre: {self.nombre} \nDescripcion: {self.descripcion} \nDirector: {self.director} \nProtagonista: {self.protagonista} \nValoracion: {self.valoracion} \nPrioridad: {self.prioridad} \nCompletada: {self.completada}"

    pelicula1=Pelicula("Cars", "Infantil/Comedia", "John Lasseter", "Rayo Mcqueen", "5 estrellas", "Alta")
    pelicula2=Pelicula("The Notebook", "Romance", "Nick Cassavetes", "Ryan Gosling", "5 estrellas", "Alta")

    print("\n--- DATOS DE LA PELÍCULA 1 ---")
    print(película1)
    print("\n--- DATOS DE LA PELÍCULA 2 ---")
    print(película2)

    # --- Ventana Principal ---
    ventana = tk.Tk()
    ventana.title("Gestor de películas")
    ventana.geometry("1000x700")
    ventana.configure(bg= "#2E3440")

    # --- Frame: Formulario ---
    frame_formulario = tk.Frame(ventana, bg= "#2E3440")
    frame_formulario.grid(row=0, column=0, padx=10, pady=10)

    #--- Diccionario de campos ---
    campos_info = {
    "Nombre": {},
    "Descripción": {},
    "Director": {},
    "Protagonista": {},
    }

    # --- Crear etiquetas y campos dinámicamente ---
    for idx, (etiqueta, datos) in enumerate(campos_info.items()):
        lbl = tk.Label(frame_formulario, text=f"{etiqueta}:", fg="black", bg="#D3D3D3", font=("Arial", 12))
        entry = tk.Entry(frame_formulario, width=70 if etiqueta == "Descripción" else 50)

        lbl.grid(row=idx, column=0, padx=5, pady=5, ipady=5,)
        entry.grid(row=idx, column=1, padx=5, pady=5, ipady=5)

        campos_info[etiqueta]["label"] = lbl
        campos_info[etiqueta]["entry"] = entry
        
    campos_info2 = {
        "Valoración": {}, 
        "Prioridad": {},
        "Completado": {}
        }
            
    for i, (etiqueta2, datos) in enumerate(campos_info2.items()):
        lbl2 = tk.Label(frame_formulario, text=f"{etiqueta2}:", fg="black", bg="#D3D3D3", font=("Arial", 12))
        entry2 = tk.Entry(frame_formulario, width=25)
            
        if etiqueta2 == "Valoración":
            
            lbl2.grid(row=4, column=i, padx=5, pady=5, ipady=5,)
            entry2.grid(row=4, column=i+1, padx=5, pady=5, ipady=5)
                    
        elif etiqueta2 == "Prioridad":
            lbl2.grid(row=4, column=i+1, padx=5, pady=5, ipady=5,)
            entry2.grid(row=4, column=i+2, padx=5, pady=5, ipady=5)
                
        else :
            lbl2.grid(row=4, column=i+2, padx=5, pady=5, ipady=5,)
            entry2.grid(row=4, column=i+3, padx=5, pady=5, ipady=5)
                    
        campos_info2[etiqueta2]["label"] = lbl2
        campos_info2[etiqueta2]["entry"] = entry2

    frame_formulario.grid_columnconfigure(1, weight=2)

        # --- Frame: Botones ---
    frame_botones = tk.Frame(ventana, bg="#88C0D0")
    frame_botones.grid(row=1, column=0, padx=10, pady=10)

    botones = ["Añadir Película", "Modificar Película", "Eliminar Película"]
    for i, texto in enumerate(botones):
        btn = tk.Button(frame_botones, text=texto, fg="black", bg= "#88C0D0", font=("Arial", 12))
        btn.grid(row=0, column=i, padx=10, pady=5)

        # --- Lista de tareas y el Scrollbar ---
    etiqueta_lista = tk.Label(ventana, text="Tareas Pendientes:", fg="black", bg= "#D3D3D3", font=("Arial", 12))
    etiqueta_lista.grid(row=2, column=0, padx=10, pady=5, sticky="w")

    frame_lista = tk.Frame(ventana)
    frame_lista.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")

    lista_tareas = tk.Listbox(frame_lista, width=60, height=5)
    scrollbar = tk.Scrollbar(frame_lista, orient="vertical", command=lista_tareas.yview)
    lista_tareas.config(yscrollcommand=scrollbar.set)

    lista_tareas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    frame_lista.grid_rowconfigure(0, weight=1)
    frame_lista.grid_columnconfigure(0, weight=1)

        # --- Barra de estado ---
    barra_estado = tk.Label(ventana, text="Listo", fg="black", bg= "#81A1C1", font=("Arial", 12))
    barra_estado.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        # --- Expansión dinámica ---
    ventana.grid_rowconfigure(3, weight=1)
    ventana.grid_columnconfigure(0, weight=1)

        # --- PASO 1: Conectar a la base de datos ---
        # Se crea el archivo 'tareas.db' si no existe
    conexion = sqlite3.connect('tareas.db')

        # Para poder enviar comandos, necesitamos un "cursor"
    cursor = conexion.cursor()

        # --- PASO 2: Ejecutar un comando SQL ---
        # Usamos un string multilínea con triples comillas para que el SQL sea más legible
    comando_sql = """
        CREATE TABLE IF NOT EXISTS Tarea (
        id INTEGER PRIMARY KEY,
        descripcion TEXT NOT NULL,
        fecha_limite TEXT,
        prioridad TEXT,
        completada INTEGER
        )
        """

        # 'IF NOT EXISTS' evita que nos dé un error si la tabla ya ha sido creada
    cursor.execute(comando_sql)

        # Para que los cambios se guarden de forma permanente, hacemos un "commit"
    conexion.commit()

        # --- PASO 3: Cerrar la conexión ---
    conexion.close()

    print("Tabla 'Tarea' creada con éxito (si no existía ya).")

    #Codigo de Alejandro
    def añadir_película(self):
        print ("Has añadido una película")

    #Codigo de Pablo
    def modificar_película(self):
        print ("Has modificado una película")

    #Codigo de Álvaro
    def eliminar_película(self):
        print ("Has eliminado una película")

    if __name__ == "__main__":
        ventana_principal = tk.Tk()
        Pelicula = Pelicula(ventana_principal)
        ventana_principal.mainloop()