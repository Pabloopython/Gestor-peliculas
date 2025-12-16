import tkinter as tk
from tkinter import ttk # añade widgets
from database_manager import DatabaseManager


class App:

    def __init__(self):
        # Creamos la ventana
        self.ventana = tk.Tk()
        self.ventana.title("Gestor de películas")
        self.ventana.geometry("700x700")
        self.ventana.configure(bg="#2E3440")

        self.db = DatabaseManager('peliculas_gestor.db')
        self.id_pelicula_seleccionada = None #siver para saber qué película está seleccionada en la lista

        self.frame_centrado = tk.Frame(self.ventana, bg="#2E3440") #organizamos la interfaz
        self.frame_centrado.place(relx=0.5, rely=0.5, anchor="center")

        # Formulario donde rellenaremos los datos de la película. 
        self.frame_formulario = tk.Frame(self.frame_centrado, bg="#2E3440")
        self.frame_formulario.grid(row=0, column=0, padx=10, pady=10)

        self.barra_menu = tk.Menu(self.ventana)
        self.ventana.config(menu=self.barra_menu)

        # Añade un menú por el cual al salir de cierra el gestor
        menu_archivo = tk.Menu(self.barra_menu, tearoff=0)
        self.barra_menu.add_cascade(label="Cerrar página", menu=menu_archivo)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.ventana.destroy)

        # Creamos el menú desplegable "Ayuda" que también muestra información
        menu_ayuda = tk.Menu(self.barra_menu, tearoff=0)
        self.barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)
        menu_ayuda.add_command(label="Uso del programa",
                               command=self.mostrar_acerca_de)

        
        menu_archivo = tk.Menu(self.barra_menu, tearoff=0)
        self.barra_menu.add_cascade(label="Creadores", menu=menu_archivo)
        menu_archivo.add_separator()
        # Dentro del menú creamos una etiqueta en la que aparecen nuestros nombres
        menu_archivo.add_command(label="Alejandro Muñoz", state="disabled")
        menu_archivo.add_command(label="Pablo Chacón", state="disabled")
        menu_archivo.add_command(label="Álvaro Rodríguez", state="disabled")

        # Definimos los campos a completar
        self.campos_info = {
            "Nombre": {},
            "Descripción": {},
            "Director": {},
            "Protagonista": {},
            # "Valoración": {},
            # "Prioridad": {}
        }
        # Crea una etiqueta y un entry donde escribir
        for idx, etiqueta in enumerate(self.campos_info.keys()):
            lbl = tk.Label(
                self.frame_formulario,
                text=f"{etiqueta}:",
                fg="black",
                bg="#D3D3D3",
                font=("Arial", 12)
            )

            entry = tk.Entry(self.frame_formulario, width=50)

            lbl.grid(row=idx, column=2, padx=5, pady=5, ipady=5)
            entry.grid(row=idx, column=3, padx=5, pady=5, ipady=5)

            self.campos_info[etiqueta]["entry"] = entry

        # Aquí aparecerán todaas las peliculas guardadas
        self.frame_lista = tk.Frame(self.frame_centrado)
        self.frame_lista.grid(row=1, column=0, padx=10, pady=5)

        self.lista_tareas = tk.Listbox(self.frame_lista, width=100, height=10)
        self.scrollbar = tk.Scrollbar(
            self.frame_lista, orient="vertical", command=self.lista_tareas.yview)

        self.lista_tareas.config(yscrollcommand=self.scrollbar.set)

        self.lista_tareas.grid(row=0, column=0)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Creamos el Combobox que incluye la valoración de las peliculas
        tk.Label(self.frame_formulario, text="Valoración:", fg="black",
                 bg="#D3D3D3", font=("Arial", 12)).grid(row=4, column=2, padx=5, pady=5, ipady=5)
        self.combo_valo = ttk.Combobox(self.frame_formulario, values=["1/5", "2/5", "3/5", "4/5", "5/5"],
                                       state="readonly"  # Para que no se pueda escribir, solo seleccionar
                                       )
        self.combo_valo.grid(row=4, column=3, padx=5, pady=5, sticky="ew")
        self.combo_valo.current()

        # Creamos el Combobox que incluye la prioridad
        tk.Label(self.frame_formulario, text="Prioridad:", fg="black",
                 bg="#D3D3D3", font=("Arial", 12)).grid(row=5, column=2, padx=5, pady=5, ipady=5)
        self.combo_prio = ttk.Combobox(self.frame_formulario, values=["Baja", "Media", "Alta", "Urgente"],
                                       state="readonly"  # Para que no se pueda escribir, solo seleccionar
                                       )
        self.combo_prio.grid(row=5, column=3, padx=5, pady=5, sticky="ew")
        self.combo_prio.current()
        # Para cargar los datos al iniciar
        self.actualizar_lista()

        # Barra de estado, sirve para mostrar mensajes como “Guardado”, “Error”, etc
        self.barra_estado = tk.Label(
            self.frame_centrado,
            text="Listo",
            fg="black",
            bg="#81A1C1",
            font=("Arial", 12)
        )
        self.barra_estado.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        # --- Botones ---
        self.frame_botones = tk.Frame(self.frame_centrado, bg="#88C0D0")
        self.frame_botones.grid(row=2, column=0, padx=10, pady=10)

        # Relacionamos los tres botones con su función correspondiente
        botones = [
            ("Añadir Película", self.añadir_pelicula),
            ("Modificar Película", self.modificar_pelicula),
            ("Eliminar Película", self.eliminar_pelicula)
        ]

        # Creamos lista de botones con texto y comando (función) de cada uno:
        for i, (texto, comando) in enumerate(botones):
            # Creamos botón
            btn = tk.Button(
                self.frame_botones,
                text=texto,
                fg="black",
                bg="#88C0D0",
                font=("Arial", 12),
                command=comando
            )
            btn.grid(row=0, column=i, padx=10, pady=5)

        self.lista_tareas.bind('<<ListboxSelect>>', self.cargar_seleccion)

        # Iniciamos la interfaz
        self.ventana.mainloop()

    # ---------- MÉTODOS ----------
    def mostrar_acerca_de(self):
        # Toplevel crea una nueva ventana "hija" de la ventana principal
        ventana_acerca_de = tk.Toplevel(self.ventana)
        ventana_acerca_de.title("Información del Gestor")
        ventana_acerca_de.geometry("615x250")

        # Hacemos que la ventana sea "modal": bloquea la ventana principal
        ventana_acerca_de.grab_set()
        ventana_acerca_de.transient(self.ventana)

        # Mensajes de texto con la ayuda del programa
        tk.Label(ventana_acerca_de, text="Gestor de Películas ").pack(pady=20)
        tk.Label(ventana_acerca_de,
                 text="La función que tiene este gestor es que puedes añadir todas las películas que quieres ver para que no se te olviden.").pack(pady=5)
        tk.Label(ventana_acerca_de,
                 text="Además, puedes modificar las películas guardadas por si has tenido un error añadiendolas").pack(pady=5)
        tk.Label(ventana_acerca_de,
                 text="y si ya has visto la película tienes la opción de borrarla de la lista").pack(pady=5)

        boton_cerrar = tk.Button(
            ventana_acerca_de, text="Cerrar", command=ventana_acerca_de.destroy)
        boton_cerrar.pack(pady=20)

    def añadir_pelicula(self):
        # Lee los datos de las entradas 
        datos_entry = [self.campos_info[c]["entry"].get().strip()
                       for c in self.campos_info]

        # Lee los datos de los valores
        valoracion = self.combo_valo.get()
        prioridad = self.combo_prio.get()

        # En caso de que no rellenemos todos los datos
        if not all(datos_entry) or not valoracion or not prioridad:
            self.barra_estado.config(
                text="⚠️ Rellena todos los campos antes de añadir.")
            return

        # Unimos datos de entrada y valores
        datos = datos_entry + [valoracion, prioridad]

        self.db.añadir_pelicula(*datos)

        self.actualizar_lista()
        self.barra_estado.config(text="✅ Película añadida correctamente.")

        # Dejar campos en blanco para añadir otra película
        for campo in self.campos_info.values():
            campo["entry"].delete(0, tk.END)

        self.combo_valo.set("")
        self.combo_prio.set("")

    def modificar_pelicula(self):
        # Si no hay películas seleccionadas
        if not self.id_pelicula_seleccionada:
            self.barra_estado.config(
                text="⚠️ Selecciona una película para modificar.")
            return

        id_pelicula = self.id_pelicula_seleccionada

        datos_entry = [self.campos_info[c]["entry"].get().strip()
                       for c in self.campos_info]

        valoracion = self.combo_valo.get()
        prioridad = self.combo_prio.get()
        # Si no se han rellenado todos los campos
        if not all(datos_entry) or not valoracion or not prioridad:
            self.barra_estado.config(
                text="⚠️ Rellena todos los campos antes de modificar.")
            return

        # Para actualizar los datos de la película
        datos = datos_entry + [valoracion, prioridad]

        self.db.modificar_pelicula(*datos, id_pelicula)
        self.actualizar_lista()
        self.barra_estado.config(text="✏️ Película modificada correctamente.")

    def eliminar_pelicula(self):
        seleccion = self.lista_tareas.curselection()
        if not seleccion:
            self.barra_estado.config(
                text="⚠️ Selecciona una película para eliminar.")
            return

        # Recupera el id de la película
        index = seleccion[0]
        id_pelicula = self.peliculas_cache[index]

        # Eliminar en Database
        self.db.eliminar_pelicula(id_pelicula)

        # Actualizar lista
        self.actualizar_lista()
        self.barra_estado.config(text="🗑️ Película eliminada.")

    def actualizar_lista(self, event=None):
        # Borra toda la lista 
        self.lista_tareas.delete(0, tk.END)
        self.peliculas_cache = []

        peliculas = self.db.actualizar_lista()

        for pelicula in peliculas:
            # Cargar películas en la lista: (id, nombre, descripcion, director, protagonista, valoracion, prioridad)
            id_p, nom_t, desc_t, direc_t, prota_t, valo_t, prio_t = pelicula
            texto = f"{nom_t}| {desc_t} | {direc_t} | {prota_t} | {valo_t} | {prio_t}"
            self.lista_tareas.insert(tk.END, texto)
            self.peliculas_cache.append(id_p)

    def cargar_seleccion(self, event=None):
        # llenar campos con los datos de la película
        seleccion = self.lista_tareas.curselection()
        if not seleccion:
            return

        # Obtener índice y sacar el id 
        index = seleccion[0]
        id_pelicula = self.peliculas_cache[index]

        # Guardar el id seleccionado
        self.id_pelicula_seleccionada = id_pelicula

        datos = self.db.cargar_pelicula_seleccionada(id_pelicula)
        if not datos:
            return

        # Separa los valores
        entries = datos[:4]
        valoracion = datos[4]
        prioridad = datos[5]

        # Ajustar los Combobox con los nuevos valores
        for campo, valor in zip(self.campos_info.values(), entries):
            campo["entry"].delete(0, tk.END)
            campo["entry"].insert(0, valor)

        self.combo_valo.set(valoracion)
        self.combo_prio.set(prioridad)


# --- Ejecutar y arrancar la App ---
if __name__ == "__main__":
    app = App()
